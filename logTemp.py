if __name__ == "__main__":
    import time
    import pigpio
    import DHT22
    # Intervals of about 2 seconds or less will eventually hang the DHT22.
    INTERVAL=3
    pi = pigpio.pi()
    s = DHT22.sensor(pi, 24)
    r = 0
    next_reading = time.time()
    try:
        while True:
            r += 1
            s.trigger()
            time.sleep(0.2)
            print("{} {} {} {:3.2f} {} {} {} {}".format(
                r, s.humidity(), s.temperature(), s.staleness(),
                s.bad_checksum(), s.short_message(), s.missing_message(),
                s.sensor_resets()))
            next_reading += INTERVAL
            time.sleep(next_reading-time.time()) # Overall INTERVAL second polling.
    finally:
        s.cancel()
        pi.stop()