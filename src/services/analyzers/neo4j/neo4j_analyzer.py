import json
from typing import List, Optional, Any

from models import ScannerInterface, DBDriverInterface, AnalyzerInterface
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

    def _scan_from(self, address: str, max_iterations: Optional[int] = None):
        self.db_driver.load(self.active_scanner.scan_from(address, max_iterations))

    def run_command(self, command: str, args: Any):
        if command == 'scan':
            self._scan_from(*args)
            return "Finished scan"
        if command not in self.queries:
            return "No such command"
        res = self.db_driver.query(self.queries[command].format_query(args))
        return list(res)
