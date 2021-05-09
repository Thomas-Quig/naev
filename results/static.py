f = open("staticdata.txt","r").read().splitlines()
versions = []

# Dump every version
for line in f:
    line = line.split(' ')
    if line[0] not in versions:
        versions.append(line[0])
versions.append('2.0.0')
heatmap = [[0] * len(versions) for _ in range(len(versions))]
print(heatmap)
print(versions)

for line in f:
    line = line.split(' ')
    heatmap[versions.index(line[0])][versions.index(line[2][:-1])] = line[3]

print(heatmap)

out = open('heatmap.csv','w')
out.write(', ')
for v in versions:
    out.write(v + ', ')
out.write('\n')

i = 0
for row in heatmap:
    out.write(versions[i] + ', ')
    for val in row:
        out.write(str(val) + ', ')
    i += 1
    out.write('\n')