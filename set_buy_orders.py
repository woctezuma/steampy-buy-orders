import json
import time
from pathlib import Path

from steampy.client import SteamClient
from steampy.exceptions import ApiException
from steampy.models import Currency
from steampy.utils import GameOptions

with Path("data/price_to_appids.to_skip.json").open() as f:
    price_to_appids_0 = json.load(f)


def main() -> None:
    with Path("secrets.json").open() as f:
        secrets = json.load(f)

    steam_client = SteamClient(secrets["api_key"])
    steam_client.login(secrets["username"], secrets["password"], secrets["steam_guard"])

    # Reference: https://github.com/bukson/steampy#market-methods
    listings = steam_client.market.get_my_market_listings()

    print_threshold = 3
    for i in listings["buy_orders"].values():
        if i["quantity"] < print_threshold:
            print(i)
    # > {'order_id': '4968003847', 'quantity': 1, 'price': '0,12€', 'item_name': 'Railgun (Foil)'}
    # > {'order_id': '4968008301', 'quantity': 2, 'price': '0,12€', 'item_name': 'Survivor (Foil)'}
    # > {'order_id': '4968028709', 'quantity': 2, 'price': '0,09€', 'item_name': 'Close Quarters Combat (Foil)'}
    # > {'order_id': '4968053367', 'quantity': 1, 'price': '0,11€', 'item_name': 'Cheeseburger (Foil)'}

    # Reference: https://gist.github.com/woctezuma/23e34a3bc4c0304840ce406903aec514
    price_to_appids = price_to_appids_0

    remove_app_ids = False

    if remove_app_ids:
        for price, appids in price_to_appids.items():
            if price in price_to_appids_0:
                print(
                    f"[price: {price} cents] Removing {sorted(set(appids).intersection(price_to_appids_0[price]), key=str)}",
                )
                price_to_appids[price] = list(
                    set(appids).difference(price_to_appids_0[price]),
                )

    with Path("../steam-market/data/listings_for_foil_cards.json").open(
        encoding="utf8",
    ) as f:
        foil_cards = json.load(f)

    target_appids_as_list = []
    for app_list in price_to_appids.values():
        target_appids_as_list += app_list
    target_appids = set(target_appids_as_list)

    appid_to_cards: dict[int, list[str]] = {}
    for card_name in foil_cards:
        app_id = int(card_name.split("-")[0])
        if app_id in target_appids:
            if app_id not in appid_to_cards:
                appid_to_cards[app_id] = []
            appid_to_cards[app_id].append(card_name)

    ## To cancel buy orders:
    remove_buy_orders = False

    if remove_buy_orders:
        for e in listings["buy_orders"].values():
            if e["price"] == "0,11€":
                if any(
                    s in e["item_name"]
                    for s in (
                        "Cheeki Breeki",
                        "Cop",
                        "Nagibator",
                        "Survivalist",
                        "Zombie",
                    )
                ):
                    continue
                print(e["item_name"])
                print(e["order_id"])
                response = steam_client.market.cancel_sell_order(e["order_id"])
                time.sleep(1)

    card_names_with_existing_buy_orders = [
        e["item_name"] for e in listings["buy_orders"].values()
    ]

    for price_single_item in price_to_appids:
        # Set 100 buy orders at {price_single_item} for every foil card for every appID in the list price_to_appids[price_single_item]
        quantity = 100

        for app_id in sorted(price_to_appids[price_single_item], key=str):
            print(f"AppID: {app_id}")
            for market_name in appid_to_cards[app_id]:
                print(f"- {market_name}")

                card_name = market_name.lstrip(f"{app_id}-")
                if card_name in card_names_with_existing_buy_orders:
                    continue
                print("TODO")

                try:
                    response = steam_client.market.create_buy_order(
                        market_name,
                        price_single_item,
                        quantity,
                        GameOptions.STEAM,
                        Currency.EURO,
                    )
                except ApiException:
                    response = None

                print(response)
                time.sleep(1)


if __name__ == "__main__":
    main()
