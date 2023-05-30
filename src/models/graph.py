from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict


@dataclass
class AddressNode:
    address: str
    balance: Optional[float] = None
    is_contract: Optional[bool] = None
    first_tx_date: Optional[int] = None
    last_tx_date: Optional[int] = None
    number_of_outgoing_txs : int = 0
    number_of_incoming_txs: int = 0
    scan_id: Optional[int] = None



class TransactionType(Enum):
    CREATE = 0
    CALL = 1
    SEND = 2
    INTERNAL = 3


@dataclass
class TransactionEdge:
    tx_hash: str
    address_from: str
    address_to: str
    trace_id: str = ''
    date: Optional[int] = None
    tx_type: Optional[TransactionType] = None
    value: Optional[float] = None
    block: Optional[int] = None
    gas: Optional[int] = None
    gas_price: Optional[int] = None
    tx_args: Dict = field(default_factory=dict)
