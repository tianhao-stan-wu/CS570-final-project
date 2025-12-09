import sys
import time
import psutil

delta = 30  # Gap penalty

# Mismatch costs
alpha = {
    'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94},
    'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48},
    'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
    'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0}
}


# Input string generation
def generate_string(base_str, indices):
    current_str = base_str
    for idx in indices:
        current_str = current_str[:idx+1] + current_str + current_str[idx+1:]
    return current_str


def parse_input(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Parse first string data
    s1_base = lines[0]
    s1_indices = []
    curr_idx = 1
    while curr_idx < len(lines) and lines[curr_idx].replace('-', '').isdigit():
        s1_indices.append(int(lines[curr_idx]))
        curr_idx += 1

    # Parse second string data
    s2_base = lines[curr_idx]
    curr_idx += 1
    s2_indices = []
    while curr_idx < len(lines) and lines[curr_idx].replace('-', '').isdigit():
        s2_indices.append(int(lines[curr_idx]))
        curr_idx += 1

    return generate_string(s1_base, s1_indices), generate_string(s2_base, s2_indices)


# Alignment utilities
def get_mismatch_cost(c1, c2):
    return alpha[c1][c2]


def space_efficient_score(seq1, seq2):
    n = len(seq2)
    prev = [j * delta for j in range(n + 1)]
    curr = [0] * (n + 1)

    for c1 in seq1:
        curr[0] = prev[0] + delta
        for j in range(1, n + 1):
            c2 = seq2[j-1]
            cost_match = prev[j-1] + get_mismatch_cost(c1, c2)
            cost_delete = prev[j] + delta
            cost_insert = curr[j-1] + delta
            curr[j] = min(cost_match, cost_delete, cost_insert)
        prev[:] = curr[:]

    return prev


# Basic DP alignment
def basic_alignment_solver(seq1, seq2):
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Init
    for i in range(m + 1):
        dp[i][0] = i * delta
    for j in range(n + 1):
        dp[0][j] = j * delta

    # Fill
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_match = dp[i-1][j-1] + get_mismatch_cost(seq1[i-1], seq2[j-1])
            cost_delete = dp[i-1][j] + delta
            cost_insert = dp[i][j-1] + delta
            dp[i][j] = min(cost_match, cost_delete, cost_insert)

    # Backtrack
    align1 = []
    align2 = []
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + get_mismatch_cost(seq1[i-1], seq2[j-1]):
            align1.append(seq1[i-1])
            align2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + delta:
            align1.append(seq1[i-1])
            align2.append('_')
            i -= 1
        else:
            align1.append('_')
            align2.append(seq2[j-1])
            j -= 1

    return "".join(reversed(align1)), "".join(reversed(align2)), dp[m][n]


# Divide and Conquer
def divide_and_conquer_alignment(seq1, seq2):
    m, n = len(seq1), len(seq2)

    # base cases
    if m == 0:
        return "_" * n, seq2, n * delta
    if n == 0:
        return seq1, "_" * m, m * delta
    if m == 1 or n == 1:
        return basic_alignment_solver(seq1, seq2)

    mid = m // 2


    score_l = space_efficient_score(seq1[:mid], seq2)
    score_r = space_efficient_score(seq1[mid:][::-1], seq2[::-1])
    score_r = score_r[::-1] 

    # Find k that minimizes split
    min_cost = float('inf')
    split_k = 0
    for k in range(n + 1):
        cost = score_l[k] + score_r[k]
        if cost < min_cost:
            min_cost = cost
            split_k = k

    # Recursive solve
    left_align = divide_and_conquer_alignment(seq1[:mid], seq2[:split_k])
    right_align = divide_and_conquer_alignment(seq1[mid:], seq2[split_k:])

    total_cost = left_align[2] + right_align[2]

    return left_align[0] + right_align[0], left_align[1] + right_align[1], total_cost


# Memory measurement
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    return int(memory_info.rss / 1024)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 efficient.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        s1, s2 = parse_input(input_path)
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    start_time = time.time()
    mem1 = process_memory()
    aligned_s1, aligned_s2, min_cost = divide_and_conquer_alignment(s1, s2)
    end_time = time.time()
    mem2 = process_memory()

    time_taken_ms = (end_time - start_time) * 1000
    memory_used_kb = mem2 - mem1

    with open(output_path, 'w') as f:
        f.write(f"{min_cost}\n")
        f.write(f"{aligned_s1}\n")
        f.write(f"{aligned_s2}\n")
        f.write(f"{time_taken_ms:.2f}\n")
        f.write(f"{memory_used_kb}\n")
