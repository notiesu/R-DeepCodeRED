import tornado.ioloop
import tornado.web
import json

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        # Extract the data from the body of the request
        data = json.loads(self.request.body)
        prompt = data.get('prompt')

        # Process the prompt here and generate a response
        response = f"Received prompt: {prompt}"

        # Send the response back to the client
        self.write(response)

def make_app():
    return tornado.web.Application([
        (r"/api", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/Users/Jonathan_1/Downloads/R-DeepCodeRED/r-deep-demo/src"}),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
