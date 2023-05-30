from utils import contract_erc20_events
from collections import defaultdict
from itertools import product
from sklearn.cluster import AgglomerativeClustering
import numpy as np


if __name__ == '__main__':
    RAILGUN_ADDRESS = "0xFA7093CDD9EE6932B4eb2c9e1cde7CE00B1FA4b9"
    RESULT_FILENAME = "railgun_balances.txt"
    EPS = 0.02
    TX_INFO = False
    token_to_events = defaultdict(list)
    for event in contract_erc20_events(RAILGUN_ADDRESS):
        token_to_events[event["contractAddress"].lower()].append(event)

    print(f"{len(token_to_events)} tokens found")
    with open(RESULT_FILENAME, 'w') as f:
        for token in token_to_events:
            f.write(f"Token {token}:\n")
            address_to_interaction_value = defaultdict(int)
            address_to_txs = defaultdict(set)
            for event in token_to_events[token]:
                if event["from"].lower() == RAILGUN_ADDRESS.lower():
                    address_to_interaction_value[event["to"]] += int(event["value"])
                    address_to_txs[event["to"]].add(event["hash"])
                else:
                    address_to_interaction_value[event["from"]] -= int(event["value"])
                    address_to_txs[event["from"]].add(event["hash"])

            values = []
            ind_to_address = []
            for address, value in address_to_interaction_value.items():
                ind_to_address.append(address)
                values.append(np.log(np.abs(value) + 1e-8))

            if len(values) < 2:
                continue
            values = np.array(values, dtype=np.float32).reshape(-1, 1)
            ind_to_address = np.array(ind_to_address)

            model = AgglomerativeClustering(n_clusters=None, linkage="single", distance_threshold=np.log(1+EPS))
            groups = model.fit_predict(values)
            for group in np.unique(groups):
                addresses = ind_to_address[groups == group]
                pos = []
                neg = []
                for address in addresses:
                    if address_to_interaction_value[address] > 0:
                        pos.append(address)
                    else:
                        neg.append(address)
                if len(pos) * len(neg) > 0:
                    if len(pos) * len(neg) == 1:
                        f.write("Possible clear match:\n")
                    else:
                        f.write("Possible matches:\n")
                    spenders = []
                    for address in neg:
                        spenders.append(f"{address}({-address_to_interaction_value[address]})")
                    f.write(f"Spenders: {', '.join(spenders)}\n")

                    receivers = []
                    for address in pos:
                        receivers.append(f"{address}({address_to_interaction_value[address]})") 
                    f.write(f"Receivers: {', '.join(receivers)}\n\n")


            f.write("\n\n")
            
