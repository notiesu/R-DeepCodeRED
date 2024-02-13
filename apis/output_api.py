from dotenv import load_dotenv
import time
load_dotenv() # Load .env file
from openai import OpenAI


class Output_API:
    def __init__(self):
        
        # self.assistant_id = 'REMOVED'
        self.assistant_id = 'REMOVED'
        self.load_openai_client_and_assistant()
        
    def load_openai_client_and_assistant(self):
        print('this is called')
        self.client = OpenAI()
        self.my_assistant = self.client.beta.assistants.retrieve(self.assistant_id)
        self.assistant_thread = self.client.beta.threads.create()

        
    def wait_on_run(self, run):
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.assistant_thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run
    
    def get_assistant_response(self, user_input=""):

        message = self.client.beta.threads.messages.create(
            thread_id=self.assistant_thread.id,
            role="user",
            content=user_input,
        )

        run = self.client.beta.threads.runs.create(
            thread_id=self.assistant_thread.id,
            assistant_id=self.assistant_id,
        )

        run = self.wait_on_run(run)

        # Retrieve all the messages added after our last user message
        messages = self.client.beta.threads.messages.list(
            thread_id=self.assistant_thread.id, order="asc", after=message.id
        )

        return messages.data[0].content[0].text.value, messages
