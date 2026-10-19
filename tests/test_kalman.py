from app.nucleo_mro.filtro_kalman import Kalman1D


def test_kalman_converges():
    k = Kalman1D(x0=0.0, P0=1.0, Q=1e-5, R=1e-2)
    measurements = [0.1]*10
    for m in measurements:
        x = k.step(m)
    assert abs(x - 0.1) < 0.05
