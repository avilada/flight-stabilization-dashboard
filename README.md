# flight-stabilization-dashboard

## Ideas
1. Telemetry script
2. PID controller for drone flight stabilization
3. Connect PID to flight sim
4. Build dashboard to visualize data

## Tech Stack
1. Python: PID prototype, logging, visualizations
2. Flight Sim and Middleware: PX4 SITL and Gazebo
3. Visualizations: Matplotlib or Plotly (In progress)

## Setup and Roadmap
1. Install PX4 SITL :white_check_mark:
2. Configure Gazebo :white_check_mark:
3. Configure QGC :white_check_mark:
4. Verify drone can fly using default controller :white_check_mark:
5. MAVLink Basics :white_check_mark:
6. PID
7. Telemetry
8. PID Altitude Wrapper
9. Testing

Operating System: Linux 24 or later, MacOS, or Windows WSL2  
Python version: 3.12 or later  
PX4 Firmware: latest stable release  
Gazebo: latest (some versions come preconfigured with PX4)  
  
<mark>Note: PX4 SITL is best supported on Linux. MacOS support is limited and comes with some potential bugs.</mark>

## Testing

Pytest
```
pip install pytest
pytest -v
```
## Simulation

Currently, the physics is being tested with simulation to:
  1. confirm PID reduces error over time
  2. confirm there are no huge oscillations or runaway behavior
