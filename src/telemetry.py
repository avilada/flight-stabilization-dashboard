import asyncio
from mavsdk import System

class DroneConnectionError(Exception):
    """Raised when the drone fails to connect via MAVSDK."""
    pass

async def setup_drone(connection_url: str = "udpin://<IP>:<PORT>", timeout: int = 10) -> System:
    """
    Connect to the PX4 autopilot using MAVSDK.
    Raises DroneConnectionError if not successful within the timeout limit.
    """
    drone = System()
    await drone.connect(system_address=connection_url)

    print(f"Connecting to drone on {connection_url} ...")

    try:
        async with asyncio.timeout(timeout):
            async for state in drone.core.connection_state():
                if state.is_connected:
                    print("Drone discovered and connected successfully!")
                    return drone
    except TimeoutError:
        raise DroneConnectionError(
            f"Failed to connect to drone at {connection_url} within {timeout} seconds."
        )

async def print_telemetry(drone: System):
    """
    Subscribe to telemetry streams and print altitude, velocity, orientation.
    """
    async for position in drone.telemetry.position():
        altitude = position.relative_altitude_m
        print(f"Altitude: {altitude:.2f} m")
        break # remove for continous output

    async for velocity in drone.telemetry.velocity_ned():
        print(f"Velocity (NED): north={velocity.north_m_s:.2f}, "
              f"east={velocity.east_m_s:.2f}, down={velocity.down_m_s:.2f}")
        break # remove for continous output

    async for attitude in drone.telemetry.attitude_euler():
        print(f"Orientation (Euler): roll={attitude.roll_deg:.1f}, "
              f"pitch={attitude.pitch_deg:.1f}, yaw={attitude.yaw_deg:.1f}")
        break # remove for continous output

async def main():
    try:
        drone = await setup_drone()
        await print_telemetry(drone)
    except DroneConnectionError as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
