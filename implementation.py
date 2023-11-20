from pickett import Pickett_plot
import pandas as pd

data = pd.read_csv('sample_data.csv')
print(data.columns)
# Plotting phit > 10% only
Pickett_plot(data[data['PHIT']>0.1]['Rt'], data[data['PHIT']>0.1]['PHIT'])