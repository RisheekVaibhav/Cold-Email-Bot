"""utils/tracker.py — Track which companies have been emailed (logs/tracker.json)"""

import json
import os
from datetime import datetime


class Tracker:
    def __init__(self, path: str = "logs/tracker.json"):
        self.path = path
        self.data: list = []
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.data = []

    def find_duplicates(self, contacts: list) -> list:
        """
        Return tracker entries that match any email in the given contacts list.
        Used for pre-send duplicate warning.
        """
        contact_emails = {c["email"].lower() for c in contacts}
        return [
            entry for entry in self.data
            if entry.get("hr_email", "").lower() in contact_emails
            and entry.get("status") == "SENT"
        ]

    def update(self, contact: dict, status: str, note: str = ""):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "company":   contact.get("company", ""),
            "hr_name":   contact.get("name", ""),
            "hr_email":  contact.get("email", ""),
            "role":      contact.get("role", ""),
            "status":    status,
            "note":      note,
        }

        # Update existing entry for same email, or append new
        for i, existing in enumerate(self.data):
            if existing["hr_email"] == entry["hr_email"]:
                self.data[i] = entry
                return
        self.data.append(entry)

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def print_report(self):
        if not self.data:
            print("  No records yet.\n")
            return

        sent   = [e for e in self.data if e["status"] == "SENT"]
        failed = [e for e in self.data if e["status"] == "FAILED"]

        print(f"  Total companies contacted : {len(sent)}")
        print(f"  Failed                    : {len(failed)}")
        print()

        col = "{:<22} {:<20} {:<8}"
        print("  " + col.format("Company", "Role", "Status"))
        print("  " + "─" * 52)
        for e in self.data:
            company = e["company"][:20]
            role    = e["role"][:18]
            status  = e["status"]
            print("  " + col.format(company, role, status))
        print()
