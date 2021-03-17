import numpy as np
import pandas as pd
import itertools
from collections import defaultdict

url = "https://raw.githubusercontent.com/DexterHyde/Python-Data-Engineering-Projects/master/Sales%20Analysis/sales_data_sample.csv"
#Cheating a bit using pandas to read the csv,
#but everyone knows pandas is the best for reading a csv
data = pd.read_csv(url, encoding='latin1', header = None).values

#create salesData as a json with 3 keys, the third one containing a 0
salesData = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

#Obtain total number of rows
rows = data.shape[0]

#salesData = efficiently (o(n)) way of getting all sales and #products for each year and month in the database
#9th column is the month of the sale
#10th column is the year of the sale
#second column is the # of products sold
#fifth column are the sales for that particular month in the year
for p in range(1, rows):
    salesData[int(data[p,8])][data[p,9]]['prods'] += int(data[p, 1])
    salesData[int(data[p,8])][data[p,9]]['sales'] += float(data[p, 4])

#Print total products sold and the sales revenue for each month for all years
#also, basically transform the dictionary into an array containing sales for each month in each year
container = []
for month in sorted(salesData.keys()):
  for year in sorted(salesData[month].keys()):
    print(f"month: {month}, year: {year}, # sold: {salesData[month][year]['prods']}, Sales Revenue: {salesData[month][year]['sales']:2.2f}")
    container.append([month, year, salesData[month][year]['sales']])
print("\n")
#Let's sort the data by monthly sales revenue and print it
orderedData = sorted(container, key = lambda x: x[2], reverse = True)
[print(f"Month: {x[0]}, Year: {x[1]}, Sales Revenue: {x[2]:2.2f}") for x in orderedData]

#Get sales average (per month)
averageSales = sum(x[2] for x in container)/len(container)
print(f'\nAverage Sales per month:{averageSales:2.2f}')

#Get the best overall month for the company's history:
bestMonth = orderedData[0]

print(f'\nBest Month: {bestMonth[0]}, Year: {bestMonth[1]}, Total Sold: {bestMonth[2]:2.2f}')