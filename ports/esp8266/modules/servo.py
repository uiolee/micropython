class SERVO:

    def __init__(self, port, duty_unlock, duty_lock, freq=50) -> None:
        from machine import PWM, Pin, Timer

        self.duty_unlock = duty_unlock
        self.duty_lock = duty_lock
        self.servo = PWM(Pin(port, Pin.OUT, pull=Pin.PULL_UP), freq, self.duty_lock)
        self.__t = Timer('servo')
        self.tdeinit()

    def tdeinit(self, s=1):
        next = self.lock if s > 1 else self.servo.deinit
        self.__t.init(period=1000 * s, mode=0, callback=lambda t: next())

    def unlock(self, s=5):
        print('unlock',s)
        self.servo.duty(self.duty_unlock)
        self.tdeinit(s)

    def lock(self):
        print('lock')
        self.servo.duty(self.duty_lock)
        self.tdeinit()
