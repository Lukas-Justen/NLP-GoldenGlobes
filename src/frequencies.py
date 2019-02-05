import pandas as pd

import warnings
warnings.filterwarnings('ignore')
import matplotlib
%matplotlib inline
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#This takes in a dataset and then replaces the column specified in the second parameter, with an instant instead of timestamp. Returns this data with conversion
def convert_instants(data, timeLabel, numbins = 200):
    from datetime import datetime
    timeLabel = 'timestamp_ms'
    times = data[[timeLabel]]
    timevals = str(times.timestamp_ms[0])

    # Parsing out the timestamp values and adding to new dataframe
    datetimes = []
    for i in times.timestamp_ms.iloc[:]:
        i = str(i)
        try:
            datetime = datetime.strptime(i, '%Y-%m-%d %X')
            dtTuple = [datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second]
            datetimes.append(dtTuple)
        except ValueError:
            pass

    df_timestamps = pd.DataFrame(datetimes, columns=['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second'])
    print('There are %d examples.' % len(df_timestamps))
    df_timestamps['Instant'] = (df_timestamps.Hour * 3600) + (df_timestamps.Minute * 60) + df_timestamps.Second
    df_timestamps[['Instant']].plot.hist('Instant', bins=numbins, alpha=0.5)
    plt.show()
    data[['Instant']] = df_timestamps[['Instant']]
    data.drop([timeLabel], axis=1, inplace=True)
    return data



#Shows a histogram of the input data across the column specified in second parameter. Third parameter determines number of bins.
#returns the indices that include the largest bin, the minimal value of this bin, and maximum value of this bin.
def freq_hist(data, label, numbins=200):
    import numpy as np
    count, division = np.histogram(data[[label]], bins=numbins)
    data[['Instant']].hist(bins=division)
    maxvalindex = count.argmax()
    interval_min = division[maxvalindex]
    interval_max = division[maxvalindex + 1]

    maxvalindexes = data.index[(data[label] >= interval_min) & (data[label] <= interval_max)].tolist()

    return maxvalindexes, interval_min, interval_max

new_data = convert_instants(data, 'timestamp_ms', 100)

new_data.head()

data.head()

indexes, minval, maxval = freq_hist(data, 'Instant', 100)

print(len(indexes))
print(minval)
print(maxval)

print(len(data))
print(indexes)

data.iloc[56453:60612]