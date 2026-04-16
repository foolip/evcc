import csv
import math

def calculate_stats(data):
    n = len(data)
    if n == 0: return None
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)
    return {"mean": mean, "std_dev": std_dev, "min": min(data), "max": max(data)}

def analyze_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames[1:] # Skip timestamp
        data = {col: [] for col in columns}
        
        for row in reader:
            for col in columns:
                try:
                    val = float(row[col])
                    data[col].append(val)
                except ValueError:
                    continue

    print(f"{'Register':<10} | {'Mean':>10} | {'StdDev':>10} | {'Min':>10} | {'Max':>10}")
    print("-" * 65)
    
    stats_list = []
    for col in columns:
        s = calculate_stats(data[col])
        if s:
            stats_list.append((col, s))
            print(f"{col:<10} | {s['mean']:10.1f} | {s['std_dev']:10.1f} | {s['min']:10.1f} | {s['max']:10.1f}")

if __name__ == "__main__":
    analyze_csv('solar_log_filtered.csv')
