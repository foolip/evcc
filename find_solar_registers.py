import re

def find_candidates(log_path, target_min=6500, target_max=8000):
    candidates = []
    current_addr = 0
    
    with open(log_path, 'r') as f:
        content = f.read()
        
    # Pattern to find blocks like "Addr 4001 (+100): [val1, val2, ...]"
    blocks = re.findall(r"Addr ([0-9A-F]+) \(\+\d+\): \[(.*?)\]", content)
    
    for addr_hex, vals_str in blocks:
        addr = int(addr_hex, 16)
        vals = [v.strip() for v in vals_str.split(',')]
        for i, v in enumerate(vals):
            try:
                val = int(v)
                # Check both unsigned and signed int16
                unsigned_val = val
                signed_val = val if val <= 32767 else val - 65536
                
                if target_min <= unsigned_val <= target_max:
                    candidates.append((addr + i, unsigned_val, "unsigned"))
                if target_min <= abs(signed_val) <= target_max:
                    candidates.append((addr + i, signed_val, "signed"))
            except ValueError:
                continue
                
    return candidates

if __name__ == "__main__":
    log_file = 'full_scan_with_fallback.log'
    # Current app says around 7.1kW, so look for values between 6800 and 7400
    results = find_candidates(log_file, target_min=6800, target_max=7400)
    
    # Sort by address (first element of the tuple)
    sorted_results = sorted(list(set(results)), key=lambda x: x[0])
    
    print(f"{'Address':<10} {'Value':<10} {'Type':<10}")
    print("-" * 30)
    for addr, val, t in sorted_results:
        print(f"0x{addr:04X} ({addr:<5}) {val:<10} {t:<10}")
