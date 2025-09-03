import asyncio
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udpin://127.0.0.1:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

    # Print altitude
    async for pos in drone.telemetry.position():
        print(f"Altitude: {pos.relative_altitude_m:.2f} m")
        await asyncio.sleep(1)  # Limit printing

if __name__ == "__main__":
    asyncio.run(run())

