from services import DirectedTreeScanner, BFSEthScanner, Neo4jDriver, Neo4jAnalyzer
from user_interface.cl.simple_cl_interface import CLInterface
from config.neo4j_config import Neo4jConfig


if __name__ == '__main__':
    with open('../configs/neo4j_analyzer_config.json', 'r') as f:
        data = f.read()
        cfg: Neo4jConfig = Neo4jConfig.from_json(data)
    scanner = DirectedTreeScanner(cfg.etherscan_api_key)
    driver = Neo4jDriver(*cfg.neo4j_driver_args, import_dir=cfg.neo4j_import_dir, buffer_size=1)
    analyzer = Neo4jAnalyzer(driver, [scanner], cfg.queries_path)
    CLInterface(analyzer, True).run()
    