import sys
import time
import psutil

#### Gap Cost ####
delta = 30
ALPHA = {
    'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94},
    'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48},
    'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
    'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0}
}
gap_character = '_'
invalid_cost = 500

#### Sequence generation ####
def generate(s, indices):
    for i in indices:
        s = s[:i+1] + s + s[i+1:]
    return s


def read_input(path):
    with open(path) as f:
        lines = [l.strip().upper() for l in f if l.strip()]

    i = 0
    A = lines[i]; i += 1

    A_idx = []
    while i < len(lines) and lines[i].isnumeric():
        A_idx.append(int(lines[i])); i += 1

    if i >= len(lines):
        raise ValueError("Input file format error: Sequence B missing.")

    B = lines[i]; i += 1
    B_idx = []
    while i < len(lines) and lines[i].isnumeric():
        B_idx.append(int(lines[i])); i += 1

    return generate(A, A_idx), generate(B, B_idx)


#### DP Alignment ####
def basic_sequence_alignment_algorithm(x, y):
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1): dp[i][0] = i * delta
    for j in range(n + 1): dp[0][j] = j * delta

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            try:
                mm_cost = ALPHA[x[i-1]][y[j-1]]
            except KeyError:
                mm_cost = invalid_cost

            dp[i][j] = min(
                dp[i-1][j-1] + mm_cost,
                dp[i-1][j] + delta,
                dp[i][j-1] + delta
            )

    ax, ay = [], []
    i, j = m, n
    EPSILON = 1e-9

    while i > 0 or j > 0:
        mm_cost = invalid_cost
        if i > 0 and j > 0:
            try:
                mm_cost = ALPHA[x[i-1]][y[j-1]]
            except KeyError:
                pass

        cost_diag = dp[i-1][j-1] + mm_cost if i > 0 and j > 0 else float('inf')
        cost_up = dp[i-1][j] + delta if i > 0 else float('inf')
        cost_left = dp[i][j-1] + delta if j > 0 else float('inf')

        min_cost = dp[i][j]

        if abs(min_cost - cost_diag) < EPSILON:
            ax.append(x[i-1])
            ay.append(y[j-1])
            i -= 1
            j -= 1

        elif abs(min_cost - cost_left) < EPSILON:
            ax.append('_')
            ay.append(y[j-1])
            j -= 1

        elif abs(min_cost - cost_up) < EPSILON:
            ax.append(x[i-1])
            ay.append('_')
            i -= 1
        else:
            raise Exception("Traceback error.")

    ax.reverse()
    ay.reverse()
    return ''.join(ax), ''.join(ay), dp[m][n]

#### Memory measurement  ####
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    return int(memory_info.rss / 1024)


### Main function ###
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 sequence_aligner.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        x, y = read_input(input_path)
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    ### Time + Memory Start ###
    start_time = time.time()
    mem1 = process_memory()
    
    aligned_x, aligned_y, score = basic_sequence_alignment_algorithm(x, y)
    end_time = time.time()
    mem2 = process_memory()

    time_taken_ms = (end_time - start_time) * 1000
    memory_used_kb = mem2 - mem1
   

    try:
        with open(output_path, 'w') as f:
            f.write(f"{score}\n")
            f.write(f"{aligned_x}\n")
            f.write(f"{aligned_y}\n")
            f.write(f"{time_taken_ms:.2f}\n")
            f.write(f"{memory_used_kb}\n")

    except IOError:
        print(f"Error: Could not write to output file '{output_path}'.")
        sys.exit(1)
