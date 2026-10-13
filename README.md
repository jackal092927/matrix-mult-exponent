# Omega Relay: matrix multiplication below 9/4

A public research project for lowering the **arithmetic matrix multiplication
exponent**. Our first target is a rigorous bound **omega(C) < 9/4**, building on
[OpenAI's 9/4 construction](https://github.com/openai/math/tree/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026).
Humans and AI-assisted researchers can contribute constructions, exact
certificates, proofs, independent audits, useful negative results and reusable
search methods through issues and pull requests.

**Launch status:** the 9/4 baseline is attributed upstream. This project has
not established a smaller omega, a practical GEMM speedup or a new world record.
Independent finite algebra checks, a formal proof and external mathematical
review have different scopes; every contribution must say which it supplies.

## The question

For a fixed scalar field F, omega(F) is the infimum of admissible exponents
for arithmetic algorithms that multiply every pair of n-by-n matrices. Our
initial field is C. A successful main contribution gives an unconditional
arithmetic upper bound beta < 9/4 with a complete family/transfer proof,
including field assumptions and every asymptotic cost. Conditional improvements
are welcome when their unresolved premises are explicit; they receive a separate
status.

Extending an unchanged exponent to more fields, optimizing fixed-size tensor
rank, improving numerical matrix throughput, or reducing integer multiplication's
bit complexity are useful related work with their own objectives. They do not
automatically discharge this project's omega target.

## Directions to pursue

| Lane | Construction question | Evidence required |
| --- | --- | --- |
| Spectrum and sector inequalities | Can new coupled tensor relations improve the polynomial-multiplication profile beyond the current 4/3 growth route? | Exact local identities plus a uniform argument for every relevant spectral character, normalization and omega transfer |
| Growing tensor powers | Can global-type sweet pieces admit explicit low-rank or border-rank constructions within an improving budget? | Full coefficient certificate, complete rank/interpolation cost and a proved asymptotic transfer |
| Algebraic constructions | Can an appropriate sweet-piece algebra admit a smoothing or another rigorously low-border-rank unrestriction? | An actual flat deformation or rank construction; dimension alone is insufficient |
| Finite discovery and verification | Can numerical/flip-graph ideas yield exact reusable decompositions or ingredients for the above lanes? | Exact coefficient recovery and independent verification; explain the gap to a global exponent |

Read [research directions](docs/RESEARCH_DIRECTIONS.md), the
[scope audit](docs/SCOPE_AUDIT.md), and [related work](docs/RELATED_WORK.md).
The agenda was informed by a user-supplied discussion and checked against
primary sources. Its promising directions are research hypotheses, not results.

For the spectral route, the schematic implication omega <= 3t requires a common
upper bound on the relevant exponent parameters **for all characters**. Proving
one stronger numerical profile, testing finitely many dimensions, or selecting
one character is insufficient. In particular, a hypothetical uniform profile
growth 4/3+delta yields 3/(4/3+delta) only after all source hypotheses and
comparison steps are proved.

## Reuse what has already been learned

Our earlier local research identified several scoped boundaries: Fourier-period
tuning preserved its entropy exponent; one higher-variable Koszul family admits
an endpoint countermodel; single-copy sweet-piece rank targets and the n=4,N=6
target were excluded by exact border-rank certificates. A low-dimensional
Gorenstein quotient retains a desired tensor, but its smoothability remains
unproved. These close particular routes, not the general possibility of
omega < 9/4. Read the scope audit before reopening one of those searches.

Existing source records and immutable receipts are retained locally. This launch
does not copy private operational logs, entire conversations, credentials,
unlicensed upstream search code or giant duplicate archives into GitHub.

## A research relay with an independent gate

1. Pick an issue and specify the exact tensor, field, target, assumptions and
   predecessor revisions.
2. Freeze a bounded experiment/proof card with the proposed change, baseline,
   budgets, controls and possible endpoints.
3. Produce a candidate or a useful negative result. Preserve failures, timeouts
   and counterexamples.
4. Hand the evidence to an independent verifier. A generator cannot accept its
   own result.
5. Submit a PR containing the proof/certificate, reproducible commands,
   provenance and exact claim scope. Integration, numerical priority and
   publication are reviewed separately.

[CONTRIBUTING.md](CONTRIBUTING.md) specifies the contribution contract.
[Research issues](https://github.com/jackal092927/matrix-mult-exponent/issues)
are the public agenda. Local worker state and handoffs stay in ignored runtime
directories; concise source-backed milestones are synced to GitHub.

## Exact finite-certificate baseline

The initial executable gate accepts rational finite bilinear decompositions.
It checks every tensor coefficient independently of the producing search code.
Known scalar multiplication and Strassen's rank-7 2-by-2 scheme serve as
reproduction baselines. Their acceptance supplies no new omega record.

```sh
python3 scripts/verify_certificate.py
python3 -m unittest discover -s tests -v
```

See [the certificate contract](docs/CERTIFICATE_CONTRACT.md). Border-rank
families, symbolic degenerations, spectral inequalities and smoothability proofs
need further domain-specific checks; the rational finite gate does not claim to
verify them. For an exact square n-by-n rank-r block, the strict inequality
r^4 < n^9 is a useful exact threshold for log_n(r) < 9/4, alongside the complete
recursive arithmetic construction. The repository does not turn an arbitrary
local tensor rank into that square-block theorem.

## Working together

Independent GPT-6 Astra sessions use xhigh reasoning and separate lane
directories. One coordinator owns public integrations; a separate evaluator
checks submitted evidence. Source revisions and settled negative results are
shared so work can build on prior findings. Subscription sessions are distinct
from paid API calls. Remote experiments require an actual authorized allocation
and run receipt; idle hardware is not an allocation.

We record source authorship, inherited ideas, new constructions and audit work
separately. Account handles, model mentions and PR volume do not measure
independent agents, mathematical novelty or research success.

## Attribution and source status

OpenAI supplied the original 9/4 construction and published proof sources.
[All-fields extensions](https://github.com/selanavot/matrix-multiplication-all-fields)
are credited as extensions of scope. Finite discovery tools and their licenses
are listed in [related work](docs/RELATED_WORK.md). Baseline receipts specify
what was independently replayed here; reading an upstream verification report
is not a fresh local Lean build.

Original new project code is licensed under [MIT](LICENSE). Referenced or imported
third-party material retains its own authorship and license; this license does
not relicense upstream proofs, articles, datasets or discussions.
