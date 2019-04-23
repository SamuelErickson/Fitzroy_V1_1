if __name__ == "__main__":
    import time
    import datetime
    import pigpio
    import DHT22
    import pandas as pd
    from math import floor

    # find information on box config
    df_config = pd.read_csv('config.csv')

    # Intervals of about 2 seconds or less will eventually hang the DHT22.
    INTERVAL = df_config["TempLogInterval_sec"]
    window = df_config["TempDisplayWindow_sec"]
    maxSamples = floor(window/INTERVAL) #the number of rows of data to be held in short term storage

    df_s = pd.read_csv('tempData_shortTerm.csv')
    numSamples = df_s.shape[0] #number of rows of data already stored in short term storage

    pi = pigpio.pi()
    s = DHT22.sensor(pi, 24)
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
            vals = {"Time":timeStamp,"Temp":s.temperature()}
            if (numSamples < maxSamples):
                df_s = df_s.append(vals, ignore_index=True)
                df_s.to_csv('tempData_shortTerm.csv', index=False)
                numRows = numSamples + 1
            else:
                df_s = df_s.iloc[1:]
                df_s = df_s.append(vals, ignore_index=True)
                df_s.to_csv('tempData_shortTerm.csv', index=False)
    finally:
        s.cancel()
        pi.stop()