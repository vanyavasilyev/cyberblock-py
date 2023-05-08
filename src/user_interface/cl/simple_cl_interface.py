from models import AnalyzerInterface


class CLInterface:
    def __init__(self, analyzer: AnalyzerInterface) -> None:
        self.analyzer = analyzer

    def run(self):
        try:
            while True:
                try:
                    inp = input('%>').split()
                    if len(inp) == 0:
                        continue
                    command = inp[0]
                    args = [] if len(inp) == 1 else inp[1:]
                    res = self.analyzer.run_command(command, args)
                    if isinstance(res, list):
                        for obj in res:
                            print(obj)
                    else:
                        print(res)
                except Exception as e:
                    print("Error")
                    print(e)
        except KeyboardInterrupt:
            print("\nExit")
            return
