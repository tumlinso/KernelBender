# Native Boolean transition candidate

## Contract and construction

For each step, site `i` reads the previous epoch's bytes at `i` and `(i-1) mod N), plus the per-site mask byte, then selects one of the 32 rule bytes. The API requires the complete final byte array and the final number of state-3 sites.

For `N <= 1024`, `small_epoch` keeps both state buffers, the mask, and the 32-byte rule in shared memory. One CTA performs all steps with a barrier between ping-pong buffers, writes every output site, reduces the final state-3 count, and writes the count. This avoids per-step launches and temporary global allocations for the supplied small and 1024-site cases.

For larger inputs whose shared-memory footprint is at most 40 KiB, `fused_tiles` assigns 256 output sites to each CTA. Since dependencies move only toward the left, a tile needs a left halo of exactly `steps` initial sites and no right halo. It loads the `256 + steps`-site interval starting at `tile_base - steps`, wraps each load modulo `N`, and shrinks the valid left boundary by one site per local step. After the final step it writes the tile's complete in-range output and atomically contributes its local count. The host zeros the count in the caller's stream before launching this kernel.

When the fused tile would exceed the 40 KiB dynamic shared-memory bound, the candidate falls back to a conventional per-step global kernel and final count pass. This keeps arbitrary positive step counts within the semantic contract without assuming a hardware-specific opt-in shared-memory limit.

## Rationale and rejection conditions

The state domain is small enough to consider bitplanes, but the rule is an arbitrary per-call 32-entry table and each output byte is required. A packed representation would add encoding, neighbor routing, arbitrary-table selection, and decoding at the API boundary. The shared byte representation preserves the rule lookup directly and removes repeated global epochs and launches for the provided shapes. This is a cost hypothesis, not a measured advantage.

The construction should be rejected if an independent oracle finds any mismatch on exhaustive local tuples, periodic short lengths, odd tails, or held-out shapes. Its expected benefit should be judged only by full-call epoch latency against the supplied scalar baseline, including the count initialization and any fallback allocation cost.

## Validation and limits

The supplied CPU-only build helper completed its corrected SM70 compilation successfully. The helper archives source, output, and hashes under `/work/build-history/attempt-02`. No GPU execution, independent runtime correctness check, held-out validation, or latency measurement was available in this isolated attempt. The compile result establishes buildability only.
