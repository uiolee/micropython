
def delay(s:int):
    from time import sleep_ms
    while s>0:
        print(s)
        s-=1
        sleep_ms(1000)
