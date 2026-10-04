"""Stage a receipt for the three October 2 books. Not an apply.

Fresh sums are printed only when the pack file for that book is on disk.
A missing file is BLOCKED with computed=NONE. A present file whose sum
differs from the target is DRIFT. An equal sum is MATCH.

catalog.json figures are a citation check against the same targets. They are
not a fresh sum. This module does not arm a rule, invent a bar, or restart a bot.
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent

TARGETS = {
    "journal": Decimal("-2647.77"),
    "broker": Decimal("-2208.95"),
    "scorer": Decimal("-2041.95"),
}
JOURNAL_CYCLES = 41

PACK_CANDIDATES = (
    Path("/tmp/oct2_pack/oct2_pack"),
    Path("/workspace/oct2_pack"),
    Path("/workspace/oct2_pack/oct2_pack"),
    Path("/workspace/packs/oct2"),
)

BOOK_FILES = {
    "journal": (
        "journal_closed/batch_c_4162.jsonl",
        "packs/oct2/journal_closed/batch_c_4162.jsonl",
    ),
    "broker": (
        "broker_day/day_pnl_20261002.jsonl",
        "packs/oct2/broker_day/day_pnl_20261002.jsonl",
    ),
    "scorer": (
        "journals/inv_price_v3_2026-10-02_2026-10-02.json",
        "packs/oct2/journals/inv_price_v3_2026-10-02_2026-10-02.json",
    ),
}

CATALOG_KEYS = {
    "journal": "journal_synthetic",
    "broker": "broker_day",
    "scorer": "scorer_actual",
}


class BookSchemaError(Exception):
    pass


def money(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'))}"


def _as_decimal(value) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool) or value is None:
        raise BookSchemaError("pnl is missing")
    return Decimal(str(value))


def _read_jsonl_sum(path: Path) -> tuple[Decimal, int]:
    total = Decimal("0")
    n = 0
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw, parse_float=Decimal)
        except json.JSONDecodeError as exc:
            raise BookSchemaError(f"{path.name}:{line_no}: {exc}") from exc
        if not isinstance(row, dict) or "pnl" not in row:
            raise BookSchemaError(f"{path.name}:{line_no}: pnl required")
        total += _as_decimal(row["pnl"])
        n += 1
    if n == 0:
        raise BookSchemaError(f"{path.name}: no rows")
    return total, n


def _read_scorer_actual(path: Path) -> Decimal:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"), parse_float=Decimal)
    except json.JSONDecodeError as exc:
        raise BookSchemaError(f"{path.name}: {exc}") from exc
    try:
        return _as_decimal(payload["total"]["ACTUAL"])
    except (KeyError, TypeError, BookSchemaError) as exc:
        raise BookSchemaError(f"{path.name}: total.ACTUAL missing") from exc


def _find(roots: list[Path], rels: tuple[str, ...]) -> Path | None:
    for root in roots:
        if not root.is_dir():
            continue
        for rel in rels:
            path = root / rel
            if path.is_file():
                return path
    return None


def _judge(computed: Decimal | None, target: Decimal, *, present: bool) -> str:
    if not present or computed is None:
        return "BLOCKED"
    if money(computed) == money(target):
        return "MATCH"
    return "DRIFT"


def _roots(pack: Path | None) -> list[Path]:
    roots: list[Path] = []
    if pack is not None:
        roots.append(pack)
    for candidate in PACK_CANDIDATES:
        if candidate not in roots:
            roots.append(candidate)
    return roots


def catalog_citations(catalog_path: Path) -> dict:
    """Compare catalog.json reference figures to the targets. Not a recompute."""
    out = {}
    if not catalog_path.is_file():
        for book, target in TARGETS.items():
            out[book] = {
                "catalog_citation": "BLOCKED",
                "catalog_cited": None,
                "target": money(target),
                "missing": str(catalog_path),
            }
        return out
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    ref = payload.get("reference") or {}
    for book, target in TARGETS.items():
        key = CATALOG_KEYS[book]
        if key not in ref:
            out[book] = {
                "catalog_citation": "BLOCKED",
                "catalog_cited": None,
                "target": money(target),
                "missing": f"reference.{key}",
            }
            continue
        cited = _as_decimal(ref[key])
        out[book] = {
            "catalog_citation": _judge(cited, target, present=True),
            "catalog_cited": money(cited),
            "target": money(target),
        }
    cycles = ref.get("journal_cycles")
    out["journal"]["catalog_cycles"] = cycles
    out["journal"]["catalog_cycles_status"] = (
        "MATCH" if cycles == JOURNAL_CYCLES else "DRIFT" if cycles is not None else "BLOCKED"
    )
    return out


def fresh_books(pack: Path | None = None) -> dict:
    """Sum pack files when they exist. Missing files stay computed=NONE."""
    roots = _roots(pack)
    checked = [{"root": str(root), "exists": root.is_dir()} for root in roots]
    books = {}
    for book, target in TARGETS.items():
        path = _find(roots, BOOK_FILES[book])
        row = {
            "book": book,
            "target": money(target),
            "fresh_computed": None,
            "fresh_status": "BLOCKED",
            "path": str(path) if path else None,
            "missing": list(BOOK_FILES[book]) if path is None else [],
        }
        if path is None:
            books[book] = row
            continue
        try:
            if book == "scorer":
                computed = _read_scorer_actual(path)
                cycles = None
            else:
                computed, cycles = _read_jsonl_sum(path)
        except BookSchemaError as exc:
            row["fresh_status"] = "BLOCKED"
            row["fresh_computed"] = None
            row["detail"] = str(exc)
            books[book] = row
            continue
        row["fresh_computed"] = money(computed)
        row["fresh_status"] = _judge(computed, target, present=True)
        if book == "journal":
            row["cycles"] = cycles
            row["cycles_target"] = JOURNAL_CYCLES
            row["cycles_status"] = "MATCH" if cycles == JOURNAL_CYCLES else "DRIFT"
            if row["cycles_status"] == "DRIFT" and row["fresh_status"] == "MATCH":
                row["fresh_status"] = "DRIFT"
                row["detail"] = f"dollars match and cycles {cycles} != {JOURNAL_CYCLES}"
        books[book] = row
    statuses = [books[name]["fresh_status"] for name in TARGETS]
    if "DRIFT" in statuses:
        overall = "DRIFT"
    elif "BLOCKED" in statuses:
        overall = "BLOCKED"
    else:
        overall = "MATCH"
    return {"checked_roots": checked, "books": books, "fresh_result": overall}


def evaluate(pack: Path | None = None, catalog_path: Path | None = None, *, apply_live: bool = False) -> dict:
    if apply_live:
        raise RuntimeError("NOT_APPLIED: live apply is refused")
    catalog_path = catalog_path or (HERE / "catalog.json")
    fresh = fresh_books(pack)
    cited = catalog_citations(catalog_path)
    return {
        "apply": "NOT_APPLIED",
        "armed": False,
        "fleet_restarted": False,
        "ratchet_armed": False,
        "fresh_result": fresh["fresh_result"],
        "books": {
            name: {**fresh["books"][name], **cited[name]}
            for name in TARGETS
        },
        "checked_roots": fresh["checked_roots"],
        "note": (
            "fresh_status is this run's sum. "
            "catalog_citation compares catalog.json reference to the targets and is not a recompute. "
            "APPLY is NOT_APPLIED."
        ),
    }


def render(result: dict) -> str:
    lines = [
        "# October 2 three-book receipt",
        "",
        "APPLY: NOT_APPLIED",
        "ARMED: false",
        f"Fresh result: {result['fresh_result']}",
        "",
        "A fresh figure is printed only when that book's file is on disk. catalog_cited is the number already stored in catalog.json.",
        "",
        "| Book | Target | Fresh | Fresh computed | Catalog cited | Catalog citation |",
        "|---|---:|---|---:|---:|---|",
    ]
    for name in TARGETS:
        row = result["books"][name]
        computed = row["fresh_computed"] if row["fresh_computed"] is not None else "NONE"
        lines.append(
            f"| {name} | {row['target']} | {row['fresh_status']} | {computed} | {row['catalog_cited']} | {row['catalog_citation']} |"
        )
    lines.append("")
    for name in TARGETS:
        row = result["books"][name]
        if row["fresh_status"] == "BLOCKED" and row.get("missing"):
            lines.append(f"- {name} missing: {', '.join(row['missing'])}")
        if row.get("detail"):
            lines.append(f"- {name} detail: {row['detail']}")
    lines.append("")
    lines.append("This receipt does not apply a gate, arm Ultra Ratchet, or restart a bot.")
    lines.append("")
    return "\n".join(lines)


def write_outputs(result: dict, dest: Path | None = None) -> Path:
    dest = dest or HERE
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "BOOK_RECEIPT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    path = dest / "BOOK_RECEIPT.md"
    path.write_text(render(result), encoding="utf-8")
    return path


def main() -> int:
    pack = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    result = evaluate(pack)
    path = write_outputs(result)
    print(
        json.dumps(
            {
                "fresh_result": result["fresh_result"],
                "apply": result["apply"],
                "wrote": str(path),
                "books": {
                    name: {
                        "fresh_status": result["books"][name]["fresh_status"],
                        "fresh_computed": result["books"][name]["fresh_computed"],
                        "catalog_citation": result["books"][name]["catalog_citation"],
                        "catalog_cited": result["books"][name]["catalog_cited"],
                        "target": result["books"][name]["target"],
                    }
                    for name in TARGETS
                },
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
