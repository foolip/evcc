import sys
from pymodbus.client import ModbusTcpClient

# --- Configuration ---
INVERTER_IP = "10.0.3.145"
UNIT_ID = 1

# Comprehensive ranges for SAJ H2
RANGES = [
    (0x4000, 50), (0x4050, 50), (0x40A0, 50), (0x40F0, 50),
    (0x8000, 50), (0x8100, 50), (0x8F00, 50)
]

def main():
    ip = sys.argv[1] if len(sys.argv) > 1 else INVERTER_IP
    client = ModbusTcpClient(ip, port=502)
    
    if not client.connect():
        print(f"[-] Could not connect to {ip}")
        return

    print(f"Searching for 11kW charging values on {ip}...")
    print(f"Looking for: Currents (1500-2500) and Power (3000-6000)")
    print(f"{'Addr (Hex)':10} | {'Addr (Dec)':10} | {'Value'}")
    print("-" * 45)

    for start_addr, count in RANGES:
        try:
            # We use small steps to avoid "Invalid exception" on large blocks
            step = 10
            for offset in range(0, count, step):
                addr = start_addr + offset
                result = client.read_holding_registers(address=addr, count=step, slave=UNIT_ID)
                if result.isError(): continue
                
                for i, val in enumerate(result.registers):
                    # 1. Look for Amps (15.00A - 25.00A)
                    is_amp = 1500 <= val <= 2500
                    # 2. Look for Power (3000W - 6000W)
                    is_pwr = 3000 <= val <= 6000
                    
                    if is_amp or is_pwr:
                        reg_addr = addr + i
                        label = "AMPS?" if is_amp else "POWER?"
                        print(f"{hex(reg_addr):10} | {reg_addr:10} | {val:10}  {label}")
        except Exception:
            continue
            
    client.close()
    print("\nScan complete. Look for three consecutive AMPS? or POWER? hits.")

if __name__ == "__main__":
    main()
