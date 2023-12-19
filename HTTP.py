import requests
import time
import ast

class Request:

    def __init__(self, url, data=None, headers=None):
        self.url = url
        self.headers = headers
        self.data = data

    def get(self):
        resp = requests.get(self.url, headers=self.headers)
        
        if resp.status_code >= 200 and resp.status_code <= 299:
            return resp.text
        elif resp.status_code >= 400:
            print("something went wrong with get request")
            return resp.status_code
        
    def post(self):

        resp = requests.post(self.url, 
                      json=self.data,
                      headers=self.headers)
        
        if resp.status_code >= 200 and resp.status_code <= 299:
            return resp
        elif resp.status_code >= 400:
            raise Exception(f'Something went wrong with post request! Errror {resp.status_code}')
            
        
    def audio_complete_callback(request_audio):
        lapsed_time = 0
        resp = request_audio.get()
        status = ast.literal_eval(resp)["data"]["attributes"]["status"]

        while(status != 'done'):
            resp = request_audio.get()
            status = ast.literal_eval(resp)["data"]["attributes"]["status"]
            time.sleep(3)
            lapsed_time += 3
            if lapsed_time > 30:
                raise Exception("Timeout Error") 

        return resp

