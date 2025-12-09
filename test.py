import os
import subprocess
import matplotlib.pyplot as plt

INPUT_FOLDER = "Datapoints"
# OUTPUT_FOLDER = "Results_efficient"
# PROGRAM = "efficient.py"

OUTPUT_FOLDER = "Results_basic"
PROGRAM = "basic.py"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

problem_sizes = []
cpu_times = []
memory_usages = []

# Process each file in Datapoints/
for filename in sorted(os.listdir(INPUT_FOLDER)):
    if not filename.endswith(".txt"):
        continue

    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, "out_" + filename)

    # Run your alignment program
    result = subprocess.run(
        ["python3", PROGRAM, input_path, output_path],
        capture_output=True,
        text=True
    )

    # Read its output
    with open(output_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    cost = int(lines[0])
    aligned_s1 = lines[1]
    aligned_s2 = lines[2]
    time_ms = float(lines[3])
    mem_kb = int(lines[4])

    # Problem size = |s1| + |s2|
    problem_size = len(aligned_s1.replace("_", "")) + len(aligned_s2.replace("_", ""))

    problem_sizes.append(problem_size)
    cpu_times.append(time_ms)
    memory_usages.append(mem_kb)

    print(f"Processed {filename}: size={problem_size}, time={time_ms} ms, mem={mem_kb} KB")

# # -------------------------------
# # Plot CPU Time vs Problem Size
# # -------------------------------
# plt.figure(figsize=(8, 5))
# plt.plot(problem_sizes, cpu_times, marker='o')
# plt.xlabel("Problem Size (m + n)")
# plt.ylabel("CPU Time (ms)")
# plt.title("CPU Time vs Problem Size")
# plt.grid(True)
# plt.tight_layout()
# plt.savefig(OUTPUT_FOLDER + "/cpu_time_vs_size.png")

# # -------------------------------
# # Plot Memory vs Problem Size
# # -------------------------------
# plt.figure(figsize=(8, 5))
# plt.plot(problem_sizes, memory_usages, marker='o')
# plt.xlabel("Problem Size (m + n)")
# plt.ylabel("Memory Usage (KB)")
# plt.title("Memory Usage vs Problem Size")
# plt.grid(True)
# plt.tight_layout()
# plt.savefig(OUTPUT_FOLDER + "/memory_vs_size.png")

# print("\nPlots generated:")
# print(" → cpu_time_vs_size.png")
# print(" → memory_vs_size.png")
