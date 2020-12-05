from fastapi import APIRouter, HTTPException
import pandas as pd
import requests
import pprint
import datetime
import numpy as np

router = APIRouter()

@router.get('/getHistoricalData/{name}')
async def rise(NAME: str, METRIC: str, startDate: str, endDate: str):
    """
    Valid inputs:   
    NAME: STEINAKER  
    METRIC: STORAGE, EVAPORATION, INFLOW, ELEVATION, RELEASE, DELTA STORAGE, AREA  
    StartDate: 1950-01-01  
    EndDate: Current Date  
    **********************

    Returns historical data from the Bureau of Reclamation's [RISE catalog](https://data.usbr.gov/catalog).

    [Link](https://data.usbr.gov/rise/api/) to RISE api documentation
    """
    # user can input a name, start date, end date, and metric and receive historical data in return
    # capitalize the inputs
    name = NAME.upper()
    metric = METRIC.upper()
    start = startDate
    end = endDate

    '''
    I had to hard code this dictionary, by going to the RISE API myself and finding this information manually,
    but in an ideal world, we would have this information stored in our own database along with some of the other 
    information which would decrease the number of calls to the RISE API we'd have to make and improve our latency.
    '''
    # MAKE SURE THIS DICTIONARY IS UP TO DATE
    bodies = dict()
    bodies['STEINAKER'] = {'CODE': 2454}
    bodies['STEINAKER']['METRICS'] = {'STORAGE': [774], 'EVAPORATION': [775], 
                                    'INFLOW': [776, 4479], 'ELEVATION': [778], 'RELEASE': [4318, 4478],
                                    'DELTA STORAGE': [4477], 'AREA': [4809] }
    #####################################

    # extract the id from our dictionary
    ids = bodies[name]['METRICS'][metric]
    id = ids[0] # for now, we are just going to use the first id that appears in the list

    # get the historical data from the specified time range
    url = f'https://data.usbr.gov/rise/api/result?itemId={id}&dateTime%5Bbefore%5D={end}&dateTime%5Bafter%5D={start}&itemsPerPage=1000000'
    r = requests.get(url).json()


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

    

    final_result = dict()

    # get the units
    paramid = r['data'][0]['attributes']['parameterId']
    params = getParams(paramid)
    units = params[1]

    # store the values in a list to perform calculations
    calculations = []

    # restructure the result
    for dictionary in r['data']:
    # convert string to datetime
        date_time = dictionary['attributes']['dateTime']

        result = dictionary['attributes']['result']

        final_result[date_time] = [result, units]

        calculations.append(result)

    # perform calculations on the list of values
    avg = np.mean(calculations)
    med = np.median(calculations)
    max = np.max(calculations)
    min = np.min(calculations)
    range = max-min
    calculations = dict()
    calculations['average'] = avg
    calculations['median'] = med
    calculations['maximum'] = max
    calculations['minimum'] = min
    calculations['range'] = range
    
    return calculations, final_result