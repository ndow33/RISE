import requests
import pprint
import numpy as np

url = 'https://data.usbr.gov/rise/api/location?stateId=UT'
r = requests.get(url).json()

# get the name and the category record id for each site in utah in a dictionary
data = r['data']
cat_ids = dict()

# the list of bodies of water that we want information for
bodies = ['Steinaker Reservoir and Dam', 'Red Fleet Reservoir and Dam', 'Flaming Gorge Reservoir Dam and Powerplant']
#bodies = ['Steinaker Reservoir and Dam']

# iterate through the dictionary
for i in data:
    name = i['attributes']['locationName']
    locationid = i['id']
    catalogitems = i['relationships']['catalogItems']
    catalogrecordid = i['relationships']['catalogRecords']

    if name in bodies:
        cat_ids[name] = {'catalogRecords':catalogrecordid, 'catalogItems':catalogitems, 'locationId':locationid}


# convert catalog items to their metrics
# iterate through each body of water
# store the titles and urls in a new dictionary
results = dict()
for name in cat_ids:
    results[name] = []

    # iterate through each catalog item id for the body of water
    items = cat_ids[name]['catalogItems']['data']
    for item in items:

        # make a request to the rise api to get the itemTitle and the temporalParameterId
        url1 = 'https://data.usbr.gov'
        url2 = item['id']
        url = url1 + url2
        r = requests.get(url).json()
        title = r['data']['attributes']['itemTitle']

        # get the item code
        code = url.split('/')[-1]

        # get the result url
        url3 = '/rise/api/result/'
        url4 = url1 + url3 + code
        # add the title and the url to the dictionary
        results[name].append({'metric':title, 'catalogItemUrl':url, 'resultUrl': url4})

        

my_file = open('codes.txt', 'w+')

# write the results to a txt file in a nice format
for name in results:
    my_file.write('################################################\n')
    my_file.write(name + '\n')
    my_file.write('################################################\n')
    my_file.write('\n')
    my_file.write('\n')
    for metric in results[name]:
        my_file.write(metric['metric']+ '\n')
        my_file.write(metric['catalogItemUrl']+ '\n')
        my_file.write(metric['resultUrl'] + '\n')
        my_file.write('\n')
        my_file.write('\n')