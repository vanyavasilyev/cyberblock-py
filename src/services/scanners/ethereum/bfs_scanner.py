from typing import Generator, Optional, Union
from queue import Queue
from collections import defaultdict

from models.graph import AddressNode, TransactionEdge
from .ethereum_scanner import EthereumScanner


class BFSEthScanner(EthereumScanner):
    def scan_from(self, address: str, max_inerations: Optional[int] = None
                  ) -> Generator[Union[AddressNode, TransactionEdge], None, None]:
        iterations_left = max_inerations if max_inerations else -1

        queue = Queue()
        queue.put((address, []))

        visited = set()
        visited.add('')

        address_set = set()
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
                yield tx

            txs = self.get_txs_for_address(cur_address)
            to_add = defaultdict(list)
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
            
            for new_address, new_txs in to_add.items():
                address_set.add(new_address)
                queue.put((new_address, new_txs))
