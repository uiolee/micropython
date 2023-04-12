import uos
import network
from flashbdev import bdev


def wifi():
    import ubinascii

    ap_if = network.WLAN(network.AP_IF)
    ssid = b"芝麻开门-%s" % ubinascii.hexlify(ap_if.config("mac")[-3:])
    ap_if.config(ssid=ssid, security=network.AUTH_OPEN, key=b"")


def check_bootsec():
    buf = bytearray(bdev.SEC_SIZE)
    bdev.readblocks(0, buf)
    empty = True
    for b in buf:
        if b != 0xFF:
            empty = False
            break
    if empty:
        return True
    fs_corrupted()


def fs_corrupted():
    import time

    while 1:
        print(
            """\
The filesystem starting at sector %d with size %d sectors looks corrupt.
You may want to make a flash snapshot and try to recover it. Otherwise,
format it with uos.VfsLfs2.mkfs(bdev), or completely erase the flash and
reprogram MicroPython.
"""
            % (bdev.start_sec, bdev.blocks)
        )
        time.sleep(3)


def setup():
    check_bootsec()
    print("Performing initial setup")
    wifi()
    uos.VfsLfs2.mkfs(bdev)
    vfs = uos.VfsLfs2(bdev)
    uos.mount(vfs, "/")
    with open("boot.py", "w") as f:
        f.write("""\
# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import uos, machine
# uos.dupterm(None, 1) # disable REPL on UART(0)
import gc

# import webrepl
# webrepl.start()
gc.collect()
print('芝麻开门 - ZMKM')
""")

    with open("webrepl_cfg.py", "w") as f:
        f.write("""\
PASS = ''
""")

    return vfs
