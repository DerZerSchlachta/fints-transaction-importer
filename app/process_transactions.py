# Purpose of this module is to match incoming Transaction onto a set of templates, 
# and fill a fitting one out, or, if none fits, mark transactions as unknown

import yaml
import textwrap

def load_templates(path="data/conf/templates.yaml"):
    """Load YAML templates once."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def match_against_template(transaction, templates):
    for name, template in templates.items():
        if template.get("match-issuer") == transaction["issuer"]:
            # Fill template with trailing newline
            ledger_str = template["template"].format(
                date=transaction["date"],
                issuer=transaction["issuer"],
                # ledger is switched because amount, how I like to write it, is denominated as how it impacts the issuers account and not your own
                amount=transaction["amount"] * -1,     
                currency=transaction["currency"]
            ).rstrip() # remove any trailing whitespaces / newlines
            entry = {
                "ledger":ledger_str,
                "date":transaction["date"],
                "path":template.get("path"),
                "id":transaction["id"]
            }
            return entry
        
    return None # unknown transaction


def process_transactions(transactions):
    
    templates = load_templates()
    known_entries = []
    unknown_entries = []
    processed_transactions = []
    
    for t in transactions:
        entry = match_against_template(t, templates)

        if entry is not None:
            known_entries.append(entry)
            processed_transactions.append(t)

        else:
            ledger_str = textwrap.dedent("""
                {date} * {issuer} | {purpose}
                    {type}:Unknown      {amount} {currency}
                    Assets:Checking:GLSBank
            """).format(
                date=t["date"],
                issuer=t["issuer"],
                purpose=t.get("description", "Unknown"),
                amount=t["amount"] * -1,
                type=t["type"],
                currency=t["currency"]
            ).strip()
            entry = {
                "ledger": ledger_str,
                "date":t["date"],
                "path": "income.ledger" if t["amount"] >= 0 else "expenses.ledger",
                "id":t["id"]
            }

            unknown_entries.append(entry)

    return known_entries, unknown_entries, processed_transactions