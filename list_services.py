import asyncio
from bleak import BleakClient

DEVICE_ADDRESS = "DC:2C:48:D2:71:6B"  # Substitua pelo endereço do seu STM32WB09

async def list_services():
    async with BleakClient(DEVICE_ADDRESS) as client:
        if await client.is_connected():
            print("Conectado ao dispositivo!")
            services = await client.get_services()
            for service in services:
                print(f"Serviço: {service.uuid}")
                for char in service.characteristics:
                    print(f"  Característica: {char.uuid} - Properties: {char.properties}")

asyncio.run(list_services())
