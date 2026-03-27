# This module will be responsible for keeping a persistent database between runs of the Program:
# 1. logging all transactions which have been processed, with their process-status, so that they needn't be processed twice
# 2. logging all transactions which do not fit into the templates so that they can be presented, at a later point, to the user for confirmation / correction.

import json
import os

path = "data/db/transaction_db.json"
os.makedirs(os.path.dirname(path), exist_ok=True)

def db_load():
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except json.JSONDecodeError:
            existing = []
    else:
        existing = []

    return existing, {e.get("id") for e in existing if "id" in e}

def filter_processed_transactions(transactions):

    existing, ids = db_load()

    #   Create a new list of transactions with ID not present in existing ids:
    filtered_transactions = [t for t in transactions if t["id"] not in ids]

    return filtered_transactions

def save_as_processed(transactions):
    existing, ids = db_load()

    for t in transactions:
        if t["id"] not in ids:
            existing.append(t)
            ids.add(t["id"]) 

    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4, ensure_ascii=False)