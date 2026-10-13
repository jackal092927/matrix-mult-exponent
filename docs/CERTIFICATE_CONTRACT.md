# Exact finite bilinear certificate contract

This lane checks a small, exact matrix multiplication algorithm over **Q**. It is a launch scaffold for auditable submissions. It does not check asymptotic constructions, border rank, degeneration limits, numerical approximations, or claims of a new world record.

## Run the intake

From the repository root, using Python 3.10 or newer:

```sh
python3 scripts/verify_certificate.py
python3 scripts/verify_certificate.py --manifest submissions/strassen-2x2-rank7.json
python3 -m unittest discover -s tests -v
```

The first command verifies every top-level `submissions/*.json` manifest, in sorted order. Successful intake prints JSON receipts and exits 0. Rejection prints an error receipt and exits 1. The checked-in `submissions/receipts/baseline-intake.json` is a reproducible example; fresh invocation is the authority after any file changes. Receipt subdirectories are not consumed as submissions. No packages, network requests, contributor programs, remote compute, or API calls are needed by these commands.

## Mathematical meaning

The dimensions `(m,k,n)` specify `A` of shape `m by k`, `B` of shape `k by n`, and `C = AB` of shape `m by n`. All three coefficient vectors use row-major order. For each product term `t`:

```text
p_t = (sum_u a_t[u] A_flat[u]) (sum_v b_t[v] B_flat[v])
C_flat[w] = sum_t c_t[w] p_t
```

The validator constructs the full coefficient tensor

```text
T[w,u,v] = sum_t c_t[w] a_t[u] b_t[v].
```

It checks **every** entry, including those required to be zero. The required entry is 1 exactly when `w=(i,j)`, `u=(i,h)`, and `v=(h,j)` for some common `h`; all other entries must be 0. Arithmetic uses Python's exact `Fraction` type. There is no numerical tolerance, random evaluation, sampled coefficient check, or executable field in the format.

Acceptance proves tensor rank over Q is **at most** the declared number of products. It does not prove minimal rank. Every factor must be nonzero, but the validator does not attempt to identify redundant or canceling products.

## Certificate and manifest

`schema/certificate.schema.json` and `schema/submission.schema.json` describe the JSON shapes. `scripts/verify_certificate.py` performs the authoritative structural and semantic checks without a schema library. A schema-only check cannot prove the identity or canonical fraction reduction.

A certificate has exactly these keys:

| Key | Meaning |
| --- | --- |
| `format` | `matrix-mult-bilinear-v1` |
| `domain` | `Q` |
| `dimensions` | Exactly the integer fields `m`, `k`, `n`, each in 1 through 4 |
| `declared_rank` | Integer in 1 through 64, equal to the number of terms |
| `terms` | List of objects containing exactly `a`, `b`, `c` vectors |

Vector lengths are `m*k`, `k*n`, and `m*n`, respectively. Each coefficient is a **string**, either an integer such as `"-1"`, `"0"`, or `"7"`, or a reduced fraction such as `"-2/3"`. Numerator magnitude and positive denominator are each at most nine decimal digits. `"2/4"`, `"1/1"`, `"-0"`, decimals, floats, booleans, and numeric JSON coefficients are rejected. Duplicate keys, nonstandard numeric constants, additional fields, and files larger than 1 MiB are rejected.

A submission manifest pins the raw-byte SHA256, dimensions, domain, and declared rank of its certificate. A formatting-only certificate edit changes its hash and requires an explicit manifest update. It also supplies:

| Key | Meaning |
| --- | --- |
| `format` | `matrix-mult-intake-v1` |
| `certificate` | `certificates/baselines/NAME.json` or `certificates/candidates/NAME.json` |
| `classification` | `known_baseline` or `candidate`, consistent with the directory |
| `attribution` | Authors, title, year, and HTTPS source URL |
| `claim` | `exact_identity` or `square_recursion_bound` |

The complete examples are in `submissions/`. Attribution and classification are contributor declarations; acceptance does not independently establish authorship, source contents, priority, or novelty. The receipt explicitly says attribution was not verified by the validator. Do not label a known algorithm as a new discovery.

Paths are local, relative, and restricted to the documented directory depth and safe filename characters. Traversal components, empty components, absolute paths, backslashes, and symlinks are rejected. Intake accepts at most 128 manifests. These limits keep this lane small and auditable; larger constructions require a separately reviewed format change.

New candidates belong in `certificates/candidates/` with a matching top-level submission manifest. JSON is the entire input. Contributor scripts and external proof links are never executed or fetched. Neither certificate nor manifest may assert a decimal exponent, `omega < 9/4`, border-rank result, or alternative computational model. Such extra fields or claim values are rejected.

## Square recursion proof

For an accepted identity with `m=k=n=b >= 2` and `r` products, replace each scalar input with an `N/b by N/b` block and recurse on the `r` ordered products. The identity is bilinear, so this substitution preserves the order of the two operands. Rational coefficients are central and fixed. The remaining additions and multiplications by fixed rational constants cost `O(N^2)` exact field operations for this fixed certificate.

The resulting recurrence on powers of `b` is

```text
T(N) <= r T(N/b) + O(N^2).
```

The matrix multiplication tensor has flattening rank `b^2`, so a valid decomposition has `r >= b^2`. When `r > b^2`, the recurrence gives `O(N^(log_b r))`; when `r = b^2`, it gives `O(N^2 log N)`. Padding arbitrary sizes to a power of `b` costs only a constant factor. By the definition of the arithmetic exponent as an infimum, both cases imply **omega_Q <= log_b(r)**.

This is a unit-cost exact arithmetic statement over Q. It does not provide bit complexity for growing rational inputs, floating-point stability, practical speed, or a theorem for unsupported fields. No logarithm is evaluated numerically by intake. The exact test for a bound strictly below 9/4 is

```text
log_b(r) < 9/4  if and only if  r^4 < b^9.
```

The receipt exposes both integers and the strict comparison only after verifying the identity and the square-model prerequisites. A positive comparison would be evidence for this particular arithmetic model under the proof above; record novelty and broader research claims still require independent review. The receipt always sets `new_exponent_record_certified` to `false`. A valid rectangular certificate or the 1-by-1 baseline has no square-recursion exponent assertion in this format.

## Known baselines and attribution

The scalar fixture is the elementary identity `C[0,0] = A[0,0] B[0,0]`, independently encoded by this project. It is a parser and identity baseline, with no exponent bound.

The 2-by-2 fixture is an independent encoding of the classical seven-product algorithm attributed to Volker Strassen, [*Gaussian elimination is not optimal*, Numerische Mathematik 13, 354–356 (1969)](https://doi.org/10.1007/BF02165411). The publisher's bibliographic record was checked on 2026-10-12; no claim is made that publisher full text was retrieved. The algebraic identity is independently checked by this repository. With `A=[[a,b],[c,d]]`, `B=[[e,f],[g,h]]`, the chosen equivalent presentation is:

```text
P1 = (a+d)(e+h)    P2 = (c+d)e       P3 = a(f-h)
P4 = d(g-e)        P5 = (a+b)h       P6 = (c-a)(e+f)
P7 = (b-d)(g+h)

C11 = P1 + P4 - P5 + P7     C12 = P3 + P5
C21 = P2 + P4               C22 = P1 - P2 + P3 + P6
```

Its derived bound is `omega_Q <= log_2(7)`. Here `7^4 = 2401` and `2^9 = 512`, so it does **not** meet the `omega < 9/4` objective. Both checked-in schemes remain under `certificates/baselines/`, separate from research candidates.

## Verification and CI trust boundary

The tests include an independent nested-matrix multiplication oracle on every basis pair, a nonsquare 2-by-3 times 3-by-4 layout, and exact rational inputs. All 36 nonzero Strassen coefficients are individually sign-corrupted and rehashed; every resulting identity must be rejected. A formerly zero cross-term is also corrupted. Further controls cover hash and metadata pins, unsupported exponent assertions, malformed fractions and dimensions, duplicate keys, traversal, symlinks, byte limits, and empty intake. A CLI integration control places executable traps in an untrusted checkout and its Python import path, then confirms the isolated trusted validator accepts the JSON without executing those traps.

The workflow uses `pull_request_target` deliberately: the workflow, validator, and tests come from the trusted base revision. A separate sparse checkout supplies untrusted certificate and submission JSON at the pinned PR head commit. No code, test, package installer, Git hook, or workflow from that checkout is invoked. There are no write permissions, secrets explicitly passed, comments, deployments, or remote compute jobs. GitHub Actions still needs its normal checkout infrastructure; validation itself performs no network requests. A PR changing the validator cannot validate itself with that changed validator in this intake job. Maintainers must review such changes before merging them.

Receipts include the exact validator SHA256, manifest SHA256, certificate SHA256, all pinned mathematical metadata, number of coefficients checked, and the optional derived bound. CI prints receipts to the job log. A locally generated receipt is not evidence that hosted CI ran, that a repository was published, or that any research threshold improved.
