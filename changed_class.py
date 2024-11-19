def __init__(self, bus=0, device=0, spd=1000000, pin_mode=10, pin_rst=-1, debugLevel='WARNING'):
    self.spi = spidev.SpiDev()
    self.spi.open(bus, device)
    self.spi.max_speed_hz = spd

    self.logger = logging.getLogger('mfrc522Logger')
    self.logger.addHandler(logging.StreamHandler())
    level = logging.getLevelName(debugLevel)
    self.logger.setLevel(level)

    # Get the current GPIO mode
    gpioMode = GPIO.getmode()

    # If no mode is set, set it
    if gpioMode is None:
        GPIO.setmode(pin_mode)
    elif gpioMode != pin_mode:
        raise ValueError("GPIO mode mismatch. Ensure consistent GPIO mode.")

    if pin_rst == -1:
        if pin_mode == GPIO.BOARD:
            pin_rst = 15
        else:
            pin_rst = 22

    GPIO.setwarnings(False)  # Suppress warnings
    GPIO.setup(pin_rst, GPIO.OUT)
    GPIO.output(pin_rst, 1)
    self.MFRC522_Init()
