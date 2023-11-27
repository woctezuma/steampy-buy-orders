def show_low_quantity_buy_orders(
    listings: dict,
    quantity_threshold: int = 3,
    verbose: bool = True,
) -> list[dict]:
    # > {'order_id': '4968003847', 'quantity': 1, 'price': '0,12€', 'item_name': 'Railgun (Foil)'}
    # > {'order_id': '4968008301', 'quantity': 2, 'price': '0,12€', 'item_name': 'Survivor (Foil)'}
    # > {'order_id': '4968028709', 'quantity': 2, 'price': '0,09€', 'item_name': 'Close Quarters Combat (Foil)'}
    # > {'order_id': '4968053367', 'quantity': 1, 'price': '0,11€', 'item_name': 'Cheeseburger (Foil)'}

    buy_orders = [
        i for i in listings["buy_orders"].values() if i["quantity"] < quantity_threshold
    ]
    if verbose:
        for i in buy_orders:
            print(i)
    return buy_orders
