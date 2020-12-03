import requests
import pprint

### helper functions ###
def getParams(paramid):
        '''
        Takes a parameter id as an argument
        Returns a list of parameters/units for each result
        '''
        url = f'https://data.usbr.gov/rise/api/parameter/{paramid}'
        r = requests.get(url).json()
        parameterUnit = r['data']['attributes']['parameterUnit']
        parameterName = r['data']['attributes']['parameterName']


        return [parameterName, parameterUnit]

########################################################################

# user can input a name, start date, end date, and metric and receive historical data in return
name = 'steinaker'
metric = 'inflow'
start = '2018-01-01'
end = '2019-01-01'

# MAKE SURE THIS DICTIONARY IS UP TO DATE
bodies = dict()
bodies['STEINAKER'] = {'CODE': 2454}
bodies['STEINAKER']['METRICS'] = {'STORAGE': [774], 'EVAPORATION': [775], 
                                'INFLOW': [776, 4479], 'ELEVATION': [778], 'RELEASE': [4318, 4478],
                                'DELTA STORAGE': [4477], 'AREA': [4809] }

metrics = ['STORAGE', 'EVAPORATION', 'INFLOW', 'ELEVATION', 'RELEASE', 'DELTA STORAGE', 'AREA']
#####################################

# capitalize the inputs
name = name.upper()
metric = metric.upper()

# extract the id
ids = bodies[name]['METRICS'][metric]
id = ids[0] # for now, we are just going to use the first id that appears in the list

# get the historical data from the specified time range
url = f'https://data.usbr.gov/rise/api/result?itemId={id}&dateTime%5Bbefore%5D={end}&dateTime%5Bafter%5D={start}&itemsPerPage=1000000'
r = requests.get(url).json()

final_result = dict()

# get the units
paramid = r['data'][0]['attributes']['parameterId']
params = getParams(paramid)
units = params[1]

# restructure the result
for dictionary in r['data']:
# convert string to datetime
    date_time = dictionary['attributes']['dateTime']

    result = dictionary['attributes']['result']

    final_result[date_time] = [result, units]

pprint.pprint(final_result)


