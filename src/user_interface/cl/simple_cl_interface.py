from models import AnalyzerInterface


class CLInterface:
    def __init__(self, analyzer: AnalyzerInterface, safe=True) -> None:
        self.analyzer = analyzer
        self.safe = safe

    def run(self):
        try:
            while True:
                if self.safe:
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
                else:
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
        except KeyboardInterrupt:
            print("\nExit")
            return
