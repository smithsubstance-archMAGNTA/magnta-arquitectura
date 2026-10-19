"""Filtro de Kalman 1D para señales ruidosas."""


class Kalman1D:
    def __init__(self, x0=0.0, P0=1.0, Q=1e-5, R=1e-2):
        self.x = float(x0)
        self.P = float(P0)
        self.Q = float(Q)
        self.R = float(R)

    def predict(self, u=0.0):
        self.x = self.x + u
        self.P = self.P + self.Q
        return self.x

    def update(self, z):
        K = self.P / (self.P + self.R)
        self.x = self.x + K * (z - self.x)
        self.P = (1 - K) * self.P
        return self.x

    def step(self, z, u=0.0):
        self.predict(u)
        return self.update(z)
