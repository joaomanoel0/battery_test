import asyncio
import datetime
from bleak import BleakClient, BleakScanner
import csv
import os

DEVICE_ADDRESS = "C1:68:B6:D7:F5:C0"
DEVICE_ADDRESS = "D5:73:6C:58:6A:5D"

CHARACTERISTIC_UUID_PERCENT =   "00002a19-0000-1000-8000-00805f9b34fb" 
CHARACTERISTIC_UUID_TENSAO =    "0000aa22-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID_CORRENTE =  "0000aa33-0000-1000-8000-00805f9b34fb"
CSV_FILE = "bateryAnalisys_v3.csv"

async def get_rssi_of_device(target_address):
    print("🔍 Escaneando dispositivos BLE para obter RSSI...")
    devices = await BleakScanner.discover(return_adv=True)
    for address, (device, adv_data) in devices.items():
        if address.upper() == target_address.upper():
            print(f"📡 Dispositivo encontrado! RSSI: {adv_data.rssi} dBm")
            return adv_data.rssi
    print("❌ Dispositivo não encontrado na varredura.")
    return None

async def read_sensor():
    while True:
        # await client.disconnect()
        # Passo 1: Buscar RSSI
        rssi = await get_rssi_of_device(DEVICE_ADDRESS)
        
        # Passo 2: Conectar ao dispositivo
        async with BleakClient(DEVICE_ADDRESS) as client:
            connected = await client.is_connected()
            if connected:
                print("✅ Conectado ao sensor!")

                file_exists = os.path.isfile(CSV_FILE)
                with open(CSV_FILE, "a", newline="") as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(["timestamp", "rssi", "battery_value", "tensao", "corrente"])

                    try:
                        percent = await client.read_gatt_char(CHARACTERISTIC_UUID_PERCENT)
                        await asyncio.sleep(1)
                        corrente = await client.read_gatt_char(CHARACTERISTIC_UUID_CORRENTE)
                        await asyncio.sleep(1)
                        tensao = await client.read_gatt_char(CHARACTERISTIC_UUID_TENSAO)
                        await asyncio.sleep(1)

                        valor_tensao = int.from_bytes(tensao, byteorder="little", signed=True)
                        valor_corrente = int.from_bytes(corrente, byteorder="little", signed=True)
                        valor_percent = int.from_bytes(percent, byteorder="little", signed=True)

                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{timestamp} | RSSI: {rssi} dBm | %: {valor_percent} | V: {valor_tensao} | I: {valor_corrente}")
                        writer.writerow([timestamp, rssi, valor_percent, valor_tensao, valor_corrente])
                        file.flush()

                    except Exception as e:
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Erro na leitura: {e}")
            else:
                print("❌ Não foi possível conectar ao sensor.")

        await asyncio.sleep(20)  # Tempo entre ciclos

try:
    asyncio.run(read_sensor())
except KeyboardInterrupt:
    print("\n🛑 Interrompido pelo usuário.")
