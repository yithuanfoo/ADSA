import sys

class UnionFind:
    def __init__(self, n):
        self.parent = []
        self.size = []
        for i in range(n):
            self.parent.append(i)
            self.size.append(1)

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)

        if x_root == y_root:
            return False
        
        if self.size[x_root] < self.size[y_root]:
            self.parent[x_root] = y_root
            self.size[y_root] = self.size[y_root] + self.size[x_root]
        else:
            self.parent[y_root] = x_root
            self.size[x_root] = self.size[x_root] + self.size[y_root]

        return True
    
def char_to_index(c):
    if c >= 'A' and c <= 'Z':
        return ord(c) - ord('A')
    else:
        return ord(c) - ord('a') + 26
    
def solve(country_str, build_str, destroy_str):

    country_rows = country_str.split(',')
    build_rows = build_str.split(',')
    destroy_rows = destroy_str.split(',')

    n = len(country_rows)

    country = []
    for row in country_rows:
        country_row = []
        for c in row:
            country_row.append(int(c))
        country.append(country_row)

    build = []
    for row in build_rows:
        build_row = []
        for c in row:
            build_row.append(char_to_index(c))
        build.append(build_row)

    destroy = []
    for row in destroy_rows:
        destroy_row = []
        for c in row:
            destroy_row.append(char_to_index(c))
        destroy.append(destroy_row)

    edges = []
    destroy_cost = 0

    for i in range(n):
        for j in range(i + 1, n):
            if country[i][j] == 1:
                edges.append((i, j, -destroy[i][j]))
                destroy_cost = destroy_cost + destroy[i][j]
            else: 
                edges.append((i, j, build[i][j]))

    edges.sort(key=lambda edge: edge[2])

    union_find = UnionFind(n)
    mst_cost = 0

    for edge in edges:
        u = edge[0]
        v = edge[1]
        cost = edge[2]

        if union_find.union(u, v):
            mst_cost = mst_cost + cost

    total_cost = destroy_cost + mst_cost
    return total_cost

if __name__ == "__main__":
    input_line = sys.stdin.readline().strip()
    string_part = input_line.split()

    country_str = string_part[0]
    build_str = string_part[1]
    destroy_str = string_part[2]

    result = solve(country_str, build_str, destroy_str)
    print(result)



