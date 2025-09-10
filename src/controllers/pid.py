from dataclasses import dataclass

@dataclass
class PID:
    kp: float
    ki: float
    kd: float
    i_min: float = -0.5      # integral clamp
    i_max: float =  0.5
    out_min: float = -1.5    # output clamp (e.g., vertical speed)
    out_max: float =  1.5
    d_alpha: float = 0.9     # smoothing for derivative filter (0..1)

    _i: float = 0.0
    _prev_meas: float = None
    _d_filt: float = 0.0

    def reset(self):
        """Reset integral and derivative history."""
        self._i = 0.0
        self._prev_meas = None
        self._d_filt = 0.0

    def update(self, setpoint: float, measurement: float, dt: float) -> float:
        """Compute PID output given a setpoint and current measurement."""

        if dt <= 0:
            return 0.0

        # error
        e = setpoint - measurement

        # Proportional
        p = self.kp * e

        # Integral with clamp
        self._i += self.ki * e * dt
        self._i = max(self.i_min, min(self._i, self.i_max))

        # Derivative on measurement (robust against setpoint steps)
        if self._prev_meas is None:
            d_raw = 0.0
        else:
            d_raw = -self.kd * (measurement - self._prev_meas) / dt
        self._prev_meas = measurement

        # Filtered derivative
        self._d_filt = self.d_alpha * self._d_filt + (1 - self.d_alpha) * d_raw

        # Sum and clamp
        u = p + self._i + self._d_filt
        return max(self.out_min, min(u, self.out_max))
