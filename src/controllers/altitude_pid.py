from src.controllers.pid import PID

class AltitudeController:
    """
    AltitudeController wraps a PID controller for altitude stabilization.
    
    - It compares the drone's current altitude against the target (setpoint).
    - Computes an output (thrust adjustment).
    - Can be tuned with kp, ki, kd values for altitude dynamics.
    """

    def __init__(self, kp=1.0, ki=0.0, kd=0.0, setpoint=0.0):
        # Create a PID controller specifically for altitude
        self.pid = PID(kp=kp, ki=ki, kd=kd, setpoint=setpoint)

    def set_target_altitude(self, target):
        """Set the desired altitude (meters)."""
        self.pid.setpoint = target

    def update(self, current_altitude, dt):
        """
        Compute the thrust adjustment given the current altitude.
        
        Args:
            current_altitude (float): Measured altitude in meters.
            dt (float): Time step since last update (seconds).
        
        Returns:
            float: Control output (thrust adjustment).
        """
        return self.pid.update(current_altitude, dt)

    def reset(self):
        """Reset the PID controller (clear accumulated error)."""
        self.pid.reset()
