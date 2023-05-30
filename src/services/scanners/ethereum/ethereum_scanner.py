import requests
from collections import defaultdict
from abc import ABC
from typing import List, Generator

from models import ScannerInterface, TransactionEdge, TransactionType


class EthereumScanner(ScannerInterface, ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_txs_for_address(self, address: str, internal: bool = False,
                            startblock: int = 0, endblock: int = 99999999,
                            direction: str = "any", address_limit=None, offset = 10000) -> Generator[TransactionEdge, None, None]:
        action = 'txlistinternal' if internal else 'txlist'
        page = 1
        if address_limit is None:
            address_limit = offset + 1
        txs = []
        errors_in_row = 0
        while True:
            url = f'https://api.etherscan.io/api?module=account&page={page}$offset={offset}&action={action}&address={address}&startblock={startblock}&endblock={endblock}&apikey={self.api_key}'
            try:
                res = requests.get(url)
                txs_as_dicts = res.json()['result']
                if len(txs_as_dicts) >= address_limit:
                    return
                for _tx_dict in txs_as_dicts:
                    if int(_tx_dict["isError"]) != 0:
                        continue
                    if _tx_dict['to'].lower() == _tx_dict['from'].lower():
                        continue
                    tx_dict = defaultdict(lambda: None)
                    tx_dict.update(_tx_dict)
                    tx_type = TransactionType.SEND
                    trace_id = ''
                    address_to = tx_dict['to']
                    if tx_dict['contractAddress'] != '':
                        tx_type = TransactionType.CALL
                    if tx_dict['to'] == '':
                        tx_type = TransactionType.CREATE
                        address_to = tx_dict['contractAddress']
                    if internal:
                        tx_type = TransactionType.INTERNAL
                        trace_id = tx_dict['traceId']
                        
                    if direction == "to" and address.lower() != address_to.lower():
                        continue
                    if direction == "from" and address.lower() != tx_dict['from'].lower():
                        continue
                    tx = TransactionEdge(
                        tx_hash=tx_dict['hash'],
                        address_from=tx_dict['from'].lower(),
                        address_to=address_to.lower(),
                        trace_id=trace_id,
                        date=tx_dict['timeStamp'],
                        tx_type=tx_type,
                        value=tx_dict['value'],
                        block=tx_dict['blockNumber'],
                        gas=tx_dict['gas'],
                        gas_price=tx_dict['gasPrice']
                    )
                    yield tx

                if len(txs_as_dicts) < 10000:
                    break
                startblock = txs_as_dicts[-1]['blockNumber']
                if startblock > endblock:
                    break
                errors_in_row = 0
            except Exception as e:
                errors_in_row += 1
                if errors_in_row > 5:
                    break
