from fetch_transactions import fetch_transactions
from process_transactions import process_transactions
from database_manager import filter_processed_transactions, save_as_processed
from ledger_writer import write_ledger_entries

import json

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def main():
    transactions = fetch_transactions()

    new_transactions = filter_processed_transactions(transactions)

    # Process into ledger entries
    known_entries, unknown_entries, processed_transactions = process_transactions(new_transactions)

    save_as_processed(processed_transactions)

    # --- Known entries ---
    print_section("PROCESSED LEDGER ENTRIES")

    for entry in known_entries:
        print(entry["ledger"])
        print("-" * 40)

    # --- Unknown entries ---
    print_section("UNKNOWN TRANSACTION TYPES")

    for entry in unknown_entries:
        print(entry["ledger"])
        print("-" * 40)

    write_ledger_entries(known_entries)


    for entry in unknown_entries:  
        with open("data/db/unknown_transactions.json", "w", encoding="utf-8") as f:
            json.dump(unknown_entries, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()


# The Task of this Program, is in all essense, to turn this:

"""
{
    'amount': -14.87,
    'issuer': 'EDEKA Wirth',
    'currency': 'EUR',
    'date': '2026/03/26',
    'description': 'EDEKA Wirth/HANNOVER/DE 25.03.2026 um 17:39:15 Uhr '
                    '64044649/812070/ECTL/NPIN 43060967/4132298900/0/1226 REF '
                    '983815/260045',
    'type': 'Expense'
 }
"""

# into this:

"""
2026/03/26 * EDEKA Wirth | Lebensmitteleinkauf
    Expenses:Essen:Lebensmitteleinkauf      14.87 EUR
    Assets:Checking:GLSBank
"""