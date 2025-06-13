import asyncio
import datetime
from bleak import BleakClient, BleakScanner
import csv
import os

DEVICE_ADDRESS = "C1:68:B6:D7:F5:C0"  # Endereço do dispositivo
CHARACTERISTIC_UUID_PERCENT =   "00002a19-0000-1000-8000-00805f9b34fb" 
CHARACTERISTIC_UUID_TENSAO =    "0000aa22-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID_CORRENTE =  "0000aa33-0000-1000-8000-00805f9b34fb"
CSV_FILE = "bateryAnalisys_v3.csv"

async def read_sensor():
    async with BleakClient(DEVICE_ADDRESS) as client:
        connected = await client.is_connected()
        if connected:
            print("Conectado ao sensor!")

            file_exists = os.path.isfile(CSV_FILE)

            with open(CSV_FILE, "a", newline="") as file:
                writer = csv.writer(file)
  
                if not file_exists:
                    writer.writerow(["timestamp", "battery_value", "tensao", "corrente"])

                while True:
                    try:
                        percent = await client.read_gatt_char(CHARACTERISTIC_UUID_PERCENT)
                        await asyncio.sleep(2)
                        corrente = await client.read_gatt_char(CHARACTERISTIC_UUID_CORRENTE)
                        await asyncio.sleep(2)
                        tensao = await client.read_gatt_char(CHARACTERISTIC_UUID_TENSAO)
                        await asyncio.sleep(2)

                        # RSSI (potência do sinal)
                        try:
                            adv_dev = await BleakScanner.find_device_by_address(
                                DEVICE_ADDRESS, timeout=5.0
                            )
                            rssi_dbm = adv_dev.rssi if adv_dev else None
                        except Exception as e:
                            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Erro ao obter RSSI: {e}")
                            rssi_dbm = None

                        valor_tensao = int.from_bytes(tensao, byteorder="little", signed=True)
                        valor_corrente = int.from_bytes(corrente, byteorder="little", signed=True)
                        valor_percent = int.from_bytes(percent, byteorder="little", signed=True)
                        
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{timestamp} | Valor: {valor_percent} | Tensão: {valor_tensao} | Corrente: {valor_corrente} | RSSI: {rssi_dbm}")

                        writer.writerow([timestamp, valor_percent, valor_tensao, valor_corrente, rssi_dbm])
                        file.flush()

                    except Exception as e:
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Erro na leitura: {e}")

                    await asyncio.sleep(20)
        else:
            print("Não foi possível conectar ao sensor.")
            return

try:
    asyncio.run(read_sensor())
except KeyboardInterrupt:
    print("\nInterrompido pelo usuário. Bluetooth desconectado com segurança.")