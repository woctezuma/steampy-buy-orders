# Steampy: buy orders

[![Code Quality][codacy-image]][codacy]

This repository contains Python code to automatically set buy orders with [`steampy`][steampy].

## Requirements

-   Install the latest version of [Python 3.X][python] (at least version 3.10).
-   Install the required packages:

```bash
pip install -r requirements.txt
```

## Data

-   Set your secrets in `data/secrets.json`:
```json
{
    "api_key": "PASTE_YOUR_SECRET_HERE",
    "username": "PASTE_YOUR_SECRET_HERE",
    "password": "PASTE_YOUR_SECRET_HERE",
    "steam_guard": "PASTE_YOUR_SECRET_HERE"
}
```

-   Get a [listings of foil cards][foil-cards] from [`steam-market`][steam-market].

- Specify the foil cards of interest in `data/price_to_appids.json`.

## Usage

- To automatically set buy orders, run:

```bash
python apply_workflow.py
```

## References

- [`bukson/steampy`][steampy]: a Steam trading library for Python,
- [`woctezuma/steam-market`][steam-market]: find arbitrages on the Steam Market.

<!-- Definitions -->

[python]: <https://www.python.org/downloads/>
[steampy]: <https://github.com/bukson/steampy>
[steam-market]: <https://github.com/woctezuma/steam-market>
[foil-cards]: <https://github.com/woctezuma/steam-market/blob/master/data/listings_for_foil_cards.json>

[pyup]: <https://pyup.io/repos/github/woctezuma/steampy-buy-orders/>
[dependency-image]: <https://pyup.io/repos/github/woctezuma/steampy-buy-orders/shield.svg>
[python3-image]: <https://pyup.io/repos/github/woctezuma/steampy-buy-orders/python-3-shield.svg>
[codacy]: <https://app.codacy.com/gh/woctezuma/steampy-buy-orders/>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/8ac75ffbd0d647fcb3720dbff8a64eee>
