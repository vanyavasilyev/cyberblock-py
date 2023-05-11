import dataclasses
from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
@dataclasses.dataclass
class Neo4jConfig:
    etherscan_api_key: str
    neo4j_driver_args: List[str]
    queries_path: str
    neo4j_import_dir: str
