import random
import math
import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class DynamicMatching:
    def __init__(self, n):
        self.n = n
        self.adj = [set() for _ in range(n)]
        self.owned = [set() for _ in range(n)]
        self.level = [0] * n
        self.mate = [-1] * n
        self.threshold = int(math.sqrt(n))
        self.init_visualization()

    # VISUAL INIT
    def init_visualization(self):
        self.G = nx.Graph()
        self.pos = None    
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # MATCHING OPS
    def match(self, u, v):
        # remove old matches
        if self.mate[u] != -1:
            old = self.mate[u]
            self.mate[old] = -1
    
        if self.mate[v] != -1:
            old = self.mate[v]
            self.mate[old] = -1
    
        lvl = max(self.level[u], self.level[v])
        self.level[u] = lvl
        self.level[v] = lvl
    
        self.mate[u] = v
        self.mate[v] = u

    def unmatch(self, u, v):
        self.mate[u] = -1
        self.mate[v] = -1

    # INSERT EDGE 
    def insert_edge(self, u, v):
        print(f"\nINSERT ({u}, {v})")

        self.adj[u].add(v)
        self.adj[v].add(u)

        if self.level[u] == 1 or self.level[v] == 1:
            if self.level[u] == 1:
                self.owned[u].add(v)
            else:
                self.owned[v].add(u)
        else:         
            self.handle_insertion(u, v)


    def handle_insertion(self, u, v):
        self.owned[u].add(v)
        self.owned[v].add(u)
    
        if self.mate[u] == -1 and self.mate[v] == -1:
            self.match(u, v)
    
        if len(self.owned[v]) > len(self.owned[u]):
            u, v = v, u
    
        if len(self.owned[u]) == self.threshold:
            old_u_mate = self.mate[u]
    
            for w in list(self.owned[u]):
                self.owned[w].discard(u)
    
            x = self.random_settle(u)
    
            if x != -1:
                self.naive_settle(x)
    
            if old_u_mate != -1:
                self.naive_settle(old_u_mate)

    # RANDOM SETTLE
    def random_settle(self, u):
        if not self.owned[u]:
            return -1
    
        y = random.choice(list(self.owned[u]))
        # store old mate of y
        old_mate = self.mate[y]
    
        for w in list(self.owned[y]):
            self.owned[w].discard(y)    
    
        # free u if needed
        if self.mate[u] != -1:
            old_u = self.mate[u]
            self.unmatch(u, old_u)
    
        # free y if needed
        if old_mate != -1:
            self.unmatch(y, old_mate)
    
        # match u with y
        self.match(u, y)
    
        self.level[u] = 1
        self.level[y] = 1
    
        return old_mate 

    # NAIVE SETTLE
    def naive_settle(self, u):
        if self.mate[u] != -1:
            return
    
        for v in self.owned[u]:
            if self.mate[v] == -1:
                self.match(u, v)
                return

    # DELETE EDGE
    def delete_edge(self, u, v):
        print(f"\nDELETE ({u}, {v})")

        self.adj[u].discard(v)
        self.adj[v].discard(u)

        self.owned[u].discard(v)
        self.owned[v].discard(u)

        if self.mate[u] != v:
            return

        self.unmatch(u, v)

        if(max(self.level[u], self.level[v]) == 0):
            self.naive_settle(u)
            self.naive_settle(v)
        else:
            self.handle_deletion(u)
            self.handle_deletion(v)

    # HANDLE DELETION
    def handle_deletion(self, u):
        for w in list(self.owned[u]):
            if self.level[w] == 1:
                self.owned[w].add(u)
                self.owned[u].discard(w)

        if len(self.owned[u]) >= self.threshold:
            x = self.random_settle(u)
            if x != -1:
                self.naive_settle(x)
        else:
            self.level[u] = 0
            for w in list(self.owned[u]):
                if self.level[w] == 0:
                    self.owned[w].add(u)
            self.naive_settle(u)
            
            for w in list(self.owned[u]):
                if len(self.owned[u]) == self.threshold:
                    x = self.random_settle(w)
                    if x != -1:
                        self.naive_settle(x)


    # VISUALIZATION
    def update_visualization(self):
        self.ax1.clear()
        self.ax2.clear()
    
        self.G.clear()
    
        # add all nodes
        self.G.add_nodes_from(range(self.n))
    
        # add edges
        for u in range(self.n):
            for v in self.adj[u]:
                if u < v:
                    self.G.add_edge(u, v)
    
        # stable layout
        if self.pos is None:
            self.pos = nx.spring_layout(self.G, k=1.5, seed=42)
    
        # node colors
        node_colors = [
            "green" if self.level[i] == 1 else "lightblue"
            for i in range(self.n)
        ]
    
        # LEFT: FULL GRAPH
        nx.draw(
            self.G, self.pos,
            ax=self.ax1,
            with_labels=True,
            node_color=node_colors,
            node_size=500
        )
    
        # matching edges
        matching_edges = []
        visited = set()
        for u in range(self.n):
            v = self.mate[u]
            if v != -1 and (v, u) not in visited:
                matching_edges.append((u, v))
                visited.add((u, v))
    
        nx.draw_networkx_edges(
            self.G, self.pos,
            edgelist=matching_edges,
            edge_color="red",
            width=3,
            ax=self.ax1
        )
    
        self.ax1.set_title("Full Graph (Matching in Red)")
    
        # RIGHT: MATCHING ONLY
        M = nx.Graph()
        M.add_nodes_from(range(self.n))
        M.add_edges_from(matching_edges)
    
        nx.draw(
            M, self.pos,
            ax=self.ax2,
            with_labels=True,
            node_color=node_colors,
            node_size=600,
            edge_color="red",
            width=3
        )
    
        self.ax2.set_title("Maximal Matching Only")
    
        plt.pause(4)
        
    def print_state(self):
        print("\nCurrent Matching:")
        for u in range(self.n):
            v = self.mate[u]
            if v != -1 and u < v:
                print(f"{u} - {v}")

        print("Levels:", self.level)

# DRIVER
def run():
    import sys

    data = sys.stdin.read().strip().split()
    
    n = int(data[0])
    q = int(data[1])
    
    dm = DynamicMatching(n)

    idx = 2
    for _ in range(q):
        op = data[idx]
        u = int(data[idx + 1])
        v = int(data[idx + 2])
        idx += 3

        if op == "add":
            dm.insert_edge(u, v)
        else:
            dm.delete_edge(u, v)

        dm.print_state()
        dm.update_visualization()

    print("Done.")
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    run()