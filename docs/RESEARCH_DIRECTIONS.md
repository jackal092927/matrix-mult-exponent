# Three independent research directions

These are research tasks, not assertions that a new bound exists. Read `SCOPE_AUDIT.md` before starting. Each lane has a different primary mathematical output: a new universal relation, an explicit tensor degeneration, or a structural algebra deformation. Sessions should work independently first and exchange complete candidate/proof files for adversarial checking afterward. No persistent sessions or remote computations were started by this audit.

## Lane A — New relations outside the convolution-profile obstruction

**Question.** Can genuinely new tensor relations force a common upper bound t_lambda<T<3/4 for all characters?

**Why this remains open.** The endpoint model is only a formal assignment. The known barrier for convolution-product sources uses consistent source orientation. Its proof explicitly does not cover cyclic source-leg permutations exchanging inputs with outputs, product-valued target blocks, or new tensor families. This opening should be tested as an opening in a particular proof, not advertised as a guaranteed way around every barrier.

**First bounded task.** Choose one mixed-orientation tensor-product family, such as products containing C(a,b) and a cyclic leg permutation of C(c,d), and one class of product-valued or additional-module target blocks. Write the complete source and target indices and exact restriction/degeneration equations before searching. Establish that the proposal is outside the existing dimension-based obstruction. If it reduces to ordinary consistently oriented convolution sources and full convolution direct sums, stop and record that reduction.

Use exact small instances to discover a candidate relation; evaluate the explicit assignment P_* and every already-recorded extended endpoint assignment against it immediately. A candidate inequality compatible with the countermodel can still be useful, but is not evidence of endpoint exclusion. A countermodel violation is only useful after every tensor map is proved valid simultaneously for all slices. Independent slice-wise basis changes do not define a tensor degeneration.

**Required first output.** Either (i) an exact tensor relation, its complete character inequality, an exact endpoint test, and the remaining lemma needed to obtain a uniform bound; or (ii) a scoped analytic obstruction for the frozen family. Provide a reusable certificate for any finite identity. Do not infer a universal inequality from finite tests.

**Success criterion.** Prove one of the universal spectral criteria in `SCOPE_AUDIT.md`, with a fixed positive margin. A weaker intermediate target is an actual new relation not satisfied by the formal endpoint, followed by a proof that it cannot be repaired by choosing values on the newly introduced tensors.

**Do not spend the session on:** tuning sector count at normalized shift 1/2, retuning Fourier periods, retaining the six existing orientations alone, the already-settled carry-free product substitution or diagonal normal-order filtration, or adding variables to the same first-Koszul family.

Primary start: [OpenAI pinned manuscript](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/build/paper.tex), [PR13 endpoint and global obstruction](https://github.com/selanavot/matrix-multiplication-all-fields/blob/10c889952eb175960ae304042247f7eb0df0e749/research/beyond-nine-quarters/profile.md), and [PR13 adversarial checks](https://github.com/selanavot/matrix-multiplication-all-fields/blob/10c889952eb175960ae304042247f7eb0df0e749/research/beyond-nine-quarters/barriers.md). Also read inherited E003/E004 proofs before claiming a relation is new to this program.

## Lane B — Exact growing sweet-piece degenerations

**Question.** Can an explicit low-rank completion or degeneration for a larger global-type sweet piece beat its exact transfer budget?

**First target.** S_3, the n=4 global-type tensor at N=9, with 5,376 coordinates per leg. Use words in G=(Z/2)^2, g=1, H={2,3}; the first two legs have exactly three zeros and six H symbols, the third exactly three g symbols and six H symbols; coefficients are one exactly when x XOR y=z coordinatewise. The zero/g-position sets partition the nine positions. This gives p=84 labels per leg, 1,680 supported blocks M_8, and 860,160 nonzeros. Reconstruct the blocking and tensor rather than importing the counts without checking them.

The exact sufficient finite target is

    border_rank(S_3) <= 9,041,
    9,041^4 < 84^4 2^27 < 9,042^4.

This is a target with a valid exponent transfer, not a known decomposition. Search for a symbolic, orbit-organized prefix with a residual admitting an explicit repair decomposition. Fix a term budget counting every prefix and correction term. General tensor rank-one terms are allowed; restricting to cubes is an additional ansatz that must be named. The output-shift model is the all-positive permutation-type tensor, not the alternating tensor used in the determinant example.

**First bounded task.** Specify a tractable structured ansatz and derive exact coefficient equations or a symbolic obstruction before launching a large solver. A small exemplar may establish that the ansatz is correctly implemented, but the final certificate must address S_3 itself or another explicitly justified improving target. Account for all powers of the degeneration parameter, prove cancellation of every negative coefficient, and identify the constant tensor exactly. A sparsely supported residual is not a bound on its rank.

The same three-dimensional first-leg Koszul projection used in E007 can certify at most 3L/2=8,064 here, below the target 9,041. Changing its random seed cannot exclude this target. Avoid a blind repeat of that feasibility gate or a progression of larger dense flattenings without an explicit cost and potency calculation.

**Required first output.** A frozen construction family, the exact rank/interpolation/field budget, a complete symbolic equation system, and either a verified candidate or a mathematically justified failure for that family. If numerical search is used later, follow it with exact coefficient recovery and independent full replay, including deliberate corrupt controls.

**Success criterion.** An exact or border-rank certificate below the strict sweet-piece threshold, with independently checked blocking hypotheses and the source theorem's asymptotic transfer. A small matrix-multiplication rank record or an arbitrary lower-rank tensor does not meet this criterion.

**Do not revisit:** n=4,N=3 target 14; n=8,N=3 target 169; n=4,N=6 target 339; the unchanged 15-term determinant prefix; or tensor powers of the known 17-term determinant decomposition. These routes have explicit exclusions or insufficient budgets in the inherited record.

Primary start: [Flavi–Jelisiejew–Michalek v2, sweet-piece theorem](https://arxiv.org/html/2408.02754v2) and [Conner–Huang–Landsberg v1, fixed-weight completion method](https://arxiv.org/abs/2009.11391v1). The latter is a source of mechanisms; its historical determinant is not the target tensor. Read the observatory's exact determinant replay and S_1/S_2 exclusions.

## Lane C — A structural smoothing or obstruction for the sweet-piece quotient

**Question.** Does the explicit quotient Q_k admit a smoothing for an improving value k>=5, or is there a structural obstruction to this sufficient route?

**Concrete algebra.** In the squarefree algebra

    A = C[x_1,y_1,...,x_(3k),y_(3k)]/(x_i^2,y_i^2),

let W_k be spanned by degree-2k squarefree monomials occupying exactly 2k pairs, with at most one variable from each pair. Let C_k be the unital subalgebra generated by W_k, graded by generator degree. Remove the degree-two socle spanned by monomials whose complement in the top monomial is not in W_k. The quotient Q_k has Hilbert function (1,L_k,L_k,1), L_k=binom(3k,k)4^k, and its degree-one cubic is S_k.

**Proved sufficient implication.** A smoothing of Q_5 gives border_rank(S_5)<=6,150,146 and therefore

    omega(C) <= log_32(6,150,146/3,003) < 9/4.

The inequality was checked through exact integer fourth powers. The smoothing itself is unknown. The quotient's millions of basis elements make a direct generic deformation search a poor initial task; seek a family-level construction or obstruction using its combinatorial structure.

**First bounded task.** Independently reconstruct the algebra presentation and distinguish it from the literal Veronese and the larger generated algebra. Identify a concrete candidate flat family, decomposition theorem, or necessary deformation condition that could apply for general k. Prove flatness, the special fiber, and reduced generic fiber for a proposed smoothing; a tangent direction or an initial algebra alone is insufficient.

The inherited observatory's next action is a Q_1 negative-tangent audit. Coordinate ownership so this new lane does not independently overwrite or duplicate that active work. Use its results as diagnostics only: nonsmoothability of Q_1 does not imply nonsmoothability of Q_5, and a nontranslation negative tangent does not prove smoothability even at k=1. The present lane should focus on the structural bridge to k>=5, or prove that a proposed bridge fails.

**Required first output.** A precise structural conjecture with its exact hypotheses, a proposed family/presentation or a proved obstruction, and a dependency graph connecting it to Q_5. State which implications are proved and which remain conjectural. If a smaller auxiliary algebra is used, give the actual tensor restriction and its full rank budget.

**Success criterion.** A verified smoothing for a sufficient k, another exact low-rank degeneration of the relevant multiplication tensor, or a proved obstruction that decisively closes the named construction. Only the first two combined with the transfer theorem can supply an exponent improvement.

Primary start: [Flavi–Jelisiejew–Michalek v2](https://arxiv.org/html/2408.02754v2), [Blaser–Lysikov v1](https://arxiv.org/abs/1606.04253v1), and [Jelisiejew v5, trivial negative tangents](https://arxiv.org/abs/1710.06124v5). The inherited quotient audit supplies the precise local algebra definition. Do not replace smoothable rank with cactus rank or border subrank.

## Common dispatch contract

For each independent session, preserve the baseline pin, the exact tensor/field, a short hypothesis list, the named forbidden rediscoveries, and a single canonical continuation file. Produce mathematical content and replayable exact certificates before claiming success. Keep failed candidates and their scopes. Record command outcomes and complete denominators when computations are performed; a running process is not a result.

Start with local exact arithmetic and symbolic reasoning. No paid API, remote/GPU allocation, or external communication is justified by these initial cards. Publishing a new bound requires an independent adversarial audit of the proof and transfer; merely assembling these research directions does not establish novelty or a mathematical improvement.
