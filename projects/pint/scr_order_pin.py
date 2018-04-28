
pirm = {194147433914509093: 0.4825663256996754,
        194147433920742213: 0.1230036005529672,
        194147433920742214: 0.1237095350789634,
        194147433920742229: 0.12439978217104856}

ordered = []
for p in pirm.keys():
    ordered.append((p, pirm[p]))
print("1: {}".format(ordered))

ordered.sort(key=lambda x: x[1])
print("2: {}".format(ordered))

ordered.reverse()
print("3: {}".format(ordered))

ordered = [id for id, s in ordered]
print("4: {}".format(ordered))
