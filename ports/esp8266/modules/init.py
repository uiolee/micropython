def led(p, v):
    from machine import Pin
    return Pin(p, Pin.OUT, value=v)


def servo(p, d, f):
    from machine import PWM, Pin
    return PWM(Pin(p, Pin.OUT), f, d)


def reader(sck, mosi, miso, rst, cs):
    from rc522 import RC522
    return RC522(sck, mosi, miso, rst, cs)


def id(path='id.cfg') -> None:
    id_cfg = tuple()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            id_cfg = tuple(f.read().split(','))
            print('init.id()', id_cfg)
    except Exception as err:
        print('load id_cfg fail,', Exception, err)
    finally:
        return id_cfg
