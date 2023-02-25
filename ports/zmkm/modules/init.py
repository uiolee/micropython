

def led(p, v):
    from machine import PWM, Pin
    return Pin(p, Pin.OUT, value=v)


def servo(p, d, f):
    from machine import PWM, Pin
    return PWM(Pin(p, Pin.OUT), f, d)


def reader(sck, mosi, miso, rst, cs):
    from rc522 import RC522
    return RC522(sck, mosi, miso, rst, cs)


def id_cfg() -> None:
    pass
