import asyncio
import datetime
from bleak import BleakClient
import csv
import os

DEVICE_ADDRESS = "DC:2C:48:D2:71:6B"  # Endereço do dispositivo
CHARACTERISTIC_UUID_PERCENT =   "00002a19-0000-1000-8000-00805f9b34fb" 
CHARACTERISTIC_UUID_TENSAO =    "0000aa22-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID_CORRENTE =  "0000aa33-0000-1000-8000-00805f9b34fb"
CSV_FILE = "bateryAnalisys.csv"

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
                        # print("percent: ",percent)
                        corrente = await client.read_gatt_char(CHARACTERISTIC_UUID_CORRENTE)
                        # print("corrente: ",corrente)
                        tensao = await client.read_gatt_char(CHARACTERISTIC_UUID_TENSAO)

                        # print(f"Percent: {percent}, Corrente: {corrente}, Tensão: {tensao}")

                        valor_tensao = int.from_bytes(tensao, byteorder="little", signed=True)
                        valor_corrente = int.from_bytes(corrente, byteorder="little", signed=True)
                        valor_percent = int.from_bytes(percent, byteorder="little", signed=True)

                        # Captura o timestamp atual
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{timestamp} | Valor: {valor_percent} | Tensão: {valor_tensao} | Corrente: {valor_corrente}")

                        # Escreve a linha no CSV
                        # writer.writerow([timestamp, valor_percent])
                        writer.writerow([timestamp, valor_percent, valor_tensao, valor_corrente])
                        file.flush()

                    except Exception as e:
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Erro na leitura: {e}")

                    await asyncio.sleep(2)
        else:
            print("Não foi possível conectar ao sensor.")
            return

try:
    asyncio.run(read_sensor())
except KeyboardInterrupt:
    print("\nInterrompido pelo usuário. Bluetooth desconectado com segurança.")