import requests


def contract_erc20_events(address: str,
                 api_key="MTH46DY922UPAM5NQQ9PT45JKZAEAPADVF",
                 start_block: int = 0,
                 end_block: int = 99999999):
    while True:
        url = f'''
            https://api.etherscan.io/api
            ?module=account
            &action=tokentx
            &address={address}
            &startblock={start_block}
            &endblock={end_block}
            &sort=asc
            &apikey={api_key}
        '''
        url = "".join(url.split())
        errors_in_row = 0
        try:
            resp = requests.get(url).json()['result']
            for tx in resp:
                yield tx
            

            if len(resp) < 10000:
                break
            start_block = resp[-1]['blockNumber']
            if start_block > end_block:
                    break
            errors_in_row = 0
        except Exception as e:
            errors_in_row += 1
            if errors_in_row > 5:
                break


def contract_txs(address: str,
                 api_key="MTH46DY922UPAM5NQQ9PT45JKZAEAPADVF",
                 start_block: int = 0,
                 end_block: int = 99999999):
    while True:
        url = f'''
            https://api.etherscan.io/api
            ?module=account
            &action=txlist
            &address={address}
            &startblock={start_block}
            &endblock={end_block}
            &sort=asc
            &apikey={api_key}
        '''
        url = "".join(url.split())
        errors_in_row = 0
        try:
            resp = requests.get(url).json()['result']
            for tx in resp:
                yield tx
            

            if len(resp) < 10000:
                break
            start_block = resp[-1]['blockNumber']
            if start_block > end_block:
                    break
            errors_in_row = 0
        except Exception as e:
            errors_in_row += 1
            if errors_in_row > 5:
                break
