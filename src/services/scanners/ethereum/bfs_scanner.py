from typing import Generator, Optional, Union
from queue import Queue
from collections import defaultdict

from models.graph import AddressNode, TransactionEdge, TransactionType
from .ethereum_scanner import EthereumScanner


class BFSEthScanner(EthereumScanner):
    def scan_from(self, address: str, max_inerations: Optional[int] = None,
                  startblock: int = 0, endblock: int = 99999999) -> Generator[Union[AddressNode, TransactionEdge], None, None]:
        iterations_left = max_inerations if max_inerations else -1
        address = address.lower()
        queue = Queue()
        queue.put((address, []))

        visited = set()
        visited.add('')

        address_set = set()
        address_set.add(address)
        tx_hash_set = set()
        while (not queue.empty()) and (iterations_left != 0):
            iterations_left -= 1
            cur_address, txs_to_add = queue.get()
            visited.add(cur_address)
            node = AddressNode(
                cur_address,
            )
            yield node
            for tx in txs_to_add:
                if tx.tx_type == TransactionType.INTERNAL:
                    tx_hash_set.add(tx.tx_hash + tx.trace_id)
                else:
                    tx_hash_set.add(tx.tx_hash)
                yield tx

            to_add = defaultdict(list)
            txs = self.get_txs_for_address(cur_address, False, startblock, endblock)
            for tx in txs:
                if (tx.address_to != cur_address) and (tx.address_to != ''):
                    if tx.address_to not in address_set:
                        to_add[tx.address_to].append(tx)

                if (tx.address_from != cur_address) and (tx.address_from != ''):
                    if tx.address_from not in address_set:
                        to_add[tx.address_from].append(tx)

                if (tx.tx_hash not in tx_hash_set) and (tx.address_from in visited) and (tx.address_to in visited):
                    tx_hash_set.add(tx.tx_hash)
                    yield tx

            internal_txs = self.get_txs_for_address(cur_address, True, startblock, endblock)
            for tx in internal_txs:
                if (tx.address_to != cur_address) and (tx.address_to != ''):
                    if tx.address_to not in address_set:
                        to_add[tx.address_to].append(tx)

                if (tx.address_from != cur_address) and (tx.address_from != ''):
                    if tx.address_from not in address_set:
                        to_add[tx.address_from].append(tx)

                internal_tx_hash = tx.tx_hash + tx.trace_id
                if (internal_tx_hash not in tx_hash_set) and (tx.address_from in visited) and (tx.address_to in visited):
                    tx_hash_set.add(internal_tx_hash)
                    yield tx
            
            for new_address, new_txs in to_add.items():
                address_set.add(new_address)
                queue.put((new_address, new_txs))
