if __name__ == "__main__":
    import time
    import datetime
    import pigpio
    import pandas as pd
    from . import DHT22

    # Intervals of about 2 seconds or less will eventually hang the DHT22.
    df_config = pd.read_csv('../config.csv')

    pinNum = int(df_config["DHT22_pin"].iloc[0])

    INTERVAL=3
    pi = pigpio.pi()
    s = DHT22.sensor(pi, df_config)
    r = 0




    next_reading = time.time()
    try:
        while True:
            timeStamp = datetime.datetime.now().isoformat()
            r += 1
            s.trigger()
            time.sleep(0.2)
            print("{} {} {}".format(timeStamp, s.humidity(), s.temperature()))
            next_reading += INTERVAL
            time.sleep(next_reading-time.time()) # Overall INTERVAL second polling.
    finally:
        s.cancel()
        pi.stop()