from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
BASE_LEDGER_DIR = os.getenv("LEDGER_BASE_DIR", "journal")

def write_ledger_entries(ledger_entries):
    for ledger_entry in ledger_entries:

        if not ledger_entry.get("date") or not ledger_entry.get("path"):
            continue

        year = ledger_entry["date"][:4]  # expects YYYY/MM/DD format

        base_dir = Path(BASE_LEDGER_DIR) / year
        path = base_dir / ledger_entry["path"]

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "a", encoding="utf-8") as f:
            f.write(ledger_entry["ledger"].rstrip() + "\n\n")