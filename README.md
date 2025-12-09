# Sequence Alignment: Basic DP & Space-Efficient Divide-and-Conquer

This project implements two algorithms for optimal DNA sequence alignment:

1. **Basic Dynamic Programming (DP)** – classical Needleman–Wunsch algorithm  
2. **Space-Efficient Divide-and-Conquer Alignment** – Hirschberg’s algorithm

The programs read specially formatted input strings, expand them, compute optimal alignment with a given cost model, and output both the alignment and performance statistics.

---

## 📁 Folder Structure

```
├── Datapoints/        
├── Results/           
├── efficient.py      
├── basic.py         
├── summary.py        
└── README.md
```

---

## 🔧 Usage

### Run the Efficient (Divide-and-Conquer) Algorithm
```
./efficient.py <input_file> <output_file>
```

### Run the Basic DP Algorithm
```
./basic.py <input_file> <output_file>
```

If your system uses `python` instead of `python3`, simply replace it.

---

## 📤 Output Format

Each output file (e.g., `out_in1.txt`) contains:

```
<minimum alignment cost>
<aligned sequence 1>
<aligned sequence 2>
<CPU time in ms>
<memory usage in KB>
```

