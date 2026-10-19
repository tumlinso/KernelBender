"""Independent CPU checks for the authored Atlas-consolidation fixtures.

These test the fixture equations and boundary examples only. They do not test
KernelBender retrieval, CUDA code, or GPU performance.
"""

import unittest


def synchronous_threshold_update(offsets, indices, state):
    out = 0
    for v in range(len(offsets) - 1):
        active = sum(
            (state >> src) & 1
            for src in indices[offsets[v] : offsets[v + 1]]
        )
        if active >= 2:
            out |= 1 << v
    return out


def sequential_in_place_update(offsets, indices, state):
    for v in range(len(offsets) - 1):
        active = sum(
            (state >> src) & 1
            for src in indices[offsets[v] : offsets[v + 1]]
        )
        if active >= 2:
            state |= 1 << v
        else:
            state &= ~(1 << v)
    return state


def exact_threshold_screen(edges, query, threshold):
    """Sorted nonnegative edges with a sound suffix upper bound."""
    remaining = [0] * (len(edges) + 1)
    for i in range(len(edges) - 1, -1, -1):
        remaining[i] = remaining[i + 1] + edges[i][1]
    partial = 0
    for i, (column, weight) in enumerate(edges):
        partial += weight * query[column]
        if partial >= threshold:
            return True
        if partial + remaining[i + 1] < threshold:
            return False
    return partial >= threshold


class ConsolidationFixtureOracleTests(unittest.TestCase):
    def test_b1_synchronous_state_is_distinct_from_in_place(self):
        # v0 receives two active old sources and turns on. v1's second source
        # is v0, so it must stay off under the old-state contract.
        offsets = [0, 2, 4, 4, 4]
        indices = [1, 2, 0, 1]
        state = 0b0110
        self.assertEqual(synchronous_threshold_update(offsets, indices, state), 0b0001)
        self.assertEqual(sequential_in_place_update(offsets, indices, state), 0b0011)

    def test_b1_empty_and_threshold_boundaries(self):
        offsets = [0, 0, 1, 3]
        indices = [0, 1, 2]
        self.assertEqual(synchronous_threshold_update(offsets, indices, 0b111), 0b100)
        self.assertEqual(synchronous_threshold_update(offsets, indices, 0), 0)

    def test_b1_last_vertex_and_maximum_indegree(self):
        offsets = [0] * 64 + [63]
        indices = list(range(63))
        self.assertEqual(
            synchronous_threshold_update(offsets, indices, (1 << 63) - 1),
            1 << 63,
        )

    def test_b2_exact_threshold_and_above_maximum(self):
        row = [(0, 2), (1, 3), (2, 1)]
        query = (1, 0, 1)
        weighted_sum = sum(weight * query[col] for col, weight in row)
        self.assertEqual(weighted_sum, 3)
        self.assertEqual(int(weighted_sum >= 3), 1)
        self.assertEqual(int(weighted_sum >= 4), 0)
        self.assertEqual(int(weighted_sum >= 7), 0)

    def test_b2_screening_composition_matches_full_sum_at_boundaries(self):
        edges = [(1, 7), (3, 6), (0, 3), (2, 1)]
        for query in ((0, 0, 0, 0), (1, 1, 1, 1), (1, 0, 1, 0), (0, 1, 0, 1)):
            total = sum(weight * query[column] for column, weight in edges)
            for threshold in (1, total, total + 1, 17, 18):
                expected = total >= threshold
                self.assertEqual(exact_threshold_screen(edges, query, threshold), expected)

    def test_b3_owner_map_is_unique_for_four_samples_per_warp(self):
        owners = set()
        for sample in range(4):
            for j in range(4):
                for i in range(4):
                    p = 4 * j + i
                    lane = (p + 16 * (sample % 2)) % 32
                    slot = sample // 2
                    owners.add((lane, slot))
        self.assertEqual(len(owners), 64)

    def test_b3_small_matrix_product_coordinate_reference(self):
        a = [[1, 2, 0, 1], [0, 1, 3, 0], [2, 0, 1, 1], [1, 1, 0, 2]]
        b = [[1, 0, 2, 1], [2, 1, 0, 0], [0, 1, 1, 2], [1, 0, 1, 1]]
        c = [
            [sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)]
            for i in range(4)
        ]
        self.assertEqual(c, [[6, 2, 3, 2], [2, 4, 3, 6], [3, 1, 6, 5], [5, 1, 4, 3]])
        self.assertEqual(c[0][0], 6)
        self.assertEqual(c[0][3], 2)
        self.assertEqual(c[3][0], 5)
        self.assertEqual(c[3][3], 3)


if __name__ == "__main__":
    unittest.main()
