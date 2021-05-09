import json

compatTable = json.loads(open("naev-npm-bigresults.json","r").read())
out = open("graph.txt","w")
for v in compatTable:
    for c in compatTable[v]:
        out.write(v + ' ' + c + '\n')