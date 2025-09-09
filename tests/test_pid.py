import math
import pytest
from src.controllers.pid import PID # TODO: Fix depending on structure

def test_proportional_only():
    pid = PID(kp=2.0, ki=0.0, kd=0.0)
    output = pid.update(setpoint=10.0, measurement=8.0, dt=0.1)
    assert math.isclose(output, 4.0, rel_tol=1e-6)  # error=2 → P=4

def test_integral_accumulates():
    pid = PID(kp=0.0, ki=1.0, kd=0.0, i_min=-5.0, i_max=5.0)
    outputs = []
    for _ in range(5):  # 5 cycles with error=1, dt=1
        outputs.append(pid.update(1.0, 0.0, 1.0))
    # After 5 steps, integral term = 5
    assert math.isclose(outputs[-1], 5.0, rel_tol=1e-6)

def test_integral_clamping():
    pid = PID(kp=0.0, ki=10.0, kd=0.0, i_min=-1.0, i_max=1.0)
    for _ in range(10):
        pid.update(1.0, 0.0, 1.0)  # large accumulation
    # Integral should clamp at +1.0
    assert pid._i <= 1.0

def test_derivative_response():
    pid = PID(kp=0.0, ki=0.0, kd=1.0)
    # First call, no prev measurement → D=0
    out1 = pid.update(0.0, 0.0, 1.0)
    # Step change in measurement
    out2 = pid.update(0.0, 1.0, 1.0)
    assert out2 != 0.0  # should produce derivative term

def test_output_limits():
    pid = PID(kp=100.0, ki=0.0, kd=0.0, out_min=-10.0, out_max=10.0)
    # Big error → raw P=200 → clamp at +10
    output = pid.update(5.0, 3.0, 0.1)
    assert output == 10.0
