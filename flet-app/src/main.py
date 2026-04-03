# main.py
import flet as ft
import asyncio
import re

from pages.overview import overview
from pages.details import details


async def main(page: ft.Page):
    page.title = "FinTS2Paisa"

    # Initialize data store
    if page.data is None:
        page.data = {}
    page.data.setdefault("tx", {})

    def route_change(e=None):
        page.views.clear()

        route = page.route

        if route == "/overview":
            page.views.append(overview(page))
        elif m := re.fullmatch(r"/details/([^/]+)", route):
            transaction_id = m.group(1)
            page.views.append(details(page, transaction_id))
        else:
            page.push_route("/overview")

        page.update()

    page.on_route_change = route_change
    await page.push_route("/overview")


ft.run(main, route_url_strategy=ft.RouteUrlStrategy.PATH)