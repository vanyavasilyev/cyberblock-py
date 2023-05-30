from typing import Generator, Optional, Union
from queue import Queue
from collections import defaultdict

from models.graph import AddressNode, TransactionEdge, TransactionType
from .ethereum_scanner import EthereumScanner


class DirectedTreeScanner(EthereumScanner):
    def scan_from(self, address: str, max_inerations: Optional[int] = None,
                  startblock: int = 0, endblock: int = 99999999,
                  direction: str = "any", max_path: int = 5, min_tx_val_eth: float = 1e30, *args) -> Generator[Union[AddressNode, TransactionEdge], None, None]:
        address = address.lower()
        visited = {address, ''}
        tx_dict = defaultdict(list)
        address_set = set()
        tx_hash_set = set()

        def dfs(current_address: str, path_left: int):
            if max_inerations is not None and len(address_set) > max_inerations:
                return
            if path_left < 0:
                return
            visited.add(current_address)
            print(current_address)
            limit = None if current_address == address else 100
            offset = limit + 1 if limit else 10000
            for tx in self.get_txs_for_address(current_address, False, startblock,
                                                endblock, direction, limit, offset):
                if int(tx.value) < min_tx_val_eth * 1e18:
                    continue
                tx_dict[current_address].append(tx)
                if (tx.address_to != current_address) and (tx.address_to != ''):
                    if tx.address_to not in visited:
                        for obj in dfs(tx.address_to, path_left-1):
                            yield obj
                if (tx.address_from != current_address) and (tx.address_from != ''):
                    if tx.address_from not in visited:
                        for obj in dfs(tx.address_from, path_left-1):
                            yield obj

            if len(tx_dict[current_address]) == 0 and current_address != address:
                return

            for tx in self.get_txs_for_address(current_address, True, startblock,
                                                endblock, direction, limit, offset):
                if int(tx.value) == 0:
                    continue
                tx_dict[current_address].append(tx)
                if (tx.address_to != current_address) and (tx.address_to != ''):
                    if tx.address_to not in visited:
                        for obj in dfs(tx.address_to, path_left-1):
                            yield obj
                if (tx.address_from != current_address) and (tx.address_from != ''):
                    if tx.address_from not in visited:
                        for obj in dfs(tx.address_from, path_left-1):
                            yield obj

            node = AddressNode(
                address=current_address,
                scan_id=len(address_set)
            )
            yield node
            address_set.add(current_address)
            if len(address_set) % 20 == 0:
                print(f"Added {len(address_set)} nodes")

            tx: TransactionEdge = TransactionEdge('', '', '')
            for tx in tx_dict[current_address]:
                tx_hash = tx.tx_hash
                if tx.tx_type == TransactionType.INTERNAL:
                    tx_hash += tx.trace_id
                if tx_hash in tx_hash_set:
                    continue
                if tx.address_from not in address_set:
                    continue
                if tx.address_to not in address_set:
                    continue
                tx_hash_set.add(tx_hash)
                yield tx

        for obj in dfs(address, max_path):
            yield obj
