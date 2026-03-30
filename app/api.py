from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import json

from app.database_manager import save_as_processed
from app.ledger_writer import write_ledger_entries

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
DB_PATH = BASE_DIR / "data" / "db" / "unknown_transactions.json"

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class TransactionUpdate(BaseModel):
    id: str
    ledger: str | None = None
    date: str | None = None
    path: str | None = None


def read_unknown_transactions():
    if not DB_PATH.exists():
        return []
    with DB_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_unknown_transactions(data):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.get("/")
def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/unknown/{transaction_id}")
def unknown_detail(transaction_id: str):
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/state")
def get_state():
    return {"unknown": read_unknown_transactions(), "known": []}


@app.post("/api/update-transaction")
def update_transaction(tx: TransactionUpdate):
    tx_dict = tx.model_dump()

    save_as_processed([tx_dict])
    if tx_dict["ledger"] is not None:
        write_ledger_entries([tx_dict])

    unknown = read_unknown_transactions()
    unknown = [entry for entry in unknown if entry.get("id") != tx.id]
    write_unknown_transactions(unknown)

    return {"status": "ok", "id": tx.id}