"""Focused retrieval checks for the authored Atlas-derived skill library."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "kernelbender"


class AtlasRetrievalTests(unittest.TestCase):
    def test_every_mechanism_and_composition_id_has_a_retrieval_home(self) -> None:
        corpus = "\n".join(
            path.read_text(encoding="utf-8") for path in (SKILL / "references").rglob("*.md")
        )
        expected = {
            "M": set(range(1, 53)),
            "C": set(range(40)),
        }
        for kind, values in expected.items():
            observed = {int(value) for value in re.findall(rf"\b{kind}(\d{{2}})\b", corpus)}
            with self.subTest(kind=kind):
                self.assertEqual(values, observed)

    def test_problem_routes_reach_concrete_constructions_and_controls(self) -> None:
        index = (SKILL / "references" / "opportunity-index.md").read_text(encoding="utf-8")
        routes = {
            "mask, threshold, count": "compositions/discrete-state.md",
            "fixed local graph patches": "compositions/positional-routing.md",
            "short score": "compositions/arithmetic-circuits.md",
            "bilinear operator": "compositions/tensor-circuits.md",
            "Producer and consumer": "compositions/ownership-fragments.md",
            "decision boundary": "compositions/screening-refinement.md",
            "Partitioned data": "compositions/system-compositions.md",
            "Routine dense GEMM": "CUDA",
        }
        for cue, destination in routes.items():
            with self.subTest(cue=cue):
                self.assertIn(cue, index)
                if destination != "CUDA":
                    self.assertIn(destination, index)
                    self.assertTrue((SKILL / "references" / destination).is_file())
        self.assertIn("cuBLAS/cuBLASLt", index)
        self.assertIn("No exotic affordance is required", index)

    def test_representative_cards_show_equations_costs_and_falsifiers(self) -> None:
        discrete = (SKILL / "references/compositions/discrete-state.md").read_text(encoding="utf-8")
        tensor = (SKILL / "references/compositions/tensor-circuits.md").read_text(encoding="utf-8")
        screening = (SKILL / "references/compositions/screening-refinement.md").read_text(encoding="utf-8")
        ownership = (SKILL / "references/compositions/ownership-fragments.md").read_text(encoding="utf-8")

        self.assertIn("majority(a,b,c)", discrete)
        self.assertIn("encode + steps", discrete)
        self.assertIn("scalar/vector transitions", discrete)
        self.assertIn("four independent `8×8×4` products", tensor)
        self.assertIn("Q ∘ P⁻¹", ownership)
        self.assertIn("|s - ŝ| <= ε", screening)
        self.assertIn("direct exact", screening)
        self.assertIn("Reject", screening)

    def test_exact_hardware_and_evidence_pages_are_reachable(self) -> None:
        registry = (SKILL / "references/wiki-contracts.md").read_text(encoding="utf-8")
        required = {
            "hw-volta-mma",
            "hw-volta-participation",
            "hw-volta-numerics",
            "hw-volta-resources",
            "hw-volta-feature-boundaries",
            "hw-volta-operand-delivery",
            "hw-volta-integer-routing",
            "hw-volta-vmm-addressing",
            "hw-volta-atlas-e09-mma-coordinate",
            "hw-volta-atlas-e11-packed-intersection",
            "hw-volta-atlas-e12-independent-transform",
            "hw-volta-atlas-e16-resident-scheduling",
            "hw-volta-atlas-e23-vmm-aliasing",
            "hw-volta-atlas-e39-bitplane-addition",
            "hw-ampere-async-copy",
            "hw-ampere-tensor-operations",
            "hw-ampere-memory-resources",
        }
        for page_id in required:
            with self.subTest(page_id=page_id):
                self.assertIn(f"`{page_id}`", registry)
        self.assertIn("--architecture sm70", registry)
        self.assertIn("--architecture sm80", registry)
        self.assertIn("get_page.py hw-volta-mma --follow-sources", registry)
        bit_routing = (SKILL / "references/affordances/bit-routing.md").read_text(encoding="utf-8")
        arithmetic = (SKILL / "references/affordances/arithmetic-tensor.md").read_text(encoding="utf-8")
        positional = (SKILL / "references/compositions/positional-routing.md").read_text(encoding="utf-8")
        arithmetic_circuits = (SKILL / "references/compositions/arithmetic-circuits.md").read_text(encoding="utf-8")
        self.assertIn("hw-volta-integer-routing", bit_routing)
        self.assertIn("hw-volta-integer-routing", arithmetic)
        self.assertIn("hw-volta-integer-routing", positional)
        self.assertIn("hw-volta-integer-routing", arithmetic_circuits)

    def test_measured_and_unsupported_claim_boundaries_survive_retrieval(self) -> None:
        arithmetic = (SKILL / "references/affordances/arithmetic-tensor.md").read_text(encoding="utf-8")
        system = (SKILL / "references/affordances/system-boundaries.md").read_text(encoding="utf-8")
        wiki_map = (SKILL / "references/wiki-contracts.md").read_text(encoding="utf-8")

        self.assertRegex(arithmetic, re.compile(r"E09.*not WMMA raw ownership", re.DOTALL))
        self.assertRegex(arithmetic, re.compile(r"E12.*not test `M\^r x`", re.DOTALL))
        self.assertIn("actual iteration count one", arithmetic)
        self.assertIn("no bitplane crossover established", arithmetic)
        self.assertIn("E27–E30", system)
        self.assertIn("remain `NOT_RUN`", system)
        self.assertIn("power-of-two mask and two-segment alternatives were not tested", system)
        self.assertIn("does not make that command a public application interface", system)
        self.assertIn("`sm80`; Ampere capability", wiki_map)
        self.assertIn("Never infer this mechanism for `sm70`", wiki_map)


if __name__ == "__main__":
    unittest.main()
