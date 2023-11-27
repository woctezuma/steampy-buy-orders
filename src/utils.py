def get_target_appids(price_to_appids: dict[str, str]) -> set:
    target_appids_as_list = []
    for app_list in price_to_appids.values():
        target_appids_as_list += app_list
    return set(target_appids_as_list)


def get_appid_to_cards(foil_cards: list[str], target_appids: list[int]) -> None:
    appid_to_cards: dict[int, list[str]] = {}
    for card_name in foil_cards:
        app_id = int(card_name.split("-")[0])
        if app_id in target_appids:
            if app_id not in appid_to_cards:
                appid_to_cards[app_id] = []
            appid_to_cards[app_id].append(card_name)


def clean_price_to_appids(
    price_to_appids: dict[str, str],
    price_to_appids_to_skip: dict[str, str],
) -> dict[str, str]:
    for price, appids in price_to_appids.items():
        if price in price_to_appids_to_skip:
            inter = set(appids).intersection(price_to_appids_to_skip[price])
            diff = set(appids).difference(price_to_appids_to_skip[price])

            print(f"[price: {price} cents] Removing {sorted(inter, key=str)}")
            price_to_appids[price] = list(diff)
    return price_to_appids
