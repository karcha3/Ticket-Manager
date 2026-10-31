"""Tests for the ticket database: sync merge, CSV import and database upgrades."""
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import time
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database  # noqa: E402


def ticket(first, venue="Arena", price=10, **extra):
    t = dict(first_name=first, last_name="X", venue_type="Concert", ticket_type="Standard",
             venue_name=venue, location="", date="2026-11-01", time="19:00", seat="",
             price=price, status="Active", notes="")
    t.update(extra)
    return t


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.sync = os.path.join(self.dir, "sync.json")
        self.a = database.Database(os.path.join(self.dir, "a.db"))
        self.b = database.Database(os.path.join(self.dir, "b.db"))
        self.addCleanup(self.a.close)
        self.addCleanup(self.b.close)

    @staticmethod
    def names(db):
        return sorted(r["first_name"] for r in db.get_all_tickets())

    @staticmethod
    def tick():
        time.sleep(0.01)   # updated_at has millisecond resolution


class BasicTests(DatabaseTestCase):
    def test_delete_is_soft_and_hidden(self):
        i = self.a.add_ticket(ticket("Ann"))
        self.a.delete_ticket(i)
        self.assertEqual(self.names(self.a), [])
        self.assertEqual(self.a.get_distinct_venues(), [])
        rows = self.a._rows_with_deleted()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["deleted"], 1)

    def test_new_tickets_get_a_unique_id(self):
        self.a.add_ticket(ticket("Ann"))
        self.a.add_ticket(ticket("Bob"))
        uids = [r["uid"] for r in self.a._rows_with_deleted()]
        self.assertEqual(len(set(uids)), 2)
        self.assertTrue(all(uids))


class SyncFileTests(DatabaseTestCase):
    def test_two_devices_share_tickets(self):
        self.a.add_ticket(ticket("Ann"))
        self.a.add_ticket(ticket("Bob"))
        self.assertEqual(self.a.sync_with_file(self.sync), 0)    # file did not exist yet
        self.assertEqual(self.b.sync_with_file(self.sync), 2)
        self.assertEqual(self.names(self.b), ["Ann", "Bob"])

    def test_edit_and_delete_travel(self):
        ann = self.a.add_ticket(ticket("Ann"))
        bob = self.a.add_ticket(ticket("Bob"))
        self.a.sync_with_file(self.sync)
        self.b.sync_with_file(self.sync)
        self.tick()
        b_ann = [r for r in self.b.get_all_tickets() if r["first_name"] == "Ann"][0]
        self.b.update_ticket(b_ann["id"], ticket("Ann", price=99, status="Used"))
        self.a.delete_ticket(bob)
        for db in (self.b, self.a, self.b):
            db.sync_with_file(self.sync)
        for db in (self.a, self.b):
            rows = db.get_all_tickets()
            self.assertEqual([(r["first_name"], r["price"], r["status"]) for r in rows],
                             [("Ann", 99.0, "Used")])
        self.assertEqual(self.a.get_distinct_venues(), ["Arena"])

    def test_newest_edit_wins_a_conflict(self):
        self.a.add_ticket(ticket("Ann"))
        self.a.sync_with_file(self.sync)
        self.b.sync_with_file(self.sync)
        self.tick()
        self.a.update_ticket(self.a.get_all_tickets()[0]["id"], ticket("Ann", price=1))
        self.tick()
        self.b.update_ticket(self.b.get_all_tickets()[0]["id"], ticket("Ann", price=2))
        self.a.sync_with_file(self.sync)
        self.b.sync_with_file(self.sync)
        self.a.sync_with_file(self.sync)
        self.assertEqual(self.a.get_all_tickets()[0]["price"], 2.0)
        self.assertEqual(self.b.get_all_tickets()[0]["price"], 2.0)

    def test_android_scan_code_survives_a_desktop_edit(self):
        self.a.add_ticket(ticket("Ann"))
        self.a.sync_with_file(self.sync)
        with open(self.sync) as f:
            doc = json.load(f)
        doc["tickets"][0]["code"] = "TM-ABC"
        doc["tickets"][0]["updated_at"] += 5000
        with open(self.sync, "w") as f:
            json.dump(doc, f)
        self.a.sync_with_file(self.sync)
        row = self.a.get_all_tickets()[0]
        self.a.update_ticket(row["id"], ticket("Ann", price=3))
        code = self.a.conn.execute("SELECT code FROM tickets WHERE id=?", (row["id"],)).fetchone()[0]
        self.assertEqual(code, "TM-ABC")

    def test_bad_files_are_refused_and_not_overwritten(self):
        self.a.add_ticket(ticket("Ann"))
        for content in ('{"nope": 1}', "not json", json.dumps({"version": 2, "tickets": []})):
            with open(self.sync, "w") as f:
                f.write(content)
            with self.assertRaises(ValueError):          # JSONDecodeError is a ValueError
                self.a.sync_with_file(self.sync)
            with open(self.sync) as f:
                self.assertEqual(f.read(), content)
        self.assertEqual(self.names(self.a), ["Ann"])

    def test_falls_back_when_rename_is_not_allowed(self):
        self.a.add_ticket(ticket("Ann"))
        with mock.patch("os.replace", side_effect=OSError("not allowed")):
            self.a.sync_with_file(self.sync)
        self.assertGreater(os.path.getsize(self.sync), 0)
        self.assertFalse(os.path.exists(self.sync + ".tmp"))


class UpgradeTests(DatabaseTestCase):
    def test_old_database_is_upgraded(self):
        old = os.path.join(self.dir, "old.db")
        c = sqlite3.connect(old)
        c.execute("CREATE TABLE tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, "
                  "last_name TEXT NOT NULL, venue_type TEXT, ticket_type TEXT, venue_name TEXT, "
                  "location TEXT, date TEXT, time TEXT, seat TEXT, price REAL DEFAULT 0, "
                  "status TEXT, notes TEXT, created_at TEXT)")
        c.execute("INSERT INTO tickets (first_name, last_name, venue_name) VALUES ('Old','Row','Hall')")
        c.commit()
        c.close()
        db = database.Database(old)
        self.addCleanup(db.close)
        row = db.get_all_tickets()[0]
        self.assertEqual(row["first_name"], "Old")
        self.assertTrue(row["uid"])
        self.assertGreater(row["updated_at"], 0)


HEADER = ("First Name,Last Name,Venue Type,Ticket Type,Venue / Event,Location,Date,Time,"
          "Seat / Section,Price,Status,Notes\n")


class ImportTests(DatabaseTestCase):
    def write(self, text):
        path = os.path.join(self.dir, "in.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_import_then_import_again_skips_duplicates(self):
        path = self.write(HEADER + "Zed,Q,Concert,Standard,Hall,,2026-12-01,20:00,,\"$5.50\",Active,\n")
        self.assertEqual(self.a.import_csv(path), (1, 0, 0))
        self.assertEqual(self.a.import_csv(path), (0, 1, 0))
        self.assertEqual(self.a.get_all_tickets()[0]["price"], 5.5)

    def test_invalid_rows_and_unknown_choices(self):
        path = self.write(HEADER + ",,Concert,Standard,,,,,,1,Active,\n"
                                   "Amy,B,Weird,Odd,Hall,,,,,1,Nonsense,\n")
        self.assertEqual(self.a.import_csv(path), (1, 0, 1))
        row = self.a.get_all_tickets()[0]
        self.assertEqual((row["venue_type"], row["ticket_type"], row["status"]), ("Other", "Other", "Active"))

    def test_apostrophe_added_by_the_android_export_is_removed(self):
        path = self.write(HEADER + "Amy,B,Concert,Standard,Hall,,,,,1,Active,'=SUM(A1)\n")
        self.a.import_csv(path)
        self.assertEqual(self.a.get_all_tickets()[0]["notes"], "=SUM(A1)")

    def test_a_file_that_is_not_ours_is_refused(self):
        with self.assertRaises(ValueError):
            self.a.import_csv(self.write("a,b,c\n1,2,3\n"))


if __name__ == "__main__":
    unittest.main()
