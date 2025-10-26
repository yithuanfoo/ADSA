import sys

# Class for Union Find data structure
class UnionFind:
    def __init__(self, n): 
        self.parent = []    # Stores the parent of each element
        self.size = []  # Stores the size of each set
        for i in range(n):  # Initialise each element to be its own parent
            self.parent.append(i)   
            self.size.append(1) # Initialise size of each set to 1
    
    # Function to find root of the set in which the element x is present
    def find(self, x):
        if self.parent[x] != x: # If x is not its own parent
            self.parent[x] = self.find(self.parent[x])  # Recursively find the root and compress the path
        return self.parent[x]  
    
    # Function to join two sets containing x and y
    def union(self, x, y):
        x_root = self.find(x)   # Find root of x
        y_root = self.find(y)   # Find root of y

        if x_root == y_root:    # If both elements have the same root, they are already in the same set
            return False
        
        if self.size[x_root] < self.size[y_root]:   # If size of x's set is less than size of y's set
            self.parent[x_root] = y_root    # Make y's root the parent of x's root
            self.size[y_root] = self.size[y_root] + self.size[x_root]   # Update y's set size
        else:   # If size of y's set is less than or equal to size of x's set
            self.parent[y_root] = x_root    # Make x's root the parent of y's root 
            self.size[x_root] = self.size[x_root] + self.size[y_root]   # Update x's set size
        return True

# Helper function to convert character to index
def char_to_index(c):
    if c >= 'A' and c <= 'Z':   # If character is uppercase
        return ord(c) - ord('A')    # Convert to index 0 - 25
    else:   # If character is lowercase
        return ord(c) - ord('a') + 26   # Convert to index 26 - 51

# Main function to solve the problem    
def solve(country_str, build_str, destroy_str):
    country_rows = country_str.split(',')   # Split country string into rows
    build_rows = build_str.split(',')   # Split build string into rows
    destroy_rows = destroy_str.split(',')   # Split destroy string into rows

    n = len(country_rows)   # Number of cities

    # Build a 2D array for country, which stores which roads currently exist
    country = []    # Initialise empty country array
    for row in country_rows:    # Iterate through each row
        country_row = []    # Initialise empty row
        for c in row:   # Iterate through each character in the row
            country_row.append(int(c))  # Convert character to integer and append to row
        country.append(country_row) # Append row to country array
    
    # Build a 2D array for build costs
    build = []  
    for row in build_rows:  # Iterate through each row
        build_row = []  # Initialise empty row
        for c in row:   # Iterate through each character in the row
            build_row.append(char_to_index(c))  # Convert character to index and append to row
        build.append(build_row) # Append row to build array

    # Build a 2D array for destroy costs
    destroy = []
    for row in destroy_rows:    # Iterate through each row
        destroy_row = []    # Initialise empty row
        for c in row:   # Iterate through each character in the row
            destroy_row.append(char_to_index(c))    # Convert character to index and append to row
        destroy.append(destroy_row) # Append row to destroy array

    edges = []  # Initialise empty list for edges
    destroy_cost = 0    # Track total cost of destroying roads

    for i in range(n):  # Interate through each city
        for j in range(i + 1, n):   # Iterate through each city j where j > i to avoid duplicates
            if country[i][j] == 1:  # If a road exists between city i and city j
                edges.append((i, j, -destroy[i][j]))    # Add edge with negative destroy cost
                destroy_cost = destroy_cost + destroy[i][j] # Add to total destroy cost
            else: 
                edges.append((i, j, build[i][j]))   # If no road exists, add edge with build cost

    edges.sort(key=lambda edge: edge[2])    # Sort edges by cost in ascending order, first step of Kruskal's algorithm

    # Apply Kruskal's algorithm to find the MST
    union_find = UnionFind(n)   # Initialise Union Find for n cities
    mst_cost = 0    # Total cost of the MST

    for edge in edges:  # Iterate through each edge
        u = edge[0] # First city of the edge
        v = edge[1] # Second city of the edge
        cost = edge[2]  # Cost of the edge

        if union_find.union(u, v):  # If u and v are not already connected
            mst_cost = mst_cost + cost  # Add edge cost to MST total

    total_cost = destroy_cost + mst_cost    # Total cost of reconstructing the roads
    return total_cost

# Main Code
if __name__ == "__main__":
    input_line = sys.stdin.readline().strip()   # Read input line
    string_part = input_line.split()    # Split input line into three parts

    country_str = string_part[0]    # Country string
    build_str = string_part[1]  # Build string
    destroy_str = string_part[2]    # Destroy string

    result = solve(country_str, build_str, destroy_str) # Solve the problem
    print(result)   # Print the result



