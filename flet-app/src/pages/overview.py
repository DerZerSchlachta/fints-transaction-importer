# pages/overview.py
import asyncio
import flet as ft
import requests

from stylize_transactions import parse_ledger_entry, format_ledger_object


def overview(page: ft.Page):
    response = requests.get("http://localhost:8000/api/state")
    data = response.json()
    unknown_transactions = data["unknown"]

    transactions = ft.Column()

    for transaction in unknown_transactions:
        structured = parse_ledger_entry(transaction["ledger"])
        page.data["tx"][transaction["id"]] = structured

        transactions.controls.append(
            ft.Button(
                format_ledger_object(structured),
                on_click=lambda e, id=transaction["id"]: asyncio.create_task(
                    page.push_route(f"/details/{id}")
                ),
            )
        )
        transactions.controls.append(ft.Divider(height=5))

    headline = ft.Text(
        "FinTS-Transaction-Importer",
        size=24,
        weight=ft.FontWeight.BOLD,
    )
    subheadline = ft.Text(
        f"{len(unknown_transactions)} unprocessed transactions"
    )

    return ft.View(
        route="/overview",
        controls=[
            ft.Column(
                controls=[
                    headline,
                    subheadline,
                    ft.Divider(height=10),
                    transactions,
                ],
                spacing=10,
            )
        ],
    )