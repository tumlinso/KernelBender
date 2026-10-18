# 06 — Match algebra to a different native resource


**Recognition cue.** A specialized operation is bilinear, bounded-integer, Boolean, min-plus, or table-like, but the obvious implementation expands it into generic floating arithmetic.

**Constructions.** Packed integer dot instructions can compute a bounded category score without expanding to float; they collapse products into a sum, so they cannot replace a task needing every individual product. An explicitly supported MMA form can realize small bilinear maps whose axes are local state or graph coordinates rather than minibatches. On an eligible Hopper target, an integer dynamic-programming recurrence may map to DPX instead of a longer compare/add sequence.

For each substitution write the exact algebra, intermediate ranges, required output information, layout and rounding. Four independent small products cannot implement a coupled system merely by reshaping its state. Dense tensor expansion of sparse Boolean data pays zeros and operand construction; AND+POPC or a short shuffle/add circuit may be the stronger baseline.

**Economic question.** Does arithmetic replaced exceed packing, conversions, routing, padding and extraction across the full lifetime? Can a packed operand serve several consumers before conversion? Do not add independent hardware peak rates to predict a feasible schedule.

**First discriminator.** Prove/test bounded integer range and extraction; use one-hot mapping and an independent reference for the selected MMA form. Inspect generated code only under the caller's permitted low-level policy to determine which path actually ran. Test the complete specialized operation, not just instruction issue.

Sources: [AT-M08], [AT-C08], [AT-M24], [AT-C10], [AT-R15], [HOPPER], [PTX]. No native integer Tensor Core support on V100 is inferred from a packed-integer intrinsic.
