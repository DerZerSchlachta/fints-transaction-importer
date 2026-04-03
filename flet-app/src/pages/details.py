# pages/details.py
from flet import View
import flet as ft

from stylize_transactions import format_ledger_object


def details(page: ft.Page, transaction_id: str) -> View:
    # Try to get pre‑parsed ledger data from page.data
    tx_data = page.data.get("tx", {})
    structured = tx_data.get(transaction_id)

    if structured is None:
        # Fallback: show error or refetch
        return ft.View(
            route=f"/details/{transaction_id}",
            controls=[
                ft.Text("Transaction not found", size=20, color=ft.Colors.RED),
                ft.ElevatedButton(
                    "Back to overview",
                    on_click=lambda e: page.push_route("/overview"),
                ),
            ],
        )

    ledger_text = format_ledger_object(structured)

    return ft.View(
        route=f"/details/{transaction_id}",
        controls=[
            ft.Text(f"Details for {transaction_id}", size=30),
            ledger_text,
            ft.ElevatedButton(
                "Back to overview",
                on_click=lambda e: page.push_route("/overview"),
            ),
        ],
    )