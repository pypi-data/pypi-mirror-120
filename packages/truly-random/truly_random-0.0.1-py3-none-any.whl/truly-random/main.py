import requests
import json

class TrulyRandom():
    def __init__(self,api_key:str):
        self.api_key = api_key
        self.url = 'https://api.random.org/json-rpc/4/invoke'
        pass
    
    def generateIntegers(self,number,min,max):
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateIntegers",
            "params": {
                "apiKey": self.api_key,
                "n": number,
                "min": min,
                "max": max,
                "replacement": True
            },
            'id':1
        }

        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url=self.url,
            data=data,
            headers=headers
            )

        return(json.loads(response.text)['result']['random']['data'])


    def generateIntegerSequences(self,number:int,length,min,max):
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateIntegerSequences",
            "params": {
                "apiKey": self.api_key,
                "n": number,
                "length": length,
                "min": min,
                "max": max,
                "replacement": [False, False],
                "base": [10, 10]
            },
            "id": 2
        }
        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url=self.url,
            data=data,
            headers=headers
            )

        return(json.loads(response.text)['result']['random']['data'])

    
    def generateDecimalFractions(self,number,decimalPlaces):
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateDecimalFractions",
            "params": {
                "apiKey": self.api_key,
                "n": number,
                "decimalPlaces": decimalPlaces,
                "replacement": True
            },
            "id": 3
        }
        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url=self.url,
            data=data,
            headers=headers
            )

        return(json.loads(response.text)['result']['random']['data'])


    def generateGaussians(self,number:int,mean,standardDeviation,significantDigits):
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateGaussians",
            "params": {
                "apiKey": self.api_key,
                "n": number,
                "mean": mean,
                "standardDeviation": standardDeviation,
                "significantDigits": significantDigits
            },
            "id": 4
        }
        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url=self.url,
            data=data,
            headers=headers
            )

        return(json.loads(response.text)['result']['random']['data'])


    def generateStrings(self,number,length):
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateStrings",
            "params": {
                "apiKey": self.api_key,
                "n": number,
                "length": length,
                "characters": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "replacement": True
            },
            "id": 5
        }
        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url=self.url,
            data=data,
            headers=headers
            )

        return(json.loads(response.text)['result']['random']['data'])


    def generateUUIDs(self,number):
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateUUIDs",
            "params": {
                "apiKey": self.api_key,
                "n": number
            },
            "id": 15998
        }
        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url=self.url,
            data=data,
            headers=headers
            )

        return(json.loads(response.text)['result']['random']['data'])


    def generateBlobs(self,number,size):
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateBlobs",
            "params": {
                "apiKey": self.api_key,
                "n": number,
                "size": size
            },
            "id": 42
        }
        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url=self.url,
            data=data,
            headers=headers
            )

        return(json.loads(response.text)['result']['random']['data'])








#random = TrulyRandom('914af858-2834-40e7-ab08-27955e69fd41')
#print(random.generateIntegerSequences(2,5,1,100))