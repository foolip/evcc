import asyncio
import sys
import csv
import logging
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from pymodbus.constants import ExcCodes

# --- Silence Pymodbus Logging ---
logging.getLogger("pymodbus").setLevel(logging.CRITICAL)

# --- Configuration ---
DEFAULT_IP = "10.0.3.145"
UNIT_ID = 1
MAP_FILE = "saj_modbus_map.csv"
TIMEOUT = 1.0
RETRIES = 2

async def read_with_retry(client, read_func, addr):
    """
    Attempts to read a single Modbus register/coil with retries and connection resets.
    """
    for attempt in range(RETRIES + 1):
        try:
            response = await asyncio.wait_for(
                read_func(address=addr, count=1, device_id=UNIT_ID),
                timeout=TIMEOUT
            )
            
            if response is None:
                if attempt < RETRIES:
                    await asyncio.sleep(0.05 * (attempt + 1))
                    continue
                return None
            
            if response.isError():
                # Retry on potentially transient errors
                if isinstance(response, ExceptionResponse) and response.exception_code in [
                    ExcCodes.DEVICE_FAILURE,
                    ExcCodes.ACKNOWLEDGE,
                    ExcCodes.DEVICE_BUSY,
                    ExcCodes.GATEWAY_PATH_UNAVIABLE,
                    ExcCodes.GATEWAY_NO_RESPONSE
                ]:
                    if attempt < RETRIES:
                        await asyncio.sleep(0.2 * (attempt + 1))
                        continue
                return response
            
            return response
        except (asyncio.TimeoutError, ModbusException):
            if attempt < RETRIES:
                # Reset connection on timeout to clear transaction ID drift
                await client.close()
                await asyncio.sleep(0.2 * (attempt + 1))
                await client.connect()
                continue
            raise
    return None

async def scan_range(client, reg_type, start, end, writer, f):
    print(f"\n[*] Scanning 0x{start:04X} to 0x{end:04X} {reg_type}...")
    
    if reg_type == "HOLDING":
        read_func = client.read_holding_registers
    elif reg_type == "INPUT":
        read_func = client.read_input_registers
    elif reg_type == "COIL":
        read_func = client.read_coils
    elif reg_type == "DISCRETE":
        read_func = client.read_discrete_inputs
    else:
        return

    total = end - start + 1
    for addr in range(start, end + 1):
        # Update progress every 10 registers
        if addr % 10 == 0 or addr == end:
            percent = ((addr - start) / total) * 100
            sys.stdout.write(f"\r[*] Progress: {percent:5.1f}% | Addr: 0x{addr:04X} {reg_type}")
            sys.stdout.flush()

        try:
            response = await read_with_retry(client, read_func, addr)
            if response is not None and not response.isError():
                val = response.registers[0] if hasattr(response, 'registers') else response.bits[0]
                writer.writerow([f"0x{addr:04X}", reg_type, val])
                f.flush()
        except (asyncio.TimeoutError, ModbusException):
            continue
        except Exception as e:
            print(f"\n[!] Error at 0x{addr:04X} {reg_type}: {type(e).__name__}: {e}")
            raise e

    print(f"\n[+] {reg_type} scan complete.")

async def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 comprehensive_saj_scan.py <IP_ADDRESS>")
        sys.exit(1)
        
    target_ip = sys.argv[1]
    client = AsyncModbusTcpClient(target_ip, port=502)
    
    if not await client.connect():
        print(f"[-] Could not connect to {target_ip}")
        return

    print(f"[*] Starting sequential scan of {target_ip}...")
    
    with open(MAP_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['address', 'type', 'value'])
        
        for reg_type in ["HOLDING", "INPUT", "COIL", "DISCRETE"]:
            await scan_range(client, reg_type, 0x0000, 0xFFFF, writer, f)

    await client.close()
    print(f"\n[+] Scan complete. Map saved to {MAP_FILE}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Scan interrupted by user.")
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        import traceback
        traceback.print_exc()
