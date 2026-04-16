import csv
import math
import sys

def calculate_stats(data):
    n = len(data)
    if n == 0: return None
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)
    return {"mean": mean, "std_dev": std_dev, "min": min(data), "max": max(data)}

def analyze_combined(files):
    combined_data = {}
    columns = []
    
    for file_path in files:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            if not columns:
                columns = reader.fieldnames[1:] # Skip timestamp
                combined_data = {col: [] for col in columns}
            
            for row in reader:
                # Skip extra headers if they exist in the middle of the file
                if row['timestamp'] == 'timestamp':
                    continue
                
                # Check for NaN in any column
                if any(row[col] == "NaN" for col in columns):
                    continue
                    
                for col in columns:
                    try:
                        val = float(row[col])
                        combined_data[col].append(val)
                    except ValueError:
                        continue

    print(f"{'Register':<10} | {'Mean':>10} | {'StdDev':>10} | {'Min':>10} | {'Max':>10}")
    print("-" * 65)
    
    for col in columns:
        s = calculate_stats(combined_data[col])
        if s:
            print(f"{col:<10} | {s['mean']:10.1f} | {s['std_dev']:10.1f} | {s['min']:10.1f} | {s['max']:10.1f}")

if __name__ == "__main__":
    analyze_combined(['solar_log.csv', 'solar_log2.csv'])
