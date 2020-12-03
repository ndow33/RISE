import requests
import pprint
import datetime

# helper functions
def toDateTime(time):
    # format the string in the proper ISO 8601 format
    date_time = time.split("T")
    date_time = date_time[0]
    date_time_obj = datetime.datetime.strptime(date_time, '%Y-%m-%d')
    return date_time_obj



class Rise:
    # have a dictionary that holds the possible reservoir's of our clients

    def __init__(self, name):

        # MAKE SURE THIS DICTIONARY IS UP TO DATE
        bodies = dict()
        bodies['steinaker'] = {'CODE': 2454}
        bodies['redfleet'] = 2416
        bodies['flaming'] = 2300
        ##########################################
        
        self.name = name
        self.bodies = bodies
        # refers to the catalog record id used by RISE api
        self.catalogRecord = bodies[name]['CODE']
        # refers to the catalogItems used by RISE api
        self.catalogItems = self.extractId()
        self.data = self.getMostRecentData()
        self.params = []
        self.results = self.getResults()
        


    def __str__(self):
        string = str(pprint.pprint(self.results))
        return string
        


    def getCatItems(self):
        '''
        Get the catalog items by using the catalog record id
        '''
        # make the request to the appropriate url
        url = f'https://data.usbr.gov/rise/api/catalog-record/{self.catalogRecord}'
        # turn it into a json object
        r = requests.get(url).json()
        r = r['data']['relationships']['catalogItems']['data']
        return r


    def extractId(self):
        '''
        Extract the id's of the catalog items in order to get the results desired
        '''
        # create an empty list to hold id's
        ids = []
        # get the id's
        r = self.getCatItems()
        # get the id's
        for i in range(0, len(r)):
            code = r[i]['id']
            # split the string
            code = code.split('/')
            # get the code
            code = code[-1]
            # append it to the list
            ids.append(code)

        # return a list of id's
        return ids


    def getMostRecentData(self):
        '''
        Returns only the most recent data for each catalog item
        '''
        data = []
        for item in self.catalogItems:
            url = f'https://data.usbr.gov/rise/api/result?itemId={item}&itemsPerPage=1'
            r = requests.get(url).json()
            # add it to our data
            data.append(r)
        return data

    
    # def getHistoricalData(self, )



    def getResults(self):
        '''
        Returns the results from the data
        '''
        data = self.data
        matrix = []
        for i in range(0, len(data)):
            # convert string to datetime
            date_time = data[i]['data'][0]['attributes']['dateTime']
            date_time = toDateTime(date_time)
            name = self.name
            result = data[i]['data'][0]['attributes']['result']
            # get the unit id
            paramid = data[i]['data'][0]['attributes']['parameterId']
            # get the parameters
            params = self.getParams(paramid)
            description = params[0]
            units = params[1]
            # update params
            self.params.append([units, description])

        

            new_data = [date_time, name, description, result, units]
            matrix.append(new_data)

        return matrix 



    def getResultsDictionary(self):
        '''
        Returns the results from the data as a dictionary
        '''
        data = self.data
        dictionary = dict()

        # get the date in datetime format
        date_time = data[0]['data'][0]['attributes']['dateTime']
        date_time = toDateTime(date_time)

        # name = steinaker, redfleet, etc.
        name = self.name

        dictionary['DATETIME'] = date_time
        dictionary['ENTITY'] = name

        for i in range(0, len(data)):            
            result = data[i]['data'][0]['attributes']['result']
            # get the unit id
            paramid = data[i]['data'][0]['attributes']['parameterId']
            # get the parameters
            params = self.getParams(paramid)
            description = params[0]
            units = params[1]
            # update params
            self.params.append([units, description])
            # create a sub dictionary to hold the value and the units
            sub_dictionary = dict()
            sub_dictionary['VALUE'] = result
            sub_dictionary['UNITS'] = units
            # add the sub dictionary to the dictionary
            dictionary[description] = sub_dictionary
        return dictionary 



    def getParams(self, paramid):
        '''
        Takes a parameter id as an argument
        Returns a list of parameters/units for each result
        '''
        url = f'https://data.usbr.gov/rise/api/parameter/{paramid}'
        r = requests.get(url).json()
        parameterUnit = r['data']['attributes']['parameterUnit']
        parameterName = r['data']['attributes']['parameterName']


        return [parameterName, parameterUnit]

