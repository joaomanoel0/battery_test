import asyncio
from bleak import BleakScanner

async def scan_ble():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Nome: {device.name}, Endereço: {device.address}")

asyncio.run(scan_ble())
