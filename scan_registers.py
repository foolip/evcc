import csv
import asyncio
from pymodbus.client import AsyncModbusTcpClient

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

async def scan_registers(host, blocks, port=502, device_id=1):
    client = AsyncModbusTcpClient(host, port=port)
    await client.connect()
    if not client.connected:
        print(f"Failed to connect to {host}")
        return

    MAX_BLOCK_SIZE = 32

    for block in blocks:
        start_addr = block['start']
        total_count = block['end'] - block['start'] + 1

        if total_count > 10000:
            print(f"\n--- Skipping 0x{start_addr:04X} to 0x{block['end']:04X} (too big: {total_count}) ---")
            continue
        
        print(f"\n--- Scanning 0x{start_addr:04X} to 0x{block['end']:04X} (count: {total_count}) ---")
        
        for offset in range(0, total_count, MAX_BLOCK_SIZE):
            chunk_addr = start_addr + offset
            chunk_size = min(MAX_BLOCK_SIZE, total_count - offset)
            
            try:
                response = await asyncio.wait_for(
                    client.read_holding_registers(chunk_addr, count=chunk_size, device_id=device_id),
                    timeout=3.0
                )
                if not response.isError():
                    print(f"Addr 0x{chunk_addr:04X} (+{chunk_size}): {response.registers}")
                else:
                    print(f"Addr 0x{chunk_addr:04X} (+{chunk_size}): ERROR {response}")
            except Exception as e:
                print(f"Addr 0x{chunk_addr:04X} (+{chunk_size}): EXCEPTION {e}")
            
    client.close()

if __name__ == "__main__":
    import sys
    target_ip = sys.argv[1] if len(sys.argv) > 1 else '10.0.3.145'
    blocks = extract_blocks('saj_modbus_map.csv')
    asyncio.run(scan_registers(target_ip, blocks))
