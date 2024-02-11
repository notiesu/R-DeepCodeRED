import tornado.ioloop
import tornado.web
import json
from nlp_api import NLP_API
import os
import time
import json

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")  # Include Content-Type
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    
    
    def parse_json(self, response):
        if 'JSON' in response or 'json' in response:
            json_str_start = response.find('{')
            json_str_end = response.rfind('}') + 1
            json_str = response[json_str_start:json_str_end]
            print(json_str)
            # Parse the JSON string into a Python dictionary
            json_data = json.loads(json_str)
            
            # call the travel api
            
        else:
            return response
        
    
    def post(self):
        data = json.loads(self.request.body)
        prompt = data.get('prompt')
        nlp_api = self.application.settings.get('nlp_api')
        response, mess = nlp_api.get_assistant_response(prompt)
        
        response = self.parse_json(response)
            # call parse
        self.write(response)
    
    def options(self):
        self.set_status(204)
        self.finish()
        

def make_app():
    nlp_api = NLP_API()
    # nlp_api = None
    return tornado.web.Application([
        (r"/api", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "..\r-deep-demo\src"}),
    ], nlp_api=nlp_api)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
