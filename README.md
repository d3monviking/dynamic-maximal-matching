# Dynamic Maximal Matching (Fully Dynamic Graph)

This project implements a **fully dynamic maximal matching algorithm** based on:

> *Baswana, Gupta, Sen — “Fully dynamic maximal matching in O(log n) update time”*

Specifically, this implementation follows **Section 4** of the paper, which achieves:

> **Expected amortized O(√n) time per update**

---

## Features

- Supports **dynamic graph updates**
  - Edge insertion
  - Edge deletion
- Maintains a **maximal matching**
- Uses:
  - **Randomized settling** for high-degree vertices
  - **Naive settling** for low-degree vertices
- Real-time **graph visualization**
- Dual view:
  - Full graph (with matching highlighted)
  - Matching-only graph

---

## Algorithm Overview

The algorithm maintains:

- A matching `M`
- A partition of vertices into:
  - **Level 0** (low degree)
  - **Level 1** (high degree)

### Key Invariants

1. Every **level 1 vertex is matched**
2. Every **free level 0 vertex has all neighbors matched**
3. **Both endpoints of every matched edge are at the same level**

---

## Data Structures Used

| Concept | Implementation |
|--------|----------------|
| Graph | Adjacency list (`list[set]`) |
| Owned edges \(O_u\) | `list[set]` |
| Matching | `mate[]` array |
| Levels | `level[]` array |
| Visualization | NetworkX + Matplotlib |

---

## Visualization

- Built using:
  - NetworkX
  - Matplotlib
- Two views:
  - **Left:** Full graph (matching edges in red)
  - **Right:** Matching-only graph
- Node colors:
  - 🟢 Green → Level 1 (high-degree, always matched)
  - 🔵 Blue → Level 0

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install networkx matplotlib
```

Run the python code by
```bash
python dynamic_matching.py
```

Input format
```
n q
<operation u v>
<operation u v>
```

where n is the number of nodes in our graph and q denotes the number of updates. Replace operation with 'add' or 'delete' to add or delete an edge, respectively. 

## Input Files
You can use the following input files instead of manually adding test cases.
- [input_1.txt](input_1.txt)
- [input_2.txt](input_2.txt)
- [input_3.txt](input_3.txt)

To directly feed in the input, run the following command
```bash
python3 dynamic_matching.py < input_d.txt
```
Replace d with 1, 2, or 3.
