#!/usr/bin/env python3
"""
CERT Event Normalizer (single-file)
- Ingests CERT-style CSV logs with inconsistent field counts
- Repairs malformed rows (extra delimiters) deterministically
- Outputs a canonical event stream (CSV or JSONL)

Canonical fields (minimum):
  ts, user, host, event_type, action, object_type, object_id,
  src, dst, attachments_count, attachments_bytes,
  source_file, rownum, parse_note, raw

Usage:
  python cert_normalizer.py in1.csv in2.csv -o out_events.jsonl --format jsonl
  python cert_normalizer.py *.csv -o out_events.csv --format csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Iterable


# -----------------------------
# Helpers: time parsing
# -----------------------------
_TS_PATTERNS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y/%m/%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M",
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M",
    "%d-%b-%Y %H:%M:%S",
]

def parse_ts(value: str) -> Optional[str]:
    """
    Parse a timestamp-ish string and return ISO-8601 string.
    Returns None if cannot parse.
    """
    if not value:
        return None
    v = value.strip()
    # common milliseconds trim
    v = re.sub(r"\.\d{3,6}$", "", v)
    # If already ISO-ish
    if re.match(r"^\d{4}-\d{2}-\d{2}T", v):
        return v
    for fmt in _TS_PATTERNS:
        try:
            dt = datetime.strptime(v, fmt)
            return dt.isoformat(sep=" ")
        except ValueError:
            continue
    return None

def coalesce(*vals: Optional[str]) -> Optional[str]:
    for v in vals:
        if v is not None and str(v).strip() != "":
            return str(v).strip()
    return None

def to_int(val: Optional[str]) -> Optional[int]:
    if val is None:
        return None
    s = str(val).strip()
    if s == "":
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


# -----------------------------
# Row repair strategy
# -----------------------------
def repair_row(fields: List[str], expected_len: int) -> Tuple[List[str], str]:
    """
    Deterministic repair for malformed CSV lines after splitting:
    - If too many fields: merge extras into the last column.
    - If too few: pad with empty strings.

    Returns (repaired_fields, note).
    """
    if expected_len <= 0:
        return fields, "no_expected_len"

    if len(fields) == expected_len:
        return fields, ""

    if len(fields) > expected_len:
        head = fields[: expected_len - 1]
        tail = fields[expected_len - 1 :]
        merged_last = ",".join(tail)
        return head + [merged_last], f"merged_extras:{len(fields)}->{expected_len}"

    # len(fields) < expected_len
    padded = fields + [""] * (expected_len - len(fields))
    return padded, f"padded_missing:{len(fields)}->{expected_len}"


# -----------------------------
# Canonical event
# -----------------------------
@dataclass
class CanonicalEvent:
    ts: Optional[str] = None
    user: Optional[str] = None
    host: Optional[str] = None
    event_type: Optional[str] = None   # e.g., file, email, web, logon
    action: Optional[str] = None       # e.g., file_open, email_send
    object_type: Optional[str] = None  # e.g., file, url, email
    object_id: Optional[str] = None    # path/url/message_id
    src: Optional[str] = None          # source address/system
    dst: Optional[str] = None          # destination address/system
    attachments_count: Optional[int] = None
    attachments_bytes: Optional[int] = None

    # provenance
    source_file: Optional[str] = None
    rownum: Optional[int] = None
    parse_note: Optional[str] = None
    raw: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "ts": self.ts,
            "user": self.user,
            "host": self.host,
            "event_type": self.event_type,
            "action": self.action,
            "object_type": self.object_type,
            "object_id": self.object_id,
            "src": self.src,
            "dst": self.dst,
            "attachments_count": self.attachments_count,
            "attachments_bytes": self.attachments_bytes,
            "source_file": self.source_file,
            "rownum": self.rownum,
            "parse_note": self.parse_note,
            "raw": self.raw,
        }


# -----------------------------
# Schema inference + mapping
# -----------------------------
def normalize_header(header: List[str]) -> List[str]:
    return [h.strip().lower().replace(" ", "_") for h in header]

def guess_event_type_and_action(row: Dict[str, str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Best-effort mapping from CERT-ish fields to event_type/action.
    Handles variations like activity/action/event.
    """
    a = coalesce(row.get("activity"), row.get("action"), row.get("event"), row.get("activitytype"))
    if not a:
        return None, None

    al = a.lower()

    # File
    if "file" in al or "open" in al or "read" in al or "write" in al or "copy" in al:
        # common canonical actions
        if "open" in al or "read" in al:
            return "file", "file_open"
        if "write" in al or "create" in al or "save" in al:
            return "file", "file_write"
        if "copy" in al:
            return "file", "file_copy"
        if "delete" in al or "remove" in al:
            return "file", "file_delete"
        return "file", "file_event"

    # Email
    if "email" in al or "mail" in al or "send" in al:
        if "send" in al:
            return "email", "email_send"
        if "receive" in al or "recv" in al:
            return "email", "email_receive"
        return "email", "email_event"

    # Web / HTTP
    if "http" in al or "web" in al or "url" in al or "browse" in al:
        return "web", "web_request"

    # Logon
    if "logon" in al or "login" in al or "auth" in al:
        return "auth", "logon"

    return None, a.strip()

def extract_object(row: Dict[str, str], event_type: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract object_type/object_id.
    """
    # common candidates
    filename = coalesce(row.get("filename"), row.get("file"), row.get("path"), row.get("object"))
    url = coalesce(row.get("url"), row.get("uri"))
    msgid = coalesce(row.get("message_id"), row.get("msgid"), row.get("mid"))

    if event_type == "file" and filename:
        return "file", filename
    if event_type == "web" and url:
        return "url", url
    if event_type == "email" and (msgid or filename):
        # attachment name often in filename
        return "email", msgid or filename

    # fallback
    if filename:
        return "file", filename
    if url:
        return "url", url
    if msgid:
        return "email", msgid
    return None, None

def extract_ts(row: Dict[str, str]) -> Optional[str]:
    # Many CERT logs have separate date + time columns
    dt = coalesce(row.get("datetime"), row.get("timestamp"), row.get("time"), row.get("ts"))
    if dt:
        parsed = parse_ts(dt)
        if parsed:
            return parsed

    d = coalesce(row.get("date"), row.get("day"))
    t = coalesce(row.get("hour"), row.get("time"))
    if d and t:
        parsed = parse_ts(f"{d} {t}")
        if parsed:
            return parsed

    return None

def extract_user_host(row: Dict[str, str]) -> Tuple[Optional[str], Optional[str]]:
    user = coalesce(row.get("user"), row.get("user_id"), row.get("username"), row.get("employee"), row.get("id"))
    host = coalesce(row.get("pc"), row.get("host"), row.get("machine"), row.get("computer"))
    return user, host

def extract_src_dst(row: Dict[str, str]) -> Tuple[Optional[str], Optional[str]]:
    src = coalesce(row.get("src"), row.get("source"), row.get("from"), row.get("sender"), row.get("ip"))
    dst = coalesce(row.get("dst"), row.get("dest"), row.get("to"), row.get("recipient"), row.get("receiver"))
    return src, dst

def extract_attachments(row: Dict[str, str]) -> Tuple[Optional[int], Optional[int]]:
    # Different datasets name these differently. We’ll try many.
    cnt = to_int(coalesce(row.get("attachment_count"), row.get("attachments"), row.get("attach_cnt"), row.get("n_attachments")))
    size = to_int(coalesce(row.get("attachment_size"), row.get("attach_size"), row.get("total_attach_size"),
                           row.get("bytes"), row.get("size"), row.get("attachments_bytes")))
    return cnt, size


# -----------------------------
# Robust CSV ingestion
# -----------------------------
def iter_rows_robust(path: Path, delimiter: str = ",") -> Iterable[Tuple[List[str], str, int]]:
    """
    Yield (fields, raw_line, rownum) for a file, using a low-level split.
    This avoids pandas choking on inconsistent row widths.
    """
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        for i, line in enumerate(f, start=1):
            raw = line.rstrip("\n")
            # naive split; we repair later relative to header length
            fields = [x.strip() for x in raw.split(delimiter)]
            yield fields, raw, i

def normalize_file(path: Path) -> Tuple[List[CanonicalEvent], Dict[str, int]]:
    """
    Normalize one CERT-ish CSV into canonical events.
    Returns (events, diagnostics_counts).
    """
    events: List[CanonicalEvent] = []
    diags = {
        "rows_total": 0,
        "rows_emitted": 0,
        "rows_skipped_empty": 0,
        "rows_repaired": 0,
        "rows_badheader": 0,
    }

    it = iter_rows_robust(path)
    try:
        header_fields, header_raw, header_rownum = next(it)
    except StopIteration:
        diags["rows_badheader"] += 1
        return events, diags

    # If header line is weird (no alpha fields), try to treat as data with default header
    if not any(re.search(r"[A-Za-z]", h) for h in header_fields):
        diags["rows_badheader"] += 1
        # Default: col1..colN
        header = [f"col{i}" for i in range(1, len(header_fields) + 1)]
        # Put header_fields back into stream by processing it as a row below
        rows = [(header_fields, header_raw, header_rownum)] + list(it)
    else:
        header = normalize_header(header_fields)
        rows = list(it)

    expected_len = len(header)

    for fields, raw, rownum in rows:
        diags["rows_total"] += 1
        if len(fields) == 1 and fields[0] == "":
            diags["rows_skipped_empty"] += 1
            continue

        repaired, note = repair_row(fields, expected_len)
        if note:
            diags["rows_repaired"] += 1

        row = {header[i]: (repaired[i] if i < len(repaired) else "") for i in range(expected_len)}

        ts = extract_ts(row)
        user, host = extract_user_host(row)
        event_type, action = guess_event_type_and_action(row)
        object_type, object_id = extract_object(row, event_type)
        src, dst = extract_src_dst(row)
        attach_cnt, attach_bytes = extract_attachments(row)

        ev = CanonicalEvent(
            ts=ts,
            user=user,
            host=host,
            event_type=event_type,
            action=action,
            object_type=object_type,
            object_id=object_id,
            src=src,
            dst=dst,
            attachments_count=attach_cnt,
            attachments_bytes=attach_bytes,
            source_file=path.name,
            rownum=rownum,
            parse_note=note or None,
            raw=raw,
        )
        events.append(ev)
        diags["rows_emitted"] += 1

    return events, diags


# -----------------------------
# Output writers
# -----------------------------
def write_jsonl(events: List[CanonicalEvent], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev.to_dict(), ensure_ascii=False) + "\n")

def write_csv(events: List[CanonicalEvent], out_path: Path) -> None:
    fieldnames = list(CanonicalEvent().to_dict().keys())
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for ev in events:
            w.writerow(ev.to_dict())


# -----------------------------
# Main
# -----------------------------
def main():
    ap = argparse.ArgumentParser(description="CERT Event Normalizer -> canonical event stream")
    ap.add_argument("inputs", nargs="+", help="Input CERT CSV logs")
    ap.add_argument("-o", "--output", required=True, help="Output file path")
    ap.add_argument("--format", choices=["jsonl", "csv"], default="jsonl", help="Output format")
    ap.add_argument("--diag", default=None, help="Optional diagnostics JSON path")
    args = ap.parse_args()

    all_events: List[CanonicalEvent] = []
    all_diags: Dict[str, Dict[str, int]] = {}

    for inp in args.inputs:
        p = Path(inp)
        if not p.exists():
            continue
        events, diags = normalize_file(p)
        all_events.extend(events)
        all_diags[p.name] = diags

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "jsonl":
        write_jsonl(all_events, out_path)
    else:
        write_csv(all_events, out_path)

    if args.diag:
        dpath = Path(args.diag)
        dpath.parent.mkdir(parents=True, exist_ok=True)
        with dpath.open("w", encoding="utf-8") as f:
            json.dump(all_diags, f, indent=2)

    print(f"Wrote {len(all_events)} canonical events -> {out_path}")
    if args.diag:
        print(f"Wrote diagnostics -> {args.diag}")

if __name__ == "__main__":
    main()
