#!/usr/bin/env python3
"""Read-only Oct 2 three-book gate.

Missing inputs print BLOCKED and computed=NONE. No totals are invented.
A computed total is printed only after that book's files are present.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_BLOCKED = 2

ARMS = ("V1", "V2", "V3")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def manifest_path() -> Path:
    return Path(__file__).resolve().parent / "oct2_three_book_manifest.json"


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    arms = data["journal_closed"]["expect"]["arms"]
    combined = Decimal(data["journal_closed"]["expect"]["combined"])
    arm_sum = sum((Decimal(arms[name]["pnl"]) for name in ARMS), Decimal("0"))
    if arm_sum != combined:
        raise SystemExit(f"manifest arm sum {arm_sum} != combined {combined}")
    n_sum = sum(int(arms[name]["n"]) for name in ARMS)
    if n_sum != 41:
        raise SystemExit(f"manifest arm count {n_sum} != 41")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def money(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'))}"


def check_blob(root: Path, spec: dict) -> str | None:
    path = root / spec["path"]
    if not path.is_file():
        return spec["path"]
    size = path.stat().st_size
    digest = sha256_file(path)
    if size != spec["bytes"] or digest != spec["sha256"]:
        raise BlobMismatch(spec["path"], size, digest, spec["bytes"], spec["sha256"])
    return None


class BlobMismatch(Exception):
    def __init__(self, rel: str, size: int, digest: str, expect_size: int, expect_digest: str):
        self.rel = rel
        self.size = size
        self.digest = digest
        self.expect_size = expect_size
        self.expect_digest = expect_digest
        super().__init__(rel)


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw, parse_float=Decimal)
        except json.JSONDecodeError as exc:
            raise SchemaError(f"{path.name}:{line_no}: {exc}") from exc
        if not isinstance(row, dict):
            raise SchemaError(f"{path.name}:{line_no}: object required")
        rows.append(row)
    if not rows:
        raise SchemaError(f"{path.name}: no rows")
    return rows


class SchemaError(Exception):
    pass


def sum_journal(rows: list[dict], exclude: set[str]) -> dict:
    buckets = {arm: {"n": 0, "pnl": Decimal("0")} for arm in ARMS}
    for index, row in enumerate(rows, 1):
        if "arm" not in row or "symbol" not in row or "pnl" not in row:
            raise SchemaError(f"journal row {index} needs arm, symbol, pnl")
        if set(row) <= {"total"} or "total" in row and "pnl" not in row:
            raise SchemaError("prebaked total is not a closed trade")
        arm = row["arm"]
        if arm not in buckets:
            raise SchemaError(f"journal row {index} arm {arm!r}")
        symbol = str(row["symbol"]).upper()
        if not symbol:
            raise SchemaError(f"journal row {index} empty symbol")
        pnl = row["pnl"]
        if not isinstance(pnl, Decimal):
            raise SchemaError(f"journal row {index} pnl must be a number")
        if symbol in exclude:
            continue
        buckets[arm]["n"] += 1
        buckets[arm]["pnl"] += pnl
    combined_n = sum(buckets[arm]["n"] for arm in ARMS)
    combined = sum((buckets[arm]["pnl"] for arm in ARMS), Decimal("0"))
    return {"arms": buckets, "n": combined_n, "pnl": combined}


def sum_broker(rows: list[dict]) -> Decimal:
    total = Decimal("0")
    for index, row in enumerate(rows, 1):
        if "symbol" not in row or "pnl" not in row:
            raise SchemaError(f"broker row {index} needs symbol, pnl")
        if not str(row["symbol"]).strip():
            raise SchemaError(f"broker row {index} empty symbol")
        pnl = row["pnl"]
        if not isinstance(pnl, Decimal):
            raise SchemaError(f"broker row {index} pnl must be a number")
        total += pnl
    return total


def parse_actual(stdout: str) -> Decimal:
    for line in stdout.splitlines():
        if line.startswith("TOTAL"):
            parts = line.split()
            if len(parts) < 3:
                break
            return Decimal(parts[2])
    raise SchemaError("scorer stdout has no TOTAL line")


def remap_scorer(source: str, base: Path, bars: Path, base_constant: str, bars_constant: str) -> str:
    old_base = "BASE=r'" + base_constant + "'"
    old_bars = "BARS=r'" + bars_constant + "'"
    if source.count(old_base) != 1 or source.count(old_bars) != 1:
        raise SchemaError("scorer BASE/BARS constants are not the known pair")
    new_base = "BASE=r'" + base.resolve().as_posix() + "'"
    new_bars = "BARS=r'" + bars.resolve().as_posix() + "'"
    return source.replace(old_base, new_base, 1).replace(old_bars, new_bars, 1)


def run_scorer(root: Path, manifest: dict) -> Decimal:
    book = manifest["scorer_actual"]
    scorer = root / book["scorer"]["path"]
    text = scorer.read_text(encoding="utf-8-sig")
    with tempfile.TemporaryDirectory(prefix="oct2-three-book-") as tmp:
        tmp_path = Path(tmp)
        journals = tmp_path / "journals"
        bars = tmp_path / "bars_sample"
        shutil.copytree(root / "packs/oct2/journals", journals)
        shutil.copytree(root / "packs/oct2/bars_sample", bars)
        rewritten = remap_scorer(
            text, journals, bars, book["base_constant"], book["bars_constant"]
        )
        script = tmp_path / "inv_price_v3.py"
        script.write_text(rewritten, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(script), *book["argv"]],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=180,
        )
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        detail = tail[-1] if tail else f"exit {proc.returncode}"
        raise SchemaError(f"scorer exit {proc.returncode}: {detail}")
    return parse_actual(proc.stdout)


def evaluate(root: Path, manifest: dict) -> list[dict]:
    results = []

    journal_spec = manifest["journal_closed"]
    journal_path = root / journal_spec["path"]
    if not journal_path.is_file():
        results.append({"book": "journal_closed", "status": "BLOCKED", "missing": [journal_spec["path"]]})
    else:
        try:
            exclude = {s.upper() for s in journal_spec["exclude_symbols"]}
            got = sum_journal(read_jsonl(journal_path), exclude)
            expect = journal_spec["expect"]
            ok = money(got["pnl"]) == expect["combined"] and got["n"] == 41
            arm_detail = []
            for arm in ARMS:
                arm_expect = expect["arms"][arm]
                arm_ok = (
                    got["arms"][arm]["n"] == arm_expect["n"]
                    and money(got["arms"][arm]["pnl"]) == arm_expect["pnl"]
                )
                ok = ok and arm_ok
                arm_detail.append(
                    f"{arm} n={got['arms'][arm]['n']} pnl={money(got['arms'][arm]['pnl'])}"
                )
            results.append(
                {
                    "book": "journal_closed",
                    "status": "PASS" if ok else "FAIL",
                    "computed": money(got["pnl"]),
                    "detail": " ".join(arm_detail),
                }
            )
        except SchemaError as exc:
            results.append({"book": "journal_closed", "status": "FAIL", "computed": "NONE", "detail": str(exc)})

    broker_spec = manifest["broker_day"]
    broker_path = root / broker_spec["path"]
    if not broker_path.is_file():
        results.append({"book": "broker_day", "status": "BLOCKED", "missing": [broker_spec["path"]]})
    else:
        try:
            got = sum_broker(read_jsonl(broker_path))
            ok = money(got) == broker_spec["expect"]
            results.append(
                {
                    "book": "broker_day",
                    "status": "PASS" if ok else "FAIL",
                    "computed": money(got),
                }
            )
        except SchemaError as exc:
            results.append({"book": "broker_day", "status": "FAIL", "computed": "NONE", "detail": str(exc)})

    scorer = manifest["scorer_actual"]
    blobs = [scorer["scorer"], *scorer["inputs"]]
    missing = []
    mismatch = None
    try:
        for spec in blobs:
            rel = check_blob(root, spec)
            if rel:
                missing.append(rel)
    except BlobMismatch as exc:
        mismatch = exc
    if mismatch is not None:
        results.append(
            {
                "book": "scorer_actual",
                "status": "FAIL",
                "computed": "NONE",
                "detail": (
                    f"hash {mismatch.rel} size {mismatch.size} sha {mismatch.digest} "
                    f"expect size {mismatch.expect_size} sha {mismatch.expect_digest}"
                ),
            }
        )
    elif missing:
        results.append({"book": "scorer_actual", "status": "BLOCKED", "missing": missing})
    else:
        try:
            got = run_scorer(root, manifest)
            ok = money(got) == scorer["expect"]
            results.append(
                {
                    "book": "scorer_actual",
                    "status": "PASS" if ok else "FAIL",
                    "computed": money(got),
                }
            )
        except SchemaError as exc:
            results.append({"book": "scorer_actual", "status": "FAIL", "computed": "NONE", "detail": str(exc)})
        except subprocess.TimeoutExpired:
            results.append(
                {"book": "scorer_actual", "status": "FAIL", "computed": "NONE", "detail": "scorer timeout"}
            )
    return results


def format_report(results: list[dict]) -> str:
    lines = []
    missing = []
    for row in results:
        if row["status"] == "BLOCKED":
            missing.extend(row["missing"])
            lines.append(
                f"{row['book']} BLOCKED computed=NONE missing={','.join(row['missing'])}"
            )
        elif row["status"] == "PASS":
            lines.append(f"{row['book']} PASS computed={row['computed']}")
        else:
            extra = f" detail={row['detail']}" if row.get("detail") else ""
            lines.append(f"{row['book']} FAIL computed={row.get('computed', 'NONE')}{extra}")
    statuses = {row["status"] for row in results}
    if "FAIL" in statuses:
        overall = "FAIL"
    elif "BLOCKED" in statuses:
        overall = "BLOCKED"
    else:
        overall = "PASS"
    lines.append(f"RESULT {overall}")
    if missing:
        lines.append("MISSING")
        lines.extend(missing)
    return "\n".join(lines) + "\n"


def exit_code(results: list[dict]) -> int:
    statuses = {row["status"] for row in results}
    if "FAIL" in statuses:
        return EXIT_FAIL
    if "BLOCKED" in statuses:
        return EXIT_BLOCKED
    return EXIT_PASS


def main() -> int:
    root = repo_root()
    manifest = load_manifest(manifest_path())
    results = evaluate(root, manifest)
    sys.stdout.write(format_report(results))
    return exit_code(results)


if __name__ == "__main__":
    raise SystemExit(main())
