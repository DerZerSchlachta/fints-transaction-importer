from datetime import date, timedelta
from decimal import Decimal
from fints.client import FinTS3PinTanClient
from dotenv import load_dotenv
import os

load_dotenv()


def get_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing env var: {name} make sure you have set it!")
    return value


BANK_ID = get_env("FINTS_BANK_ID")
USER_ID = get_env("FINTS_USER_ID")
PIN = get_env("FINTS_PIN")
ACCOUNT_IBAN = get_env("FINTS_ACCOUNT_IBAN")
PRODUCT_ID = get_env("FINTS_PRODUCT_ID")
SERVER = get_env("FINTS_SERVER")
SCAN_PERIOD = int(get_env("FINTS_SCAN_PERIOD_DAYS"))


def _clean_transaction(tx):
    """
    Convert a raw FinTS Transaction object into a clean, ledger-friendly dict.
    """

    data = tx.data

    # Amount and currency
    amount_obj = data.get('amount')
    amount = float(amount_obj.amount) if amount_obj else 0
    currency = amount_obj.currency if amount_obj else "EUR"

    return {
        "id": data.get("bank_reference"),
        "date": data.get("date").strftime("%Y/%m/%d") if data.get("date") else None,
        "issuer": data.get('applicant_name') or data.get('recipient_name'),
        "description": data.get("purpose"),
        "type": "Income" if amount >= 0 else "Expense",
        "amount": amount,
        "currency": currency
    }


def fetch_transactions():
    client = FinTS3PinTanClient(
        bank_identifier=BANK_ID,
        user_id=USER_ID,
        pin=PIN,
        server=SERVER,
        product_id=PRODUCT_ID
    )

    # TAN setup
    client.fetch_tan_mechanisms()
    client.set_tan_mechanism('946')

    # Find account
    accounts = client.get_sepa_accounts()
    giro = next(
        (acc for acc in accounts if acc.iban == ACCOUNT_IBAN),
        None
    )

    if not giro:
        raise RuntimeError("Account IBAN not found")

    # Date range
    end_date = date.today()
    start_date = end_date - timedelta(days=SCAN_PERIOD)

    transactions = client.get_transactions(giro, start_date, end_date)

    # Clean and normalize output
    return [_clean_transaction(tx) for tx in transactions]