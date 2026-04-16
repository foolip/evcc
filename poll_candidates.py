import asyncio
import sys
import csv
from datetime import datetime
from pymodbus.client import AsyncModbusTcpClient

# Comprehensive list of candidates for long-term analysis
CANDIDATES = {
    "0x050E": 0x050E, "0x4204": 0x4204, "0x4213": 0x4213, "0x51A6": 0x51A6, "0xA050": 0xA050, "0x357F": 0x357F,
    "0x402F": 0x402F, "0x40A8": 0x40A8, "0x40AA": 0x40AA, "0x4E03": 0x4E03, "0x4E11": 0x4E11,
    "0x357A": 0x357A, "0x35A1": 0x35A1, "0x35A3": 0x35A3,
    "0x4E55": 0x4E55, "0x8360": 0x8360, "0x8362": 0x8362, "0x837C": 0x837C, "0x837E": 0x837E,
}

async def poll_once(host, port, device_id):
    client = AsyncModbusTcpClient(host, port=port)
    connected = await client.connect()
    if not connected:
        return None
    
    results = {}
    try:
        for name, addr in CANDIDATES.items():
            try:
                response = await asyncio.wait_for(
                    client.read_holding_registers(addr, count=1, device_id=device_id),
                    timeout=1.0
                )
                if not response.isError():
                    val = response.registers[0]
                    if val > 32767: val -= 65536
                    results[name] = val
                else:
                    results[name] = "NaN"
            except Exception:
                results[name] = "NaN"
    finally:
        client.close()
    return results

async def main():
    if len(sys.argv) < 2:
        print("Usage: venv/bin/python3 poll_candidates.py <IP> [interval_seconds]", file=sys.stderr)
        sys.exit(1)
        
    target_ip = sys.argv[1]
    interval = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
    
    sorted_names = sorted(list(CANDIDATES.keys()))
    writer = csv.DictWriter(sys.stdout, fieldnames=['timestamp'] + sorted_names)
    writer.writeheader()
    sys.stdout.flush()

    try:
        while True:
            start_time = asyncio.get_event_loop().time()
            data = await poll_once(target_ip, 502, 1)
            
            if data:
                row = {'timestamp': datetime.now().isoformat(timespec='seconds')}
                row.update(data)
                writer.writerow(row)
                sys.stdout.flush()
            
            # Adjust sleep to maintain the interval regardless of poll duration
            elapsed = asyncio.get_event_loop().time() - start_time
            await asyncio.sleep(max(0, interval - elapsed))
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nPolling stopped by user.", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())
