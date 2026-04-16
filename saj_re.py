import sys
import time
import csv
import logging
from pymodbus.client import ModbusTcpClient
from pymodbus.pdu import ExceptionResponse

# --- Silence Pymodbus Logging ---
logging.getLogger("pymodbus").setLevel(logging.CRITICAL)

# --- Configuration ---
INVERTER_IP = "10.0.3.145"
UNIT_ID = 1
MAP_FILE = "saj_modbus_map.csv"
DELAY = 0.05  # 50ms delay between registers

def main():
    ip = sys.argv[1] if len(sys.argv) > 1 else INVERTER_IP
    client = ModbusTcpClient(ip, port=502, timeout=1.0)
    
    if not client.connect():
        print(f"[-] Could not connect to {ip}")
        return

    print(f"[*] Starting full sequential scan of {ip} (0x0000 - 0xFFFF)...")
    
    with open(MAP_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['address_hex', 'address_dec', 'result_type', 'value_or_code'])
        
        # addrs = range(0, 65536)
        addrs = [0x06AA, 0x0B23, 0x25F5, 0x3870, 0x55F2, 0x6736, 0x6E28, 0x8197, 0x964D, 0xADF1, 0xBEF1, 0xC3E4, 0xD86A, 0xEC47, 0xFE75, 0xFFFF]
        try:
            for addr in addrs:
                percent = (addr / 65536.0) * 100
                sys.stdout.write(f"\r[*] Progress: {percent:5.1f}% | Scanning: 0x{addr:04X}")
                sys.stdout.flush()

                time.sleep(DELAY)

                try:
                    res = client.read_holding_registers(address=addr, count=1, slave=UNIT_ID)
                    
                    if res is None:
                        writer.writerow([f"0x{addr:04X}", addr, "ERROR", "TIMEOUT/EMPTY"])
                    elif res.isError():
                        # Record specific Modbus exception code
                        code = getattr(res, 'exception_code', "UNKNOWN")
                        writer.writerow([f"0x{addr:04X}", addr, "EXCEPTION", code])
                    else:
                        # Record successful value
                        writer.writerow([f"0x{addr:04X}", addr, "VALUE", res.registers[0]])
                    f.flush()
                
                except Exception as e:
                    writer.writerow([f"0x{addr:04X}", addr, "ERROR", str(e)])
                    f.flush()
                    # If we get a connection error, try to reconnect
                    if not client.connected:
                        client.connect()

        except KeyboardInterrupt:
            print("\n[*] Scan interrupted by user.")
            
    client.close()
    print(f"\n[+] Scan complete. Map saved to {MAP_FILE}")

if __name__ == "__main__":
    main()
