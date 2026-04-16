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

async def poll_blocks(host, blocks, port=502, device_id=1):
    client = AsyncModbusTcpClient(host, port=port)
    await client.connect()
    if not client.connected:
        print(f"Failed to connect to {host}")
        return

    MAX_BLOCK_SIZE = 32  # More conservative block size

    for i, b in enumerate(blocks):
        start_addr = b['start']
        end_addr = b['end']
        total_count = end_addr - start_addr + 1
        
        print(f"\n--- Polling Block {i:02d}: Address {start_addr} (0x{start_addr:04X}) to {end_addr} (0x{end_addr:04X}) ({total_count} regs) ---")
        
        for offset in range(0, total_count, MAX_BLOCK_SIZE):
            chunk_addr = start_addr + offset
            chunk_size = min(MAX_BLOCK_SIZE, total_count - offset)
            
            try:
                response = await asyncio.wait_for(
                    client.read_holding_registers(chunk_addr, count=chunk_size, device_id=device_id),
                    timeout=3.0
                )
                
                if not response.isError():
                    print(f"Addr {chunk_addr:04X} (+{chunk_size}): {response.registers}")
                else:
                    # FALLBACK: If chunk fails, try one-by-one for this chunk
                    print(f"Addr {chunk_addr:04X} (+{chunk_size}): ERROR {response}. Falling back to one-by-one...")
                    for sub_offset in range(chunk_size):
                        addr = chunk_addr + sub_offset
                        try:
                            sub_resp = await asyncio.wait_for(
                                client.read_holding_registers(addr, count=1, device_id=device_id),
                                timeout=1.0
                            )
                            if not sub_resp.isError():
                                print(f"  Addr {addr:04X}: {sub_resp.registers[0]}")
                            else:
                                print(f"  Addr {addr:04X}: ERROR {sub_resp}")
                        except Exception as e:
                            print(f"  Addr {addr:04X}: EXCEPTION {e}")
            except Exception as e:
                print(f"Addr {chunk_addr:04X} (+{chunk_size}): EXCEPTION {e}")
            
    client.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 process_saj_map.py <IP_ADDRESS>")
        sys.exit(1)
        
    target_ip = sys.argv[1]
    csv_file = 'saj_modbus_map.csv'
    blocks = extract_blocks(csv_file)
    
    print(f"# Extracted {len(blocks)} contiguous blocks of VALUE registers from {csv_file}")
    print(f"\n# Starting poll of {target_ip} with fallback...")
    asyncio.run(poll_blocks(target_ip, blocks))
