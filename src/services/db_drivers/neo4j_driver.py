from typing import Any, Generator, Union
from neo4j import GraphDatabase

from models import DBDriverInterface
from models.graph import AddressNode, TransactionEdge, TransactionType


class Neo4jDriver(DBDriverInterface):
    def __init__(self, uri, user, password, *, buffer_size: int = 100, import_dir: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.edges = []
        self.buffer_size = buffer_size
        self.import_dir = import_dir

    def _close(self, *_):
        if self.driver is not None:
            self.driver.session().close()
            self.driver.close()

    def query(self, query: Any, **kwargs):
        return self.driver.session().run(query)

    def add_node(self, node: AddressNode):
        self.driver.session().run(
            f'CREATE (n:Address {{address: "{node.address}"}})'
        )

    def add_edge(self, edge: TransactionEdge):
        self.edges.append(edge)
        if len(self.edges) >= self.buffer_size:
            with open(self.import_dir + "/edges.csv", 'w') as f:
                f.write("from,to,tx_hash,tx_type,value\n")
                edge_: TransactionEdge = edge
                for edge_ in self.edges:
                    f.write(f"{edge_.address_from},{edge_.address_to},{edge_.tx_hash},{edge_.tx_type._name_},{edge_.value}\n")
                self.edges = []
        for tx_type in TransactionType._member_names_:
            self.driver.session().run(
                'LOAD CSV WITH HEADERS FROM "file:///edges.csv" AS csvLine ' +\
                'MATCH (from:Address {address: csvLine.from}), (to:Address {address: csvLine.to}) ' +\
                f'WHERE csvLine.tx_type = "{tx_type}" ' +\
                f'CREATE (from)-[r:{tx_type.upper()} {{tx_hash: csvLine.tx_hash, value: toInteger(csvLine.value)}}]->(to)'
            )

    def load(self, data_generator: Generator[Union[AddressNode, TransactionEdge], None, None]):
        for obj in data_generator:
            if isinstance(obj, AddressNode):
                self.add_node(obj)
            elif isinstance(obj, TransactionEdge):
                self.add_edge(obj)
            else:
                raise TypeError("load takes object of node and edge types from generator")
            