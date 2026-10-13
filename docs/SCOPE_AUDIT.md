# Scope and sufficient targets

Audit date: 2026-10-12, America/Los_Angeles. This project seeks a proved arithmetic matrix-multiplication exponent strictly below 9/4. No new exponent bound is established by this audit. An improved complex-field bound is a valid first target; a claim over other fields requires its own transfer argument. Extending the existing 9/4 bound to additional fields is useful prior work, but does not meet this project's objective.

## Primary baseline and reading receipt

The baseline is OpenAI's *An Upper Bound of 9/4 for the Matrix Multiplication Exponent*, pinned to commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`:

- [Manuscript source](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/build/paper.tex).
- [Actual exported Lean theorem](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/OAI/LinearAlgebra/MatrixMultiplication/Main.lean), `OAI.MatrixMultiplication.complex_omega_le_nine_quarters`.

The primary TeX was fetched again at this exact commit and compared byte-for-byte with the inherited archive. Both have SHA-256 `c396f2580a711b8b9e51ecf1265cb0e691acd745943f81bfc14ec0df209e1028`. The character definitions, profile normalization, diagonal-growth proof, detecting-character implication, and arithmetic conversion were directly inspected. This audit did not rebuild Lean or independently reprove the detecting-character appendix. The pinned commit is a reproducible source identity, not a promise that the moving main branch will remain there.

## What the spectral shorthand actually means

Work in the semiring of complex tensors modulo mutual restriction. A character lambda is normalized, additive on full direct sums, multiplicative on tensor products, and monotone under restriction. Its values on the three oriented dot products determine exponents p_X, p_Y, p_Z. Define

    t_lambda = (p_X + p_Y + p_Z)/3 > 0,
    lambda(M_n) = n^(3 t_lambda),
    C(a,b) = sum_{i=0}^{a-1} sum_{j=0}^{b-1} x_i y_j z_(i+j),
    P_lambda(a,b) = (product_{pi in S_3} lambda_pi(C(a,b)))^(1/(6 t_lambda)).

Here a and b are positive integers, lambda_pi means lambda after the specified leg permutation, and rank(C(a,b)) = a+b-1. The derived profile is not itself asserted to be an additive tensor character. Its normalization matters.

The inspected source establishes, for each character:

    P_lambda(a,b) = P_lambda(b,a) > 0,
    P_lambda(1,b) = b,
    P_lambda(a,b) <= (a+b-1)^(1/t_lambda),
    2 P_lambda(a,b) >= P_lambda(a,b-1) + P_lambda(a,b+1)  [b>=2],
    P_lambda(a,3h+a-1) >= 3 P_lambda(a,h)                 [a,h>=1].

The last two properties imply P_lambda(a,a) >= a^(4/3) for every positive integer a. Comparison with the rank upper bound as a tends to infinity gives t_lambda <= 3/4 for every character.

The statement “omega <= 3t” must not be used with the t of one arbitrary character. The valid sufficient implication is

    [for every tensor character lambda, t_lambda <= T] ==> omega(C) <= 3T.

For completeness, let nu = inf_{d>=2} log_d rank(M_d). For each d, the source's detecting-character lemma supplies a character, possibly depending on d, with value at least ceil(d^nu)-1 on M_d. The universal bound gives d^nu <= d^(3T)+1. Letting d grow proves nu <= 3T; the source's fixed-size recursive bilinear algorithm and padding argument then give the arithmetic exponent bound. There is no assertion of an exact O(n^(3T)) algorithm without epsilon slack.

## Safe sufficient spectral improvement criteria

The following are deductions from the inspected framework, not new constructions.

**Growth criterion.** Find one delta>0 such that for every actual tensor character lambda,

    limsup_{a -> infinity} log(P_lambda(a,a))/log(a) >= 4/3 + delta.

Then t_lambda <= 1/(4/3+delta) for every lambda, and

    omega(C) <= 3/(4/3+delta) < 9/4.

An easier-to-state but stronger premise is P_lambda(a,a) >= c_lambda a^(4/3+delta) for all sufficiently large a, with c_lambda>0. The constants and starting index may depend on lambda; delta must be common to all lambda. Even a character-dependent unbounded subsequence suffices for the displayed limsup criterion. A finite numerical fit, a stronger bound for one known character, or character-dependent positive margins with no common bound does not establish this criterion.

**Finite universal criterion.** It would also suffice to exhibit a fixed integer a_0>1 and fixed real B>1 satisfying

    B^3 > (2a_0-1)^4,
    P_lambda(a_0,a_0) >= B  for every actual tensor character lambda.

Then t_lambda <= log(2a_0-1)/log(B) < 3/4 uniformly. This finite criterion avoids inferring an asymptotic growth law from bounded experiments, but proving the universal inequality is still the substantive missing mathematics.

## Existing endpoint model and exclusions

The [PR13 profile at its pinned head](https://github.com/selanavot/matrix-multiplication-all-fields/blob/10c889952eb175960ae304042247f7eb0df0e749/research/beyond-nine-quarters/profile.md) and its [adversarial barrier audit](https://github.com/selanavot/matrix-multiplication-all-fields/blob/10c889952eb175960ae304042247f7eb0df0e749/research/beyond-nine-quarters/barriers.md) give the explicit formal endpoint

    u=min(a,b), v=max(a,b),
    P_*(a,b) = ((3u-1)/2)^(1/3) * (v+(u-1)/2).

It satisfies the scalar constraints at t=3/4 and has diagonal growth exponent exactly 4/3. It has not been shown to arise from an actual tensor character. This is a method obstruction, not a lower bound on omega. The PR's recorded state is closed and unmerged; this audit read its pinned contents rather than rechecking its current lifecycle state.

Do not restart these routes under a new name:

| Route already examined | Retained conclusion and scope |
| --- | --- |
| Better constants, more iterations, or more sectors with normalized shift 1/2 | The same global scalar endpoint remains feasible. |
| Retaining six orientations or optimizing the existing entropy probabilities separately | The formal equal-orientation assignment passes these local inequalities. New tensor relations are required. |
| Carry-free Kronecker substitution; consistently oriented convolution-product sources degenerating to full direct sums of convolutions | PR13's global dimension/profile arguments preserve the endpoint, including arbitrary target-block leg permutations. |
| Merely shortening the Fourier separation period or tuning auxiliary dimensions | Observatory E002 proved no improvement to the shared-leg entropy exponent. |
| The tested all-character edge comparison on oriented convolutions and formal sums/products | Observatory E003 gives a global compatible endpoint assignment; it is not a character-existence theorem. |
| The first-Koszul higher-variable family and its listed side conditions | Observatory E004 gives a global extension of the endpoint model. More variables alone do not help. |
| Single-copy sweet-piece targets at n=4 and n=8 | E005 complex border-rank lower bounds 17 and 179 exclude the proposed targets 14 and 169. |
| The n=4 global-type sweet piece at N=6 | E007 complex border rank at least 359 excludes the sufficient target 339. |
| The two-leg chimney restriction | Its asymptotic exponential base remains n; the three-leg sweet piece is a different object. |
| Fixed first 15 terms of the reproduced determinant formula, changing only independent-leg diagonal weights | The saved six-coefficient contradiction rules out repairing that fixed prefix this way. It does not cover changed vectors or general degenerations. |

The historical 17-term determinant border decomposition was exactly reproduced in E006. It is a baseline and cancellation mechanism, not a new result or an improving construction. Its tensor powers do not meet the relevant 9/4 budget. The separate displayed 42-term q=4 square expression in [Conner–Huang–Landsberg v1](https://arxiv.org/abs/2009.11391v1) remains numerical evidence in the inspected source; a small floating-point residual is not an exact border-rank certificate.

## A second sufficient target: growing sweet pieces

The source theorem `thm:sweet_bound` in [Flavi–Jelisiejew–Michalek v2, Section 6](https://arxiv.org/html/2408.02754v2) concerns a tight sweet piece with uniform equal blocking marginals, blocks isomorphic to M_a, p block labels per leg, and asymptotic rank r. It gives omega <= log_a(r/p). A finite exact-rank or complex border-rank upper bound R also bounds asymptotic rank, with the standard fixed-degeneration interpolation passage in the border-rank case. All blocking hypotheses must be verified for the actual tensor.

For the inherited n=4 global-type family S_k at N=3k:

    p_k = binom(3k,k),   a_k = 2^k,   L_k = p_k 4^k,
    sufficient condition: border_rank(S_k) <= R < p_k 2^(9k/4).

S_k has L_k coordinates on each leg. This strict threshold can be checked with integers as R^4 < p_k^4 2^(9k). The following largest sufficient integer values were recomputed exactly during this audit:

| k | L_k | Largest sufficient integer R | Current inherited status |
| ---: | ---: | ---: | --- |
| 1 | 12 | 14 | Excluded: border rank >=17 |
| 2 | 240 | 339 | Excluded: border rank >=359 |
| 3 | 5,376 | 9,041 | No upper bound meeting this target supplied |
| 4 | 126,720 | 253,439 | No upper bound meeting this target supplied; 253,440 gives equality, not improvement |
| 5 | 3,075,072 | 7,313,795 | No upper bound meeting this target supplied |

A rank lower bound on S_1 or S_2 does not exclude a better asymptotic rank or these larger global-type tensors. S_k is not interchangeable with S_1 tensor-powered k times.

## Conditional algebra route and inherited state

The observatory's `VERONESE_QUOTIENT_AUDIT.md` defines an explicit socle quotient Q_k with Hilbert function (1,L_k,L_k,1), length 2L_k+2, and degree-one multiplication tensor S_k. Its universal algebra calculation is accompanied by exact finite reconstruction at k=1,2. If Q_k is smoothable over C, restriction of a smoothing of its multiplication tensor gives border_rank(S_k) <= 2L_k+2. This agrees with the algebra/tensor degeneration framework of [Blaser–Lysikov](https://arxiv.org/abs/1606.04253v1).

The implication is proved conditionally; smoothability is UNKNOWN at every k in the inherited record. At k=5 it would give rank at most 6,150,146, below the strict improving budget. Smoothability for unbounded k would imply omega=2. Neither premise follows from the length, the Gorenstein property, smoothability of a parent algebra, or smoothability of a quotient's initial algebra.

The literal Veronese algebra, the sweet-generated algebra, and Q_k have different dimensions. The inherited source/example discrepancy must remain recorded rather than silently repairing the printed statement. Cactus rank, smoothable rank, tensor border rank, border subrank, and Kronecker powers are distinct invariants or operations.

The local handoff read for this audit was `distributed-research-observatory/research/OMEGA_DISCUSSION_HANDOFF.md`, together with `omega/NEXT_EXPERIMENT.md`, `ROUND6_STATUS.md`, `ledgers/CLAIMS.md`, `ledgers/SOURCES.md`, and `ledgers/EXPERIMENTS.md`. **NEXT_EXPERIMENT.md still proposes E007; Round 6 and completed E007/E008 supersede that proposal.** The latest completed state calls for an exact deformation audit of Q_1, with no tangent computation yet recorded in that snapshot. A Q_1 finding cannot be generalized to k>=5 without proof.

Local evidence locators, relative to the observatory's `omega/` directory, are `PROOF_PACKAGE.md`, `reports/HIGHER_KOSZUL_PROOF.md`, `reports/SWEET_RANK_CERTIFICATES.md`, `reports/SWEET_CHIMNEY_LIMIT.md`, `reports/DETERMINANT_BORDER_REPLAY.md`, `reports/GLOBAL_SWEET_N6_PROOF.md`, and `reports/VERONESE_QUOTIENT_AUDIT.md`; the corresponding immutable run receipts are indexed in the experiment ledger. They are inherited local evidence, not external peer review. If their claims are used in a public certificate, bundle the necessary statements and independently replayable evidence with stable public links.

## Acceptance boundary

A successful result must specify the field and arithmetic model, give either a universal spectral proof or a complete construction plus asymptotic transfer, and prove a strict numerical exponent below 9/4. Numerical discovery, exact finite identities, formal proof exports, local replay, and external review are separate states. Negative results and useful tooling are legitimate intermediate outputs; none alone completes the exponent objective.
