import asyncio
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udpin://<IP>:<PORT>") # TODO: enter port for testing

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected successfully!")
            break


    # Start telemetry tasks in parallel
    asyncio.create_task(print_altitude(drone))
    asyncio.create_task(print_velocity(drone))
    asyncio.create_task(print_orientation(drone))

    while True:
        await asyncio.sleep(1)


async def print_altitude(drone):
    async for pos in drone.telemetry.position():
        print(f"Altitude: {pos.relative_altitude_m:.2f} m")
        await asyncio.sleep(1)


async def print_velocity(drone):
    async for vel in drone.telemetry.velocity_ned():
        print(f"Velocity NED: "
              f"North={vel.north_m_s:.2f}, East={vel.east_m_s:.2f}, Down={vel.down_m_s:.2f} m/s")
        await asyncio.sleep(1)


async def print_orientation(drone):
    async for att in drone.telemetry.attitude_euler():
        print(f"Orientation (Euler): "
              f"Roll={att.roll_deg:.2f}°, Pitch={att.pitch_deg:.2f}°, Yaw={att.yaw_deg:.2f}°")
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run())
