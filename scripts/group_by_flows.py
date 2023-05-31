import pandas
import numpy as np
from sklearn.cluster import AgglomerativeClustering

INGOING_FLOWS_FILE = "results/flows/ingoing_flows.csv"
OUTGOING_FLOWS_FILE = "results/flows/outgoing_flows.csv"
RESULT_FILENAME = "results/flows/groups.txt"
EPS = 0.03
AVG_FEE = 0.02

inf = pandas.read_csv(INGOING_FLOWS_FILE)
outf = pandas.read_csv(OUTGOING_FLOWS_FILE)

ind_to_address = []
values = []

for row in inf.iterrows():
    mf = row[1]["n.mf"]
    address = row[1]["n.address"]
    values.append(float(mf))
    ind_to_address.append((address, "in", mf))

for row in outf.iterrows():
    mf = row[1]["n.mf"]
    address = row[1]["n.address"]
    values.append(float(mf) * (1 + AVG_FEE))
    ind_to_address.append((address, "out", mf))   

ind_to_address = np.array(ind_to_address)

model = AgglomerativeClustering(n_clusters=None, linkage="complete", distance_threshold=np.log(1+EPS)) 
groups = model.fit_predict(np.log(np.array(values) + 1e-10).reshape(-1, 1))
with open(RESULT_FILENAME, "w") as f:
    group_data = []
    for group in np.unique(groups):
        addresses = ind_to_address[groups == group]
        in_ = []
        out_ = []
        for address, direction, mf in addresses:
            if direction == "in":
                in_.append((address, direction, mf))
            else:
                out_.append((address, direction, mf))
        if len(in_) > 0 and len(out_) > 0:
            if in_[0][0] == out_[0][0]:
                continue
            s = f"Group with value ~{in_[0][2]}\n"
            s += f"Potential spenders: \n"
            for spender in in_:
                s += f"{spender[0]}: {spender[2]}\n"
            s += f"Potential receivers: \n"
            for receiver in out_:
                s += f"{receiver[0]}: {receiver[2]}\n"
            s +="\n"
            group_data.append((float(in_[0][2]), s))
    
    c = 0
    for val, s in sorted(group_data, reverse=True):
        if val > 2:
            c += val
        f.write(s)
