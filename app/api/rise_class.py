import requests
import pprint


class Rise:
    # have a dictionary that holds the possible reservoir's of our clients

    def __init__(self, name):

        # MAKE SURE THIS DICTIONARY IS UP TO DATE
        bodies = dict()
        bodies['steinaker'] = 2454
        bodies['redfleet'] = 2416
        bodies['flaming'] = 2300
        ##########################################
        
        self.name = name
        self.bodies = bodies
        # refers to the catalog record id used by RISE api
        self.catalogRecord = bodies[name]
        # refers to the catalogItems used by RISE api
        self.catalogItems = self.extractId()
        self.data = self.getData()
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


    def getData(self):
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

    def getResults(self):
        '''
        Returns the results from the data
        '''
        data = self.data
        matrix = []
        for i in range(0, len(data)):
            name = self.name
            datetime = data[i]['data'][0]['attributes']['dateTime']
            result = data[i]['data'][0]['attributes']['result']
            # get the unit id
            paramid = data[i]['data'][0]['attributes']['parameterId']
            # get the parameters
            params = self.getParams(paramid)
            units = params[1]
            description = params[0]
            # update params
            self.params.append([units, description])

            new_data = [datetime, name, description, result, units]
            matrix.append(new_data)

        return matrix 

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

