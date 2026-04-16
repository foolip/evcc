import csv
import sys

def extract_blocks(csv_path):
    blocks = []
    current_block = None
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['result_type'] == 'VALUE':
                addr = int(row['address_dec'])
                if current_block is None:
                    current_block = {'start': addr, 'end': addr}
                elif addr == current_block['end'] + 1:
                    current_block['end'] = addr
                else:
                    blocks.append(current_block)
                    current_block = {'start': addr, 'end': addr}
        if current_block:
            blocks.append(current_block)
    return blocks

def generate_bash(blocks, ip="10.0.3.145"):
    with open("poll_blocks.sh", "w") as f:
        f.write("#!/bin/bash\n\n")
        f.write(f"IP={ip}\n\n")
        for block in blocks:
            start = block['start']
            count = block['end'] - start + 1
            if count > 10000:
                print(f"Skipping huge block 0x{start:04X} to 0x{block['end']:04X}")
                continue

            MAX_COUNT = 125
            for offset in range(0, count, MAX_COUNT):
                c = min(MAX_COUNT, count - offset)
                s = start + offset
                f.write(f"echo '--- Polling 0x{s:04X} ({s}) to 0x{s+c-1:04X} ({s+c-1}) count {c} ---'\n")
                f.write(f"mbpoll -0 -r {s} -c {c} -1 $IP || echo 'Failed to poll 0x{s:04X}'\n\n")

if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else '10.0.3.145'
    try:
        blocks = extract_blocks('saj_modbus_map.csv')
        generate_bash(blocks, ip)
        print("Generated poll_blocks.sh successfully.")
    except Exception as e:
        print(f"Error: {e}")
