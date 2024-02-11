import tornado.ioloop
import tornado.web
import json
from nlp_api import NLP_API
import os
import time
import json

from flight_api import travelapi
from output_api import Output_API


global_call = False
class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")  # Include Content-Type
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    
    
    def parse_json(self, response, travel_api, output_API):
        
        
        print(response)
        if 'JSON' in response or 'json' in response:
            json_str_start = response.find('{')
            json_str_end = response.rfind('}') + 1
            json_str = response[json_str_start:json_str_end]
            
            # Parse the JSON string into a Python dictionary
            json_data = json.loads(json_str)
            print('pasrse')
            output_df = travel_api.first(json_data)
            
            output_json = output_df.to_json(orient='records', lines=False)
            ## send to the user api
            
            
            return True, output_json
            # return 
            
        else:
            return False, response
        
    
    def post(self):
        global global_call
        data = json.loads(self.request.body)
        prompt = data.get('prompt')
        
        nlp_api = self.application.settings.get('nlp_api')
        travel_api = self.application.settings.get('travel_api')
        output_API = self.application.settings.get('output_API')
        

        if global_call:
            nlp_api = output_API
            
            
        response, mess = nlp_api.get_assistant_response(prompt)
        var, response = self.parse_json(response, travel_api, output_API)
        print(var)
        if var:
            
            print('this is running')
            response = output_API.get_assistant_response(response)[0]
            global_call = True
        # print(response)
            # call parse
        
        self.write(response)
    
    def options(self):
        self.set_status(204)
        self.finish()
        

def make_app():
    nlp_api = NLP_API()
    travel_api = travelapi()
    output_API = Output_API()
    # nlp_api = None
    return tornado.web.Application([
        (r"/api", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "..\r-deep-demo\src"}),
    ], nlp_api=nlp_api, travel_api=travel_api, output_API=output_API)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
