import asyncio
from bleak import BleakScanner

def callback(device, adv_data):
    print(f"Dispositivo: {device.address}")
    print(f"Nome: {adv_data.local_name or device.name or 'Desconhecido'}")
    print(f"RSSI: {adv_data.rssi} dBm")
    print("-" * 30)

async def main():
    scanner = BleakScanner()
    scanner.register_detection_callback(callback)
    await scanner.start()
    await asyncio.sleep(5)
    await scanner.stop()

asyncio.run(main())
