#!/usr/bin/env python3
"""Bounded exact bilinear identity intake. Python standard library only."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

CERT_FORMAT = "matrix-mult-bilinear-v1"
MANIFEST_FORMAT = "matrix-mult-intake-v1"
MAX_BYTES = 1_048_576
MAX_DIMENSION = 4
MAX_RANK = 64
RATIONAL = re.compile(r"(?:0|-?[1-9][0-9]{0,8})(?:/[1-9][0-9]{0,8})?\Z")


class InvalidCertificate(ValueError):
    """Invalid data, unsupported assertion, or resource limit exceeded."""


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def exact_keys(value, keys, label):
    require(type(value) is dict and set(value) == set(keys),
            f"{label}: expected exactly {', '.join(sorted(keys))}")


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise InvalidCertificate(f"non-JSON numeric constant: {value}")


def load_json(raw):
    require(len(raw) <= MAX_BYTES, "JSON exceeds 1 MiB limit")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicate_keys,
                          parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        raise InvalidCertificate(f"invalid JSON: {exc}") from exc


def safe_file(root, relative, prefix):
    require(type(relative) is str and len(relative) <= 240, "invalid relative path")
    parts = relative.split("/")
    require(len(parts) == (3 if prefix == "certificates" else 2) and parts[0] == prefix
            and all(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", p) for p in parts)
            and relative.endswith(".json"),
            f"path must be a safe relative JSON path under {prefix}/")
    require(not PurePosixPath(relative).is_absolute(), "absolute paths forbidden")
    current = Path(root)
    for part in parts:
        current = current / part
        require(not current.is_symlink(), "symlink paths forbidden")
    require(current.is_file(), f"missing regular file: {relative}")
    require(current.stat().st_size <= MAX_BYTES, "JSON exceeds 1 MiB limit")
    return current


def dimensions(value):
    exact_keys(value, {"m", "k", "n"}, "dimensions")
    for x in value.values():
        require(type(x) is int and 1 <= x <= MAX_DIMENSION,
                "dimensions must be integers from 1 through 4")
    return value["m"], value["k"], value["n"]


def rank(value):
    require(type(value) is int and 1 <= value <= MAX_RANK,
            "declared_rank must be an integer from 1 through 64")
    return value


def vector(value, size, label):
    require(type(value) is list and len(value) == size,
            f"{label}: wrong vector length; expected {size}")
    result = []
    for coefficient in value:
        require(type(coefficient) is str and RATIONAL.fullmatch(coefficient),
                f"{label}: coefficients must be bounded canonical rational strings")
        rational = Fraction(coefficient)
        require(str(rational) == coefficient, f"{label}: noncanonical rational")
        result.append(rational)
    require(any(result), f"{label}: zero factor does not count as a product")
    return result


def verify_identity(certificate):
    exact_keys(certificate, {"format", "domain", "dimensions", "declared_rank", "terms"},
               "certificate")
    require(certificate["format"] == CERT_FORMAT, "unsupported certificate format")
    require(certificate["domain"] == "Q", "only exact rational domain Q is supported")
    m, k, n = dimensions(certificate["dimensions"])
    r = rank(certificate["declared_rank"])
    terms = certificate["terms"]
    require(type(terms) is list and len(terms) == r,
            "declared_rank must equal the number of product terms")
    # Full tensor, including all coefficients that are required to be zero.
    tensor = [[[Fraction(0) for _ in range(k * n)]
               for _ in range(m * k)] for _ in range(m * n)]
    for index, term in enumerate(terms):
        exact_keys(term, {"a", "b", "c"}, f"term {index}")
        a = vector(term["a"], m * k, f"term {index} a")
        b = vector(term["b"], k * n, f"term {index} b")
        c = vector(term["c"], m * n, f"term {index} c")
        for out, cv in enumerate(c):
            for left, av in enumerate(a):
                for right, bv in enumerate(b):
                    tensor[out][left][right] += cv * av * bv
    for out in range(m * n):
        i, j = divmod(out, n)
        for left in range(m * k):
            ai, ak = divmod(left, k)
            for right in range(k * n):
                bk, bj = divmod(right, n)
                expected = int(ai == i and bj == j and ak == bk)
                actual = tensor[out][left][right]
                require(actual == expected,
                        f"coefficient mismatch C[{i},{j}] A[{ai},{ak}] B[{bk},{bj}]: "
                        f"got {actual}, expected {expected}")
    return {"identity": "verified_exact", "coefficients_checked": m * n * m * k * k * n,
            "rank_statement": f"tensor_rank_over_Q <= {r}",
            "minimal_rank_proven": False}


def recursion_bound(dims, r):
    m, k, n = dimensions(dims)
    require(m == k == n and n >= 2,
            "square_recursion_bound requires square dimensions >= 2")
    # The flattening rank is n^2; this also catches misuse of this helper.
    require(r >= n * n, "square recursion requires rank >= n^2")
    return {
        "statement": f"omega_Q <= log_{n}({r})",
        "model": "unit-cost exact arithmetic over Q; fixed-size block recursion",
        "proof_reference": "docs/CERTIFICATE_CONTRACT.md#square-recursion-proof",
        "exact_below_9_over_4_test": {"left_r_to_4": r ** 4, "right_n_to_9": n ** 9,
                                      "strictly_less": r ** 4 < n ** 9},
        "record_novelty": "not_evaluated",
    }


def validate_manifest(manifest):
    exact_keys(manifest, {"format", "certificate", "sha256", "domain", "dimensions",
                          "declared_rank", "classification", "attribution", "claim"},
               "manifest")
    require(manifest["format"] == MANIFEST_FORMAT, "unsupported manifest format")
    require(type(manifest["sha256"]) is str
            and re.fullmatch(r"[0-9a-f]{64}", manifest["sha256"]), "invalid SHA256 pin")
    require(manifest["domain"] == "Q", "only domain Q is supported")
    dimensions(manifest["dimensions"])
    rank(manifest["declared_rank"])
    require(manifest["classification"] in ("known_baseline", "candidate"),
            "unsupported classification")
    require(manifest["claim"] in ("exact_identity", "square_recursion_bound"),
            "unsupported claim; exponent records and thresholds cannot be asserted")
    attr = manifest["attribution"]
    exact_keys(attr, {"authors", "title", "year", "url"}, "attribution")
    require(type(attr["authors"]) is list and 1 <= len(attr["authors"]) <= 20,
            "attribution requires 1 through 20 authors")
    for value in attr["authors"] + [attr["title"], attr["url"]]:
        require(type(value) is str and 1 <= len(value) <= 500
                and all(ord(c) >= 32 for c in value), "invalid attribution string")
    require(type(attr["year"]) is int and 1 <= attr["year"] <= 9999,
            "invalid attribution year")
    require(attr["url"].startswith("https://"), "attribution URL must use https")


def verify_submission(root, manifest_path):
    manifest_raw = safe_file(root, manifest_path, "submissions").read_bytes()
    manifest = load_json(manifest_raw)
    validate_manifest(manifest)
    cert_path = manifest["certificate"]
    path = safe_file(root, cert_path, "certificates")
    expected_dir = "baselines" if manifest["classification"] == "known_baseline" else "candidates"
    require(cert_path.split("/")[1] == expected_dir,
            f"classification requires certificates/{expected_dir}/")
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == manifest["sha256"], "certificate SHA256 mismatch")
    certificate = load_json(raw)
    require(type(certificate) is dict, "certificate must be an object")
    for field in ("domain", "dimensions", "declared_rank"):
        require(certificate.get(field) == manifest[field], f"manifest {field} pin mismatch")
    identity = verify_identity(certificate)
    bound = (recursion_bound(manifest["dimensions"], manifest["declared_rank"])
             if manifest["claim"] == "square_recursion_bound" else None)
    return {
        "receipt_format": "matrix-mult-receipt-v1", "status": "accepted_exact_identity",
        "manifest": manifest_path, "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "certificate": cert_path, "certificate_sha256": digest,
        "validator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "domain": manifest["domain"], "dimensions": manifest["dimensions"],
        "declared_rank": manifest["declared_rank"],
        "classification_declared": manifest["classification"],
        "attribution": manifest["attribution"], "attribution_verified_by_validator": False,
        **identity, "square_recursion_bound": bound,
        "new_exponent_record_certified": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="data repository root (defaults to this repository)")
    parser.add_argument("--manifest", action="append", help="relative submission JSON; repeatable")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    manifests = args.manifest
    if manifests is None:
        manifests = sorted(p.relative_to(root).as_posix() for p in (root / "submissions").glob("*.json"))
    try:
        require(bool(manifests), "no submission manifests found")
        require(len(manifests) <= 128, "at most 128 manifests per intake")
        receipts = [verify_submission(root, name) for name in manifests]
    except (InvalidCertificate, OSError) as exc:
        print(json.dumps({"status": "rejected", "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps({"status": "accepted", "receipts": receipts}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
