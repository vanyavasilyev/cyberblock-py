from typing import List, Union


class Neo4jQuery:
    def __init__(self, name: str, arg_names: List[str], query_str: str):
        self.name = name
        self.arg_names = arg_names
        self.query_str = query_str

    def format_query(self, args: Union[list, dict]) -> str:
        if not args:
            return self.query_str
        if isinstance(args, list):
            res = self.query_str.format(*args)
            return res
        args_list = []
        for arg_name in self.arg_names:
            args_list.append(args[arg_name])
        return self.query_str.format(*args)
