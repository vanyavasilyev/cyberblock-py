import json
from typing import List, Optional, Any

from models import ScannerInterface, DBDriverInterface, AnalyzerInterface, AddressNode, TransactionEdge
from .query import Neo4jQuery


class Neo4jAnalyzer(AnalyzerInterface):
    def __init__(self, db_driver: DBDriverInterface, scanners: List[ScannerInterface],
                 queries_path: str):
        self.db_driver = db_driver
        self.scanners = scanners
        self.active_scanner = self.scanners[0]

        self.queries = dict()
        with open(queries_path, 'r') as f:
            queries_list = json.load(f)
            for query_dict in queries_list:
                self.queries[query_dict['name']] = Neo4jQuery(
                    name=query_dict['name'],
                    arg_names=query_dict['arg_names'],
                    query_str=query_dict['query_str']
                )

    def _scan_from(self, address: str, max_iterations: Any,
                   startblock: int = 9000000, endblock: int = 99999999): 
        self.db_driver.load(self.active_scanner.scan_from(address,
                                                          int(max_iterations),
                                                          int(startblock),
                                                          int(endblock)))

    def _db_response_handler(self, response):
        as_list = response.values()
        res = []
        for obj in as_list:
            properties = obj[0]._properties
            if 'address' in properties:
                res.append(AddressNode(properties['address']))
            if 'tx_hash' in properties:
                res.append(TransactionEdge(properties['tx_hash'], '', ''))
        return res

    def run_command(self, command: str, args: Any):
        if command == 'scan':
            self._scan_from(*args)
            return "Finished scan"
        if command not in self.queries:
            return "No such command"
        res = self.db_driver.query(self.queries[command].format_query(args))
        return self._db_response_handler(res)
