from steampy.client import SteamClient

from src.data_utils import (
    APPIDS_FNAME,
    APPIDS_TO_SKIP_FNAME,
    FOIL_CARDS_FNAME,
    SECRETS_FNAME,
)
from src.json_utils import load_json, load_json_as_list
from src.order_utils import cancel_buy_orders, set_buy_orders
from src.print_utils import show_low_quantity_buy_orders
from src.utils import clean_price_to_appids, get_appid_to_cards, get_target_appids


def main() -> None:
    secrets = load_json(SECRETS_FNAME)

    steam_client = SteamClient(secrets["api_key"])
    steam_client.login(secrets["username"], secrets["password"], secrets["steam_guard"])

    # Reference: https://github.com/bukson/steampy#market-methods
    listings = steam_client.market.get_my_market_listings()

    show_low_quantity_buy_orders(listings, quantity_threshold=3)

    ## Clean dictionary

    price_to_appids = load_json(APPIDS_FNAME)
    price_to_appids_to_skip = load_json(APPIDS_TO_SKIP_FNAME)

    price_to_appids = clean_price_to_appids(price_to_appids, price_to_appids_to_skip)

    ## Cancel buy orders

    cancel_buy_orders(
        steam_client,
        listings,
        price_of_interest="0,11€",
        names_to_keep=(
            "Cheeki Breeki",
            "Cop",
            "Nagibator",
            "Survivalist",
            "Zombie",
        ),
    )

    ## Set buy orders

    foil_cards = load_json_as_list(FOIL_CARDS_FNAME)
    target_appids = get_target_appids(price_to_appids)
    appid_to_cards = get_appid_to_cards(foil_cards, target_appids)

    set_buy_orders(
        steam_client,
        listings,
        price_to_appids,
        appid_to_cards,
        quantity=100,
    )


if __name__ == "__main__":
    main()
