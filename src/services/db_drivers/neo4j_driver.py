from typing import Any, Generator, Union
from neo4j import GraphDatabase

from models import DBDriverInterface
from models.graph import AddressNode, TransactionEdge


class Neo4jDriver(DBDriverInterface):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

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
        properties = \
            f'tx_hash:"{edge.tx_hash}", ' +\
            f'value:"{edge.value}"'
        self.driver.session().run(
            f'MATCH (a:Address), (b:Address) WHERE a.address="{edge.address_from}" AND b.address="{edge.address_to}" ' +\
            f'CREATE (a)-[r:{edge.tx_type._name_} {{{properties}}}]->(b)'
        )

    def load(self, data_generator: Generator[Union[AddressNode, TransactionEdge], None, None]):
        for obj in data_generator:
            if isinstance(obj, AddressNode):
                self.add_node(obj)
            elif isinstance(obj, TransactionEdge):
                self.add_edge(obj)
            else:
                raise TypeError("load takes object of node and edge types from generator")
            