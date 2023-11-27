def get_target_appids(price_to_appids: dict[str, list[int]]) -> list[int]:
    target_appids = []
    for app_list in price_to_appids.values():
        target_appids += app_list
    return list(set(target_appids))


def get_appid_to_cards(
    foil_cards: list[str],
    target_appids: list[int],
) -> dict[int, list[str]]:
    appid_to_cards: dict[int, list[str]] = {}
    for card_name in foil_cards:
        app_id = int(card_name.split("-")[0])
        if app_id in target_appids:
            if app_id not in appid_to_cards:
                appid_to_cards[app_id] = []
            appid_to_cards[app_id].append(card_name)
    return appid_to_cards


def clean_price_to_appids(
    price_to_appids: dict[str, list[int]],
    price_to_appids_to_skip: dict[str, list[int]],
) -> dict[str, list[int]]:
    for price, appids in price_to_appids.items():
        if price in price_to_appids_to_skip:
            inter = set(appids).intersection(price_to_appids_to_skip[price])
            diff = set(appids).difference(price_to_appids_to_skip[price])

            print(f"[price: {price} cents] Removing {sorted(inter, key=str)}")
            price_to_appids[price] = list(diff)
    return price_to_appids
