import tornado.ioloop
import tornado.web
import json

# Enable CORS (Cross-Origin Resource Sharing)in Tornado Backend for local development. 
# Because frontend (React) and backend (Tornado) are served from different origins we need to allow CORS in our Tornado application.
# This is achieved by overriding the set_default_headers method in your MainHandler to include the necessary CORS headers

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    
    def post(self):
        # Your existing POST method logic
        # Extract the data from the body of the request
        data = json.loads(self.request.body)
        prompt = data.get('prompt')

        # Process the prompt here and generate a response
        response = f"Received prompt: {prompt}"

        # Send the response back to the client
        self.write(response)
    
    def options(self):
        # No body, just to handle pre-flight requests for CORS
        self.set_status(204)
        self.finish()
        

def make_app():
    return tornado.web.Application([
        (r"/api", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/Users/Jonathan_1/Downloads/R-DeepCodeRED/r-deep-demo/src"}),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
