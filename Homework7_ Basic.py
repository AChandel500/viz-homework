# Assignment 7 - Basic Question
# Uses US flight data for 2013, features are airline names, airport codes, departure/arrival times/delays and others.


try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import os
except ImportError:
    print('\nPackages pandas, seaborn or matplotlib.pyplot were not imported successfully.\n\n')


def loadfile(filepath):
    return pd.read_csv(filepath)

def cleandata(dframe):
    dframe.drop(dframe.columns[0], inplace=True, axis=1)
    dframe.drop(['alt', 'dst'], inplace=True, axis=1)
    dframe.dropna(how='any', inplace=True)
    return f'\nNull values:\n\n{dframe.isnull().sum()}'

def getcolumnnames(dframe):
    return list(dframe.columns)

def convert_data_types(dframe, col_labels):
    for label in col_labels:
        if label in ('dep_time', 'dep_delay', 'arr_time', 'arr_delay', 'air_time'):
            dframe[label] = dframe[label].astype(dtype='int64')
    return dframe.dtypes

def dataframe_byairline(dframe):
    """For no reason, accepts flight data as a dataframe and returns a dict of dataframes by airline"""
    flightdata_byairline = {}
    for airline in pd.unique(dframe['airline']):
        flightdata_byairline.update({airline: dframe[dframe.airline == airline]})
    return flightdata_byairline



filepath = 'flightdata.csv'

try:
    flight_data = loadfile(filepath)
except IOError:
    print('\n\nFile read error.\n')
    filepath = str(input(r"Please enter a file path (/folder/filename.extension): "))
    flight_data = loadfile(filepath)

# Clean data, verify data types
print(cleandata(flight_data));
flight_data.dtypes

# Get column labels
columnlabels = getcolumnnames(flight_data);

# Convert appropriate time columns to int64 and print data types
convert_data_types(flight_data, columnlabels)

flight_data_by_airline = dataframe_byairline(flight_data)

sns.set()
sns.set_style(style='dark')


os.makedirs('plots/Assignment-7/flight_count-by-route-by-airline', exist_ok=True)

months={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
            7:'July',8:'August',9:'September', 10:'October',11:'November',
            12:'December'}

# Plot Flight count by route, by airline
for airline in pd.unique(flight_data['airline']):


    df = flight_data[(flight_data['airline']==airline)]
    grouped = df.groupby(['origin','dest'])


    for origin,group in grouped:
        print(f'\n{airline} - from {origin[0]} to {origin[1]}\n')
        print(group['flight'].count())


        xticks = list(pd.unique(group['month']))
        xticks.sort()
        axes=sns.countplot(x= 'month', hue='month', data=group, hue_order=xticks, dodge=False)

        axes.set_title(f'{airline}: Number of Flights from {origin[0]} to {origin[1]} in 2013')

        xlabels=[]
        for month_num in xticks:
            xlabels.append(months[month_num])
        axes.set_xticklabels(xlabels,rotation=45, ha='right' )
        xlabels=[]

        axes.set_ylabel('Number of Flights')

        axes.legend(labels=xlabels)

        plt.savefig(f'plots/Assignment-7/flight_count-by-route-by-airline/{airline}-{origin[0]}-{origin[1]}.png', dpi=300)
        plt.show()
        plt.clf()

plt.close()

os.makedirs('plots/Assignment-7/JFK-LAX_Avg_flight_delay-by-airline-by-month', exist_ok=True)


# Plot Average Flight Delay, by month, by airline
a = flight_data['origin'] == 'JFK'; b = flight_data['dest']=='LAX'

for month in pd.unique(flight_data['month']):

    c = flight_data['month'] == month

    for airline in pd.unique(flight_data['airline']):


        d = flight_data['airline'] == airline

        df = flight_data[a & b & c & d]

        ax = sns.distplot(df['avgdelay'], hist=False, label = airline)
        ax.set_title(f'2013 - JFK to LAX: Average Flight Delay by Airline for {months[month]}')
        ax.set_xlabel('Avg Flight Delay (mins)')

    plt.savefig(f'plots/Assignment-7/JFK-LAX_Avg_flight_delay-by-airline-by-month/{months[month]}.png', dpi=300)
    plt.show()
    plt.clf()

plt.close()