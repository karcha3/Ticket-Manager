"""SQLite-backed storage for tickets."""

import os
import sqlite3
import csv
from datetime import datetime

from resources import app_data_dir
import json
import uuid
import time

DB_FILENAME = os.path.join(app_data_dir(), "tickets.db")

EXPORT_COLUMNS = [
    ("first_name", "First Name"),
    ("last_name", "Last Name"),
    ("venue_type", "Venue Type"),
    ("ticket_type", "Ticket Type"),
    ("venue_name", "Venue / Event"),
    ("location", "Location"),
    ("date", "Date"),
    ("time", "Time"),
    ("seat", "Seat / Section"),
    ("price", "Price"),
    ("status", "Status"),
    ("notes", "Notes"),
]


VENUE_TYPES = ["Concert", "Theater", "Sports", "Conference", "Cinema",
               "Festival", "Exhibition", "Comedy Show", "Other"]
TICKET_TYPES = ["Standard", "VIP", "Early Bird", "Group", "Student",
                "Season Pass", "Backstage", "Other"]
STATUSES = ["Active", "Used", "Cancelled", "Refunded"]
IMPORT_MAX_BYTES = 5_000_000
SYNC_FIELDS = ["first_name", "last_name", "venue_type", "ticket_type", "venue_name",
               "location", "date", "time", "seat", "price", "status", "notes", "code"]
SYNC_MAX_BYTES = 20_000_000


def _now_ms() -> int:
    return int(time.time() * 1000)


def _pick(value, options, default):
    for o in options:
        if o.lower() == value.lower():
            return o
    return default


class Database:
    """Thin wrapper around a local SQLite ticket database."""

    def __init__(self, path=DB_FILENAME):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name  TEXT NOT NULL,
                last_name   TEXT NOT NULL,
                venue_type  TEXT,
                ticket_type TEXT,
                venue_name  TEXT,
                location    TEXT,
                date        TEXT,
                time        TEXT,
                seat        TEXT,
                price       REAL DEFAULT 0,
                status      TEXT,
                notes       TEXT,
                created_at  TEXT
            )
        """)
        self.conn.commit()
        self._migrate()

    def _migrate(self):
        """Add the hidden columns used for sync (and the Android scan code)."""
        cols = {r["name"] for r in self.conn.execute("PRAGMA table_info(tickets)")}
        for name, ddl in (("uid", "TEXT NOT NULL DEFAULT ''"),
                          ("updated_at", "INTEGER NOT NULL DEFAULT 0"),
                          ("deleted", "INTEGER NOT NULL DEFAULT 0"),
                          ("code", "TEXT NOT NULL DEFAULT ''")):
            if name not in cols:
                self.conn.execute(f"ALTER TABLE tickets ADD COLUMN {name} {ddl}")
        self.conn.execute("UPDATE tickets SET uid = lower(hex(randomblob(16))) WHERE uid = ''")
        self.conn.execute("UPDATE tickets SET updated_at = ? WHERE updated_at = 0", (_now_ms(),))
        self.conn.commit()

    def add_ticket(self, data: dict) -> int:
        cur = self.conn.execute("""
            INSERT INTO tickets
                (first_name, last_name, venue_type, ticket_type, venue_name,
                 location, date, time, seat, price, status, notes, created_at,
                 uid, updated_at, code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["first_name"], data["last_name"], data["venue_type"],
            data["ticket_type"], data["venue_name"], data["location"],
            data["date"], data["time"], data["seat"], data["price"],
            data["status"], data["notes"], datetime.now().isoformat(timespec="seconds"),
            uuid.uuid4().hex, _now_ms(), data.get("code", "")
        ))
        self.conn.commit()
        return cur.lastrowid

    def update_ticket(self, ticket_id: int, data: dict):
        self.conn.execute("""
            UPDATE tickets SET
                first_name=?, last_name=?, venue_type=?, ticket_type=?,
                venue_name=?, location=?, date=?, time=?, seat=?, price=?,
                status=?, notes=?, updated_at=?
            WHERE id=?
        """, (
            data["first_name"], data["last_name"], data["venue_type"],
            data["ticket_type"], data["venue_name"], data["location"],
            data["date"], data["time"], data["seat"], data["price"],
            data["status"], data["notes"], _now_ms(), ticket_id
        ))
        self.conn.commit()

    def delete_ticket(self, ticket_id: int):
        self.conn.execute("UPDATE tickets SET deleted=1, updated_at=? WHERE id=?",
                          (_now_ms(), ticket_id))
        self.conn.commit()

    def get_all_tickets(self):
        cur = self.conn.execute("SELECT * FROM tickets WHERE deleted = 0 ORDER BY date ASC, time ASC")
        return [dict(row) for row in cur.fetchall()]

    def get_distinct_venues(self):
        cur = self.conn.execute("""
            SELECT DISTINCT venue_name FROM tickets
            WHERE deleted = 0 AND venue_name IS NOT NULL AND TRIM(venue_name) != ''
            ORDER BY venue_name COLLATE NOCASE ASC
        """)
        return [row["venue_name"] for row in cur.fetchall()]

    def export_csv(self, path: str, tickets: list):
        """Export the given list of ticket dicts to a CSV file at `path`."""
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([label for key, label in EXPORT_COLUMNS])
            for t in tickets:
                writer.writerow([t.get(key, "") for key, label in EXPORT_COLUMNS])

    @staticmethod
    def _dup_key(t: dict):
        return (t["first_name"], t["last_name"], t["venue_name"], t["date"],
                t["time"], t["seat"], round(float(t["price"] or 0), 2), t["status"])

    def import_csv(self, path: str):
        """Import a CSV made by Export CSV (from this app or the Android app).
        Rows already in the database are skipped. Returns (added, skipped, invalid)."""
        if os.path.getsize(path) > IMPORT_MAX_BYTES:
            raise ValueError("The file is larger than 5 MB.")
        labels = {key: label.lower() for key, label in EXPORT_COLUMNS}
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader, None) or []
            idx = {h.strip().lower(): i for i, h in enumerate(header)}
            if labels["first_name"] not in idx or labels["venue_name"] not in idx:
                raise ValueError("This does not look like a Ticket Manager CSV file.")
            existing = {self._dup_key(t) for t in self.get_all_tickets()}
            added = skipped = invalid = 0
            for row in reader:
                if not any(c.strip() for c in row):
                    continue
                data = {}
                for key, _ in EXPORT_COLUMNS:
                    i = idx.get(labels[key])
                    v = row[i].strip() if i is not None and i < len(row) else ""
                    # undo the apostrophe the Android export adds before = + - @
                    if len(v) > 1 and v[0] == "'" and v[1] in "=+-@":
                        v = v[1:]
                    data[key] = v
                try:
                    data["price"] = float(data["price"].replace("$", "").replace(",", ""))
                except ValueError:
                    data["price"] = 0.0
                data["venue_type"] = _pick(data["venue_type"], VENUE_TYPES, "Other")
                data["ticket_type"] = _pick(data["ticket_type"], TICKET_TYPES, "Other")
                data["status"] = _pick(data["status"], STATUSES, "Active")
                if not data["venue_name"] or not (data["first_name"] or data["last_name"]):
                    invalid += 1
                    continue
                if self._dup_key(data) in existing:
                    skipped += 1
                    continue
                self.add_ticket(data)
                added += 1
        return added, skipped, invalid

    def sync_with_file(self, path: str) -> int:
        """Merge with a JSON sync file (e.g. in a Google Drive folder), newest edit wins,
        then write the merged result back. Returns how many tickets were updated here."""
        doc = None
        if os.path.exists(path) and os.path.getsize(path) > 0:
            if os.path.getsize(path) > SYNC_MAX_BYTES:
                raise ValueError("The sync file is too large.")
            with open(path, encoding="utf-8") as f:
                doc = json.load(f)
        changed, out = self.merge_doc(doc)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        try:
            os.replace(tmp, path)
        except OSError:
            # Some cloud or network mounts do not allow renaming over a file.
            with open(path, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=1)
            try:
                os.remove(tmp)
            except OSError:
                pass
        return changed

    def merge_doc(self, doc):
        """Merge a sync document (a dict, or None if there is none yet) into the database.
        Newest edit wins. Returns (number of tickets updated here, merged document)."""
        remote = []
        if doc is not None:
            if not isinstance(doc, dict) or not isinstance(doc.get("tickets"), list):
                raise ValueError("This is not Ticket Manager sync data.")
            if int(doc.get("version", 1)) > 1:
                raise ValueError("This sync data was made by a newer version of the app.")
            remote = doc["tickets"]
        local = {r["uid"]: r for r in self._rows_with_deleted() if r["uid"]}
        changed = 0
        for r in remote:
            if not isinstance(r, dict):
                continue
            uid = str(r.get("uid") or "").strip()
            if not uid:
                continue
            try:
                stamp = int(r.get("updated_at") or 0)
            except (TypeError, ValueError):
                stamp = 0
            mine = local.get(uid)
            if mine is None or stamp > mine["updated_at"]:
                self._write_synced(uid, r, stamp, exists=mine is not None)
                changed += 1
        self.conn.commit()
        out = {"version": 1, "tickets": [
            {**{k: row[k] for k in SYNC_FIELDS}, "uid": row["uid"],
             "updated_at": row["updated_at"], "deleted": bool(row["deleted"])}
            for row in sorted(self._rows_with_deleted(), key=lambda x: x["uid"]) if row["uid"]]}
        return changed, out

    def _rows_with_deleted(self):
        return [dict(r) for r in self.conn.execute("SELECT * FROM tickets")]

    def _write_synced(self, uid, r, stamp, exists):
        vals = []
        for k in SYNC_FIELDS:
            v = r.get(k)
            if k == "price":
                try:
                    vals.append(float(v or 0))
                except (TypeError, ValueError):
                    vals.append(0.0)
            else:
                vals.append("" if v is None else str(v)[:1000])
        deleted = 1 if r.get("deleted") else 0
        if exists:
            sets = ", ".join(f"{k}=?" for k in SYNC_FIELDS)
            self.conn.execute(f"UPDATE tickets SET {sets}, updated_at=?, deleted=? WHERE uid=?",
                              vals + [stamp, deleted, uid])
        else:
            cols = SYNC_FIELDS + ["uid", "updated_at", "deleted", "created_at"]
            self.conn.execute(
                f"INSERT INTO tickets ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
                vals + [uid, stamp, deleted, datetime.now().isoformat(timespec="seconds")])

    def close(self):
        self.conn.commit()
        self.conn.close()
