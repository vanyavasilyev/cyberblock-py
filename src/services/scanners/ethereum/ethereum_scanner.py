import requests
from abc import ABC
from typing import List, Generator

from models import ScannerInterface, TransactionEdge, TransactionType


class EthereumScanner(ScannerInterface, ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_txs_for_address(self, address: str, internal: bool = False,
                            startblock: int = 0, endblock: int = 99999999) -> Generator[TransactionEdge, None, None]:
        action = 'txlistinternal' if internal else 'txlist'
        page = 1
        offset = 10000
        txs = []
        while True:
            url = f'https://api.etherscan.io/api?module=account&page={page}$offset={offset}&action={action}&address={address}&startblock={startblock}&endblock={endblock}&apikey={self.api_key}'
            try:
                res = requests.get(url)
                txs_as_dicts = res.json()['result']
                for tx_dict in txs_as_dicts:
                    tx_type = TransactionType.SEND
                    trace_id = ''
                    if tx_dict['contractAddress'] != '':
                        tx_type = TransactionType.CALL
                    if tx_dict['to'] == '':
                        tx_type = TransactionType.CREATE
                    if internal:
                        tx_type = TransactionType.INTERNAL
                        trace_id = tx_dict['traceId']
                    tx = TransactionEdge(
                        tx_hash=tx_dict['hash'],
                        address_from=tx_dict['from'],
                        address_to=tx_dict['to'],
                        trace_id=trace_id,
                        date=tx_dict['timeStamp'],
                        tx_type=tx_type,
                        value=tx_dict['value'],
                        block=tx_dict['blockNumber'],
                        gas=tx_dict['gas'],
                        gas_price=tx_dict['gasPrice']
                    )
                    yield tx
                page += 1
                if len(txs_as_dicts) < 10000:
                    break
            except (requests.exceptions.JSONDecodeError, TypeError):
                pass        
