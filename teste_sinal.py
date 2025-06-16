import asyncio
from bleak import BleakScanner

async def scan_ble_devices():
    print("Escaneando dispositivos BLE...")
    
    # Retorna também os dados de anúncio (inclui RSSI correto)
    devices = await BleakScanner.discover(return_adv=True)
    print(devices)
    # for device, adv_data in devices.items():
    #     print(f"Nome: {device.name or 'Desconhecido'}")
    #     print(f"Endereço: {device.address}")
    #     print(f"RSSI: {adv_data.rssi} dBm")
    #     print("-" * 30)

asyncio.run(scan_ble_devices())
