import pandas as pd

#File is too big but you can always download it from my repository instead
url = 'https://raw.githubusercontent.com/DexterHyde/Python-Data-Engineering-Projects/master/Data%20cleaning/Building_Permits.csv'
df = pd.read_csv(url)

#Let's list the database columns alphabetically
columns = sorted(df.columns)
print('\n'.join(columns))

#Total # of missing data
totalMissingData = df.isna().sum().sum()
print(f'\nThe total number of missing data is: {totalMissingData}')

# % of rows that have at least one missing data
numberRows = df.shape[0]
rowsWithMissingValues = df.isnull().any(axis = 1).shape[0]
print(f"Percentage of rows with at least one missing field: {(numberRows/rowsWithMissingValues) * 100}%")

#Reasons as to why there is missing data:
#Taking a glance at the database I could see that a lot of fields are empty whenever the description equals 'street space'
#So, one way for us to know if the description has an impact on the data is to see how many of the missing data is related to a description of 'street space'

dfStreet = df[( (df['Description'] == 'street space') | (df['Description'] == 'street space permit')) & df['Existing Use'].isna()]
dfStreetFalts = dfStreet.shape[0]
totalFalts = df['Existing Use'].isna().sum().sum()

print(f"Total Percentage of missing data where the description is a factor: {((dfStreetFalts/totalFalts) * 100):.2f}\n") #If this percentage is more than 70% we have a good basis as to why there is missing data

#Ways to clean the missing data so that we can work on it
#1st we can fill it horizontally row wise with the next nonNaN value
dfFilled = df.ffill()
#Then we can just fill everything else with 0s
dfFilled0s = dfFilled.fillna(0)
#there shouldn't be any more empty values
dfFilled0s.info()

#Let's try to find all zipCodes the software Engineering way :P

#Let's first get a df where the Zipcode is not empty for us to use it as a start
dfZip = df[df['Zipcode'].notna()]

#Since each zipcode is tied to a block we could use a combination of them as a dictionary
# for every block with an empty zipcode we have that has had a record of its zipcode somewhere in the data
dfZip = dfZip.groupby(['Block', 'Zipcode']).size().reset_index()
dic = dict(zip(dfZip['Block'], dfZip['Zipcode']))

dfTwo = df.copy()
dfTwo.loc[dfTwo['Zipcode'].isna(), "Zipcode"] = dfTwo.loc[dfTwo['Zipcode'].isna(), 'Block'].map(dic)

#See if there are still missing zipcodes
miss = numberRows - dfTwo.loc[dfTwo['Zipcode'].notna()].shape[0]
print(f"Missing zipCodes after block: zipcode dictionary method: {miss}")

#Since there are still missing zipcodes why don't we do the same as above
#but with the street name as the key now

dfZip = dfTwo.loc[dfTwo['Zipcode'].notna()].groupby(['Street Name', "Zipcode"]).size().reset_index()
dic = dict(zip(dfZip['Street Name'], dfZip['Zipcode']))
dfTwo.loc[dfTwo['Zipcode'].isna(), "Zipcode"] = dfTwo.loc[dfTwo['Zipcode'].isna(), 'Street Name'].map(dic)

#See if there are still missing zipcodes
miss = numberRows - dfTwo.loc[dfTwo['Zipcode'].notna()].shape[0]
print(f"Missing zipCodes after street Name: zipcode dictionary method: {miss}")

#since there are still missing zipcodes let's create a function that actually searches for the
# coordinates and retrieves us the zipCode, we're gonna need the geopy library

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="HTTP")

def searchZip(x):
  coordinates = x['Location'][1:-1]
  #Search with the coordinates
  location = geolocator.reverse(coordinates)
  locInfo = location.raw
  print(locInfo, "\n")
  theZipCode = locInfo['address']['postcode']
  x['Zipcode'] = theZipCode
  return x

#Apply it to our df and see if there are still any missing zipcodes
dfTwo.loc[dfTwo['Zipcode'].isna()] = dfTwo.loc[dfTwo['Zipcode'].isna()].apply(searchZip, axis = 1)
print()
dfTwo.info()