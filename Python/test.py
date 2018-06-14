import copy

dimensions = [2, 3, 4]
time = 1

map = [
    [

        [
            [
                [0 for _ in range(dimensions[2])]
            ] for _ in range(dimensions[1]) 
        ] for _ in range(dimensions[0])
    ] for _ in range(time)
]

print("map", map)

# the number of cells contained in all dimensions up to the index
CPD = [1]
for i in range(len(dimensions)):
    CPD.append(CPD[i] * dimensions[i])

CPD.append(CPD[-1] * time)

print("CPD:", CPD)

cells = [1 for _ in range(CPD[-1])]

indices = [[] for _ in range(CPD[-1])]

for d in range(len(dimensions)):
    for c in range(CPD[-1]):
        indices[c].append(c // CPD[d] % dimensions[d])

for c in range(CPD[-1]):
    indices[c].insert(0, c // CPD[-2])

print("indices:", indices)

for c in range(CPD[-1]):
    item = copy.copy(map[indices[c][0]])
    depth = 1
    while depth < len(indices[c]):
        item = copy.copy(item[indices[c][depth]])
        depth += 1
    
    item = cells[c]

print("map:", map)

