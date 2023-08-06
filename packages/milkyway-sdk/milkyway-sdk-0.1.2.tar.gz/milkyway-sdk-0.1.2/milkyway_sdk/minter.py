import asyncio

from milkyway_sdk.terra_util import Account


class Minter:
    def __init__(self, account):
        self.account = account
        self.collection_contract = None

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
        print(f"Created Collection contract: {url}")

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
            print(f"Minted {len(mint_batch)} items")


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
    account = Account(lcd_client=lcd_client, key=key)
    minter = Minter(account)

    asyncio.get_event_loop().run_until_complete(
        minter.init_collection(collection_name, collection_symbol)
    )
    asyncio.get_event_loop().run_until_complete(minter.mint_items(items_json, batch_size))
