"""SQLite-backed storage for tickets."""

import os
import sqlite3
import csv
from datetime import datetime

from resources import app_data_dir

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

    def add_ticket(self, data: dict) -> int:
        cur = self.conn.execute("""
            INSERT INTO tickets
                (first_name, last_name, venue_type, ticket_type, venue_name,
                 location, date, time, seat, price, status, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["first_name"], data["last_name"], data["venue_type"],
            data["ticket_type"], data["venue_name"], data["location"],
            data["date"], data["time"], data["seat"], data["price"],
            data["status"], data["notes"], datetime.now().isoformat(timespec="seconds")
        ))
        self.conn.commit()
        return cur.lastrowid

    def update_ticket(self, ticket_id: int, data: dict):
        self.conn.execute("""
            UPDATE tickets SET
                first_name=?, last_name=?, venue_type=?, ticket_type=?,
                venue_name=?, location=?, date=?, time=?, seat=?, price=?,
                status=?, notes=?
            WHERE id=?
        """, (
            data["first_name"], data["last_name"], data["venue_type"],
            data["ticket_type"], data["venue_name"], data["location"],
            data["date"], data["time"], data["seat"], data["price"],
            data["status"], data["notes"], ticket_id
        ))
        self.conn.commit()

    def delete_ticket(self, ticket_id: int):
        self.conn.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))
        self.conn.commit()

    def get_all_tickets(self):
        cur = self.conn.execute("SELECT * FROM tickets ORDER BY date ASC, time ASC")
        return [dict(row) for row in cur.fetchall()]

    def get_distinct_venues(self):
        cur = self.conn.execute("""
            SELECT DISTINCT venue_name FROM tickets
            WHERE venue_name IS NOT NULL AND TRIM(venue_name) != ''
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

    def close(self):
        self.conn.commit()
        self.conn.close()
