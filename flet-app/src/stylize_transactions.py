import flet as ft


def parse_ledger_entry(ledger: str):
    lines = ledger.strip().splitlines()
    if not lines:
        return {}

    # First line: "2026/04/01 * Payee | purpose"
    first_line = lines[0].strip()
    date, _, rest = first_line.partition(" ")
    payee_purpose = rest.lstrip("* ").strip()

    payee = ""
    purpose = ""
    if "|" in payee_purpose:
        payee, purpose = payee_purpose.split("|", 1)
        payee = payee.strip()
        purpose = purpose.strip()
    else:
        payee = payee_purpose

    # Postings: remaining lines
    postings = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) >= 2:
            # Line has amount and currency, e.g. "Expense:Unknown 30.88 EUR"
            account = " ".join(parts[:-2])
            amount = parts[-2]
            currency = parts[-1]
        else:
            # Line is just an account, e.g. "Assets:Checking:GLSBank"
            account = " ".join(parts)
            amount = ""
            currency = ""

        # Append the posting you just built
        postings.append({
            "account": account,
            "amount": amount,
            "currency": currency,
        })

    return {"date": date, "payee": payee, "purpose": purpose, "postings": postings}

# at the top of your file

ACCENT        = "#F5E3BE"  # beige for * / | and amount
ACCOUNT       = "#B33C3A"  # red for accounts
DATE          = "#F4CC5C"  # warm yellow for date
PAYEE         = "#497C77"  # muted teal for payee
PURPOSE       = "#435F8D"  # dark blue for purpose (foreground accent)


def format_ledger_object(ledger_object):
    spans = []

    # First line: date * payee | purpose
    spans.extend([
        ft.TextSpan(ledger_object["date"], style=ft.TextStyle(color=DATE)),
        ft.TextSpan("  *  ", style=ft.TextStyle(color=ACCENT)),
        ft.TextSpan(ledger_object["payee"], style=ft.TextStyle(color=PAYEE)),
    ])

    if purpose := ledger_object.get("purpose"):
        spans.extend([
            ft.TextSpan(" | ", style=ft.TextStyle(color=ACCENT)),
            ft.TextSpan(purpose, style=ft.TextStyle(color=PURPOSE)),
        ])

    # Every posting
    for p in ledger_object["postings"]:
        spans.append(ft.TextSpan("\n"))
        spans.append(ft.TextSpan("        "))

        spans.append(ft.TextSpan(p["account"], style=ft.TextStyle(color=ACCOUNT)))

        spans.append(ft.TextSpan("                           "))

        spans.append(ft.TextSpan(p["amount"], style=ft.TextStyle(color=ACCENT)))
        spans.append(ft.TextSpan(" "))
        spans.append(ft.TextSpan(p["currency"], style=ft.TextStyle(color=PURPOSE)))

    return ft.Text(
        spans=spans,
        style=ft.TextStyle(
            font_family="monospace",
            color=ft.Colors.WHITE,
        ),
    )