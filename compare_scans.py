import re

def parse_log(log_path):
    data = {}
    with open(log_path, 'r') as f:
        content = f.read()
    blocks = re.findall(r"Addr ([0-9A-F]+) \(\+\d+\): \[(.*?)\]", content)
    for addr_hex, vals_str in blocks:
        addr = int(addr_hex, 16)
        vals = [v.strip() for v in vals_str.split(',')]
        for i, v in enumerate(vals):
            try:
                val = int(v)
                if val > 32767: val -= 65536
                data[addr + i] = val
            except ValueError:
                continue
    return data

if __name__ == "__main__":
    old_data = parse_log('full_scan_7300.log')
    new_data = parse_log('full_scan_fresh.log')
    
    print(f"{'Address':<10} {'Old Val':<10} {'New Val':<10} {'Delta':<10}")
    print("-" * 45)
    
    # Check all registers in new data that are roughly in the range
    candidates = []
    for addr, val in new_data.items():
        if 6500 <= abs(val) <= 8000:
            old_val = old_data.get(addr, "N/A")
            delta = val - old_val if isinstance(old_val, int) else "N/A"
            candidates.append((addr, old_val, val, delta))
            
    # Sort by address
    for addr, old, new, delta in sorted(candidates, key=lambda x: x[0]):
        print(f"0x{addr:04X} ({addr:<5}) {str(old):<10} {str(new):<10} {str(delta):<10}")
