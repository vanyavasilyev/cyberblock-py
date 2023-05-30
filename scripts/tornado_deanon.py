from utils import contract_txs
from collections import defaultdict
from itertools import product
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pickle


if __name__ == '__main__':
    TORNADO_ADDRESS = "0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3c2936"
    RESULT_FILENAME = "tornado_deanon.txt"
    TIME_DELTA_SECONDS = 60

    all_txs = [tx for tx in contract_txs(TORNADO_ADDRESS)]
    groups = []
    all_txs = np.array(all_txs)
    timestamps = np.array([int(tx["timeStamp"]) for tx in all_txs]).reshape(-1, 1)
    model = AgglomerativeClustering(n_clusters=None, linkage="single", distance_threshold=TIME_DELTA_SECONDS)
    groups = model.fit_predict(timestamps)

    with open(RESULT_FILENAME, 'w') as f:
        for group in np.unique(groups):
            txs = all_txs[groups == group]
            if len(txs) > 1:
                tx_data = []
                max_wihdraw_time = 0
                min_deposit_time = 1e20
                for tx in txs:
                    function_name = tx["functionName"].split("(")[0]
                    tx_data.append(f"{function_name}:{tx['hash']}({tx['timeStamp']})")
                    if function_name == "withdraw":
                        max_wihdraw_time = max(max_wihdraw_time, int(tx['timeStamp']))
                    if function_name == "deposit":
                        min_deposit_time = min(min_deposit_time, int(tx['timeStamp']))
                if min_deposit_time > max_wihdraw_time:
                    continue
                f.write(f"Some transactions at the same time: {', '.join(tx_data)}\n")

