def handle_account_created(event: dict):
    account_id = event["account_id"]
    user_id = event["user_id"]
    created_at = event["created_at"]

    print(f"[EVENT] account.created → {event}")

    # Your logic: initialize ledger / create account entry:
    # ledger = LedgerModel(...)
    # db.add(ledger)
    # db.commit()
