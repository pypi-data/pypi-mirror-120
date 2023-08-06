import asyncio

from milkyway_sdk.async_utils import async_to_sync
from milkyway_sdk.terra_utils import Account


class Minter:
    def __init__(self, key, lcd_client):
        self.account = Account(lcd_client=lcd_client, key=key)
        self.collection_contract = None

    @async_to_sync
    async def init_collection(self, collection_name, collection_symbol):
        # txn 1) store code for contract
        nft_code_id = await self.account.store_contract("cw721_base")
        # txn 2) instantiate collection contract (from the code)
        self.collection_contract = await self.account.contract.create(
            nft_code_id,
            name=collection_name,
            symbol=collection_symbol,
            minter=self.account.acc_address,
        )
        url = f'https://finder.terra.money/{self.account.terra.chain_id}/address/{self.collection_contract.address}'
        self._log(f"Created Collection contract: {url}")

    def _log(self, s):
        print(f"[milkyway_sdk.minter] {s}")

    @async_to_sync
    async def mint_items(self, items_json, batch_size=100):
        def insert_owner(nft_details):
            if "owner" not in nft_details:
                nft_details["owner"] = self.account.acc_address
            return nft_details

        for i in range(0, len(items_json), batch_size):
            mint_batch = items_json[i : i + batch_size]
            # txn i) chain all of these .mint() into one txn
            # pass in JSON blob to a standard CosmWasm Mint: https://github.com/CosmWasm/cw-plus/blob/b126b5a702c0567e4957767fca7450efa97e4645/contracts/cw721-base/src/msg.rs#L53
            await self.account.chain(
                *[
                    self.collection_contract.mint(**insert_owner(nft_details))
                    for nft_details in mint_batch
                ]
            )
            self._log(f"Minted {len(mint_batch)} items")


def mint_collection(key, collection_name, collection_symbol, items_json, batch_size=100, lcd_client=None):
    """
    :param key: Wallet Key can be of type MnemonicKey
    :param collection_name: Name of your collection.
    :param collection_symbol: Collection symbol doesn't have to be globally unique
    :param items_json: List of Items to mint for the Collection.
    :param batch_size: How many MintMsg to chain together per transaction
    :param lcd_client: Can be "None" to signify LocalTerra
    :return:
    """
    minter = Minter(key, lcd_client)
    minter.init_collection(collection_name, collection_symbol)
    minter.mint_items(items_json, batch_size)
