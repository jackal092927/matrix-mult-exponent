"""Independent basis-matrix oracle and corrupted certificate controls."""

import copy
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verifier", ROOT / "scripts/verify_certificate.py")
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


def textbook_product(a, b):
    """Ordinary nested matrix multiplication; independent of tensor indexing."""
    return [[sum(x * y for x, y in zip(row, column)) for column in zip(*b)] for row in a]


def evaluate_terms(certificate, a, b):
    av = list(itertools.chain.from_iterable(a))
    bv = list(itertools.chain.from_iterable(b))
    outputs = [Fraction(0)] * (certificate["dimensions"]["m"] * certificate["dimensions"]["n"])
    for term in certificate["terms"]:
        product = (sum(Fraction(x) * y for x, y in zip(term["a"], av))
                   * sum(Fraction(x) * y for x, y in zip(term["b"], bv)))
        outputs = [old + product * Fraction(weight) for old, weight in zip(outputs, term["c"])]
    n = certificate["dimensions"]["n"]
    return [outputs[start:start + n] for start in range(0, len(outputs), n)]


def schoolbook_certificate(m, k, n):
    terms = []
    for i, h, j in itertools.product(range(m), range(k), range(n)):
        a, b, c = ["0"] * (m * k), ["0"] * (k * n), ["0"] * (m * n)
        a[i * k + h], b[h * n + j], c[i * n + j] = "1", "1", "1"
        terms.append({"a": a, "b": b, "c": c})
    return {"format": V.CERT_FORMAT, "domain": "Q", "dimensions": {"m": m, "k": k, "n": n},
            "declared_rank": m * k * n, "terms": terms}


class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.strassen = json.loads((ROOT / "certificates/baselines/strassen-2x2-rank7.json").read_text())
        cls.manifest = json.loads((ROOT / "submissions/strassen-2x2-rank7.json").read_text())

    def check_basis_oracle(self, certificate):
        m, k, n = (certificate["dimensions"][name] for name in ("m", "k", "n"))
        # Exhausting basis pairs checks every bilinear coefficient, including cross terms.
        for ai, ah, bh, bj in itertools.product(range(m), range(k), range(k), range(n)):
            a, b = [[0] * k for _ in range(m)], [[0] * n for _ in range(k)]
            a[ai][ah], b[bh][bj] = 1, 1
            self.assertEqual(evaluate_terms(certificate, a, b), textbook_product(a, b))

    def submit(self, certificate=None, manifest=None, raw=None):
        certificate = self.strassen if certificate is None else certificate
        manifest = copy.deepcopy(self.manifest if manifest is None else manifest)
        raw = json.dumps(certificate).encode() if raw is None else raw
        manifest["sha256"] = hashlib.sha256(raw).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "certificates/baselines").mkdir(parents=True)
            (root / "submissions").mkdir()
            (root / "certificates/baselines/strassen-2x2-rank7.json").write_bytes(raw)
            (root / "submissions/test.json").write_text(json.dumps(manifest))
            return V.verify_submission(root, "submissions/test.json")

    def test_known_baselines_and_basis_oracle(self):
        for name in ("naive-1x1-rank1", "strassen-2x2-rank7"):
            with self.subTest(name=name):
                receipt = V.verify_submission(ROOT, f"submissions/{name}.json")
                self.assertEqual(receipt["status"], "accepted_exact_identity")
                self.assertFalse(receipt["new_exponent_record_certified"])
                certificate = json.loads((ROOT / receipt["certificate"]).read_text())
                self.check_basis_oracle(certificate)

    def test_rectangular_layout_and_rational_rescaling(self):
        certificate = schoolbook_certificate(2, 3, 4)
        certificate["terms"][5]["a"] = [str(Fraction(x) / 3) for x in certificate["terms"][5]["a"]]
        certificate["terms"][5]["b"] = [str(Fraction(x) * 3) for x in certificate["terms"][5]["b"]]
        self.assertEqual(V.verify_identity(certificate)["coefficients_checked"], 576)
        self.check_basis_oracle(certificate)

    def test_dense_rational_matrix_product(self):
        a = [[Fraction(1, 3), Fraction(-7, 5)], [Fraction(11, 2), Fraction(0)]]
        b = [[Fraction(2), Fraction(-3, 7)], [Fraction(-5, 3), Fraction(13, 11)]]
        self.assertEqual(evaluate_terms(self.strassen, a, b), textbook_product(a, b))

    def test_each_nonzero_strassen_coefficient_corruption_fails_after_repin(self):
        checked = 0
        for term_index, term in enumerate(self.strassen["terms"]):
            for factor in ("a", "b", "c"):
                for index, coefficient in enumerate(term[factor]):
                    if coefficient == "0":
                        continue
                    corrupt = copy.deepcopy(self.strassen)
                    corrupt["terms"][term_index][factor][index] = str(-Fraction(coefficient))
                    with self.subTest(term=term_index, factor=factor, index=index):
                        with self.assertRaisesRegex(V.InvalidCertificate, "coefficient mismatch"):
                            self.submit(certificate=corrupt)
                    checked += 1
        self.assertEqual(checked, 36)

    def test_zero_cross_term_corruption_fails(self):
        corrupt = copy.deepcopy(self.strassen)
        corrupt["terms"][0]["a"][1] = "1"
        with self.assertRaisesRegex(V.InvalidCertificate, "coefficient mismatch"):
            self.submit(certificate=corrupt)

    def test_all_metadata_pins(self):
        for field, value in (("dimensions", {"m": 2, "k": 2, "n": 3}),
                             ("declared_rank", 8)):
            manifest = copy.deepcopy(self.manifest)
            manifest[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(V.InvalidCertificate, "pin mismatch"):
                self.submit(manifest=manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["domain"] = "F2"
        with self.assertRaisesRegex(V.InvalidCertificate, "domain Q"):
            self.submit(manifest=manifest)

    def test_hash_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "certificates/baselines").mkdir(parents=True)
            (root / "submissions").mkdir()
            (root / "certificates/baselines/strassen-2x2-rank7.json").write_text("{}")
            (root / "submissions/test.json").write_text(json.dumps(self.manifest))
            with self.assertRaisesRegex(V.InvalidCertificate, "SHA256 mismatch"):
                V.verify_submission(root, "submissions/test.json")

    def test_unsupported_exponent_claims(self):
        for value in ("omega < 9/4", "omega = 2.2", "border_rank", "approximate_identity"):
            manifest = copy.deepcopy(self.manifest)
            manifest["claim"] = value
            with self.subTest(claim=value), self.assertRaisesRegex(V.InvalidCertificate, "unsupported claim"):
                self.submit(manifest=manifest)
        manifest = copy.deepcopy(self.manifest)
        manifest["omega_upper_bound"] = "2.2"
        with self.assertRaisesRegex(V.InvalidCertificate, "expected exactly"):
            self.submit(manifest=manifest)

    def test_strict_shapes_and_rationals(self):
        for coefficient in (0, True, "0.5", "2/4", "1/1", "-0", "00", "1/0", "1/-2", "1000000000", "1e-3"):
            corrupt = copy.deepcopy(self.strassen)
            corrupt["terms"][0]["a"][0] = coefficient
            with self.subTest(coefficient=coefficient), self.assertRaises(V.InvalidCertificate):
                self.submit(certificate=corrupt)
        for change in (lambda c: c["terms"][0]["a"].pop(),
                       lambda c: c["terms"].pop(),
                       lambda c: c["terms"][0].update(code="run me"),
                       lambda c: c["terms"][0].update(c=["0"] * 4),
                       lambda c: c["dimensions"].update(m=True),
                       lambda c: c["dimensions"].update(m=5),
                       lambda c: c.update(declared_rank=65),
                       lambda c: c.update(domain="R")):
            corrupt = copy.deepcopy(self.strassen)
            change(corrupt)
            with self.assertRaises(V.InvalidCertificate):
                self.submit(certificate=corrupt)

    def test_duplicate_keys_and_non_json_constants(self):
        for raw in (b'{"a":1,"a":2}', b'{"terms":[{"a":1,"a":2}]}',
                    b'{"value":NaN}', b'{"value":Infinity}', b'\xff'):
            with self.subTest(raw=raw), self.assertRaises(V.InvalidCertificate):
                V.load_json(raw)

    def test_path_traversal_and_symlinks(self):
        for path in ("../outside.json", "/tmp/outside.json", "certificates/../outside.json",
                     "certificates//outside.json", "certificates/./outside.json",
                     "certificates\\outside.json", "certificates/%2e%2e/outside.json"):
            manifest = copy.deepcopy(self.manifest)
            manifest["certificate"] = path
            with self.subTest(path=path), self.assertRaises(V.InvalidCertificate):
                self.submit(manifest=manifest)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "certificates/baselines").mkdir(parents=True)
            (root / "outside.json").write_text("{}")
            (root / "certificates/baselines/link.json").symlink_to(root / "outside.json")
            with self.assertRaisesRegex(V.InvalidCertificate, "symlink"):
                V.safe_file(root, "certificates/baselines/link.json", "certificates")

    def test_recursion_threshold_is_exact_and_small_cases_rejected(self):
        bound = self.submit()["square_recursion_bound"]
        self.assertEqual(bound["statement"], "omega_Q <= log_2(7)")
        self.assertEqual(bound["exact_below_9_over_4_test"],
                         {"left_r_to_4": 2401, "right_n_to_9": 512, "strictly_less": False})
        for dims in ({"m": 1, "k": 1, "n": 1}, {"m": 2, "k": 3, "n": 2}):
            with self.assertRaisesRegex(V.InvalidCertificate, "square dimensions"):
                V.recursion_bound(dims, 7)

    def test_oversized_data_and_empty_intake(self):
        with self.assertRaisesRegex(V.InvalidCertificate, "1 MiB"):
            V.load_json(b" " * (V.MAX_BYTES + 1))
        with tempfile.TemporaryDirectory() as directory:
            process = subprocess.run([sys.executable, str(ROOT / "scripts/verify_certificate.py"),
                                      "--root", directory], capture_output=True, text=True)
            self.assertEqual(process.returncode, 1)
            self.assertEqual(json.loads(process.stdout)["status"], "rejected")

    def test_cli_treats_contributor_checkout_only_as_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "certificates/baselines").mkdir(parents=True)
            (root / "submissions").mkdir()
            (root / "scripts").mkdir()
            for source in (ROOT / "submissions/strassen-2x2-rank7.json",
                           ROOT / "certificates/baselines/strassen-2x2-rank7.json"):
                (root / source.relative_to(ROOT)).write_bytes(source.read_bytes())
            marker = root / "CONTRIBUTOR_CODE_RAN"
            code = f"from pathlib import Path\nPath({str(marker)!r}).touch()\nraise RuntimeError('untrusted')\n"
            for name in ("fractions.py", "sitecustomize.py", "scripts/verify_certificate.py"):
                (root / name).write_text(code)
            env = dict(os.environ, PYTHONPATH=str(root))
            process = subprocess.run([sys.executable, "-I", "-B",
                                      str(ROOT / "scripts/verify_certificate.py"), "--root", str(root)],
                                     cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr + process.stdout)
            self.assertEqual(json.loads(process.stdout)["status"], "accepted")
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
