from numpy import sin, cos, pi


def horizontal_sinusoid(t, amplitude, frequency):
    return (
        amplitude * sin(2*pi*frequency*t),
        0
    )

def circle(t, amplitude, frequency):
    return (
    amplitude * cos(2 * pi * frequency * t),
    amplitude * sin(2 * pi * frequency * t)
)

def figure8(t, amplitude, frequency):
    return (
        amplitude * sin(2*pi*frequency*t),
        amplitude * 0.5 * sin(4*pi*frequency*t)
    )