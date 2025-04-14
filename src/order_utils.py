import time

from steampy.client import SteamClient
from steampy.exceptions import ApiException
from steampy.models import Currency
from steampy.utils import GameOptions

COOLDOWN_IN_SECONDS: int = 1


def cancel_buy_orders(
    steam_client: SteamClient,
    listings: dict,
    price_of_interest: str = "0,11€",
    names_to_keep: tuple = (),
) -> None:
    for e in listings["buy_orders"].values():
        if e["price"] == price_of_interest:
            if any(s in e["item_name"] for s in names_to_keep):
                continue
            print(f"{e['item_name']} -> {e['order_id']}")
            steam_client.market.cancel_sell_order(e["order_id"])
            time.sleep(COOLDOWN_IN_SECONDS)


def set_buy_orders(
    steam_client: SteamClient,
    listings: dict,
    price_to_appids: dict[str, list[int]],
    appid_to_cards: dict[int, list[str]],
    quantity: int = 100,
) -> None:
    card_names_with_existing_buy_orders = [
        e["item_name"] for e in listings["buy_orders"].values()
    ]

    for price_single_item, app_ids in price_to_appids.items():
        # Set {quantity} buy orders at {price_single_item} for every foil card for every appID in the list price_to_appids[price_single_item]

        for app_id in sorted(app_ids, key=str):
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
                time.sleep(COOLDOWN_IN_SECONDS)
