from milkyway_sdk.terra_utils import AsyncLCDClient

DEFAULT_GAS_PRICES = {
    "uluna": "0.15",
    "usdr": "0.1018",
    "uusd": "0.15",
    "ukrw": "178.05",
    "umnt": "431.6259",
    "ueur": "0.125",
    "ucny": "0.97",
    "ujpy": "16",
    "ugbp": "0.11",
    "uinr": "11",
    "ucad": "0.19",
    "uchf": "0.13",
    "uaud": "0.19",
    "usgd": "0.2",
}


def create_lcd_client(url='https://bombay-fcd.terra.dev', chain_id='bombay-10', gas_prices=DEFAULT_GAS_PRICES):
    return AsyncLCDClient(url, chain_id=chain_id, gas_prices=gas_prices)
