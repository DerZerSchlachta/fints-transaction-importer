from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.database_manager import save_as_processed
import json
import os

from pydantic import BaseModel

class TransactionUpdate(BaseModel):
    id: str
    ledger: str
    date: str
    path: str


app = FastAPI()

# Resolve project root (since this file is inside /app)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_DIR = os.path.join(BASE_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "data", "db", "unknown_transactions.json")

# Serve static frontend files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


# ----------------------------
# API: Unknown transactions
# ----------------------------
@app.get("/api/unknown-transactions")
def get_unknown_transactions():
    import json
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "data", "db", "unknown_transactions.json")

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

@app.post("/api/update-transaction")
def update_transaction(tx: TransactionUpdate):
    from app.ledger_writer import write_ledger_entries
    from app.database_manager import save_as_processed  # assuming this exists

    tx_dict = tx.dict()

    # 1. Save as processed (wrap in list if your function expects a list)
    save_as_processed([tx_dict])

    # 2. Write ledger (also expects a list)
    write_ledger_entries([tx_dict])

    # 3. Remove from unknown_transactions.json
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        data = [entry for entry in data if entry["id"] != tx.id]

        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return {"status": "ok", "id": tx.id}