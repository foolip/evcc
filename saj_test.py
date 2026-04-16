import sys
from pymodbus.client import ModbusTcpClient

# --- Configuration ---
INVERTER_IP = "10.0.3.145"
UNIT_ID = 1

def main():
    ip = sys.argv[1] if len(sys.argv) > 1 else INVERTER_IP
    client = ModbusTcpClient(ip, port=502)
    if not client.connect():
        print(f"[-] Could not connect to {ip}")
        return

    # 1. GRID DATA (Computed like the YAML template)
    # Starts at 16525 (0x408D) to cover the 0x408D-0x4094 range
    res = client.read_holding_registers(address=16525, count=10, slave=UNIT_ID)
    if not res.isError():
        v1 = res.registers[0] / 10.0  # 0x408D
        i1_direct = res.registers[1] / 100.0 # 0x408E (Direct Current)
        p1 = res.registers[3]         # 0x4090
        i1 = p1 / v1 if v1 > 0 else 0 # (Computed Current)

        v2 = res.registers[4] / 10.0  # 0x4091
        p2 = res.registers[5]         # 0x4092
        i2 = p2 / v2 if v2 > 0 else 0
        
        v3 = res.registers[6] / 10.0  # 0x4093
        p3 = res.registers[7]         # 0x4094
        i3 = p3 / v3 if v3 > 0 else 0

        print("\n--- GRID METER (YAML Sync - Fully Computed) ---")
        print(f"Power Total: {p1+p2+p3:7.0f} W (Computed sum)")
        print(f"L1 Current:  {i1:7.2f} A (P/V) [Direct was: {i1_direct:5.2f}]")
        print(f"L2 Current:  {i2:7.2f} A (P/V)")
        print(f"L3 Current:  {i3:7.2f} A (P/V)")

    # 2. PV & BATTERY & SOC (Direct Registers)
    res = client.read_holding_registers(address=0x406F, count=60, slave=UNIT_ID)
    if not res.isError():
        soc = res.registers[0] / 100.0       # 0x406F
        pv_p = res.registers[0x40A4-0x406F]  # 0x40A4
        bat_p = res.registers[0x40A6-0x406F] # 0x40A6 (Int16, signed)
        
        if bat_p > 32767: bat_p -= 65536

        print("\n--- SYSTEM STATUS (YAML Sync) ---")
        print(f"Battery SOC: {soc:7.2f} %")
        print(f"PV Power:    {pv_p:7.0f} W")
        print(f"Bat Power:   {bat_p:7.0f} W")

    # 3. ENERGY METERS (32-bit uints)
    def read_energy(addr, label):
        res = client.read_holding_registers(address=addr, count=2, slave=UNIT_ID)
        if not res.isError():
            val = (res.registers[0] << 16) + res.registers[1]
            print(f"{label:12}: {val/100.0:10.2f} kWh")

    print("\n--- ENERGY METERS (YAML Sync) ---")
    read_energy(0x40FD, "Grid Feed-in") # 0x40FD
    read_energy(0x40C5, "PV Total")    # 0x40C5
    read_energy(0x40D5, "Bat Disch.")   # 0x40D5

    client.close()

if __name__ == "__main__":
    main()
