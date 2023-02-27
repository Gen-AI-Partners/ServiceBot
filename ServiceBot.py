from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
from pathlib import Path
from gpt_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper
from langchain.prompts import BasePromptTemplate
from pydantic import BaseModel, validator


class StavrosPromptTemplate(BasePromptTemplate, BaseModel):
    """ A custom prompt template that takes in the function name as input, and formats the prompt template to provide the source code of the function. """

    @validator("input_variables")
    def validate_input_variables(cls, v):
        """ Validate that the input variables are correct. """
        if "question" not in v:
            raise ValueError("question must be an input_variable.")
        return v

    def format(self, **kwargs) -> str:
        # Get the source code of the function

        # Generate the prompt to be sent to the language model
        prompt = f"""
        Answer the question concisely while pretending you are an old Greek grandpa (with 4 grandkids) named Stavros excited to have people experience your Greek culture at Little Greek Fresh Grill.
        Also include connections from responses to your childhood stories in Mykonos.  Tell people your name if it seems relevant.
        You can also tell them about your favorite Greek foods (Feta Cheese, Pastitsio and Lamb Gyro are some but you can make up others), and how you make them. Keep responses to under 4 sentences.
        
        Question:{kwargs["question"]}
        """
        return prompt

    def _prompt_type(self):
        return "service-bot"

app = Flask(__name__)
@app.route('/bot', methods=['POST'])
#out of the box tutorial from Twilio
def bot():
    #how to process message
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    #opentional logic
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)
@app.route('/ServiceBot', methods=['POST'])
def stavros():
    #process incoming message
    incoming_msg = request.values.get('Body', '').lower()
    #create response object
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    #call index to query
    StavrosPrompt = StavrosPromptTemplate(input_variables=["question"])
    prompt = (StavrosPrompt.format(question=incoming_msg))
    response = index.query(prompt)
    # print to show in terminal
    print(incoming_msg)
    msg.body(str(response))
    print(response)
    responded = True
    return str(resp)
@app.route('/', methods=['GET'])
def index():
    return 'Web interface for ServiceBot coming soon!'
    #expand to web UI
    #return render_template('index.html', messages=["hi", "hello"])

if __name__ == '__main__':
    #load index
    dotenv_path = Path('CRED.env')
    load_dotenv(dotenv_path=dotenv_path)
    os.getenv('OPENAI_API_KEY')
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    #run the app
    app.run(host="localhost",port=5003,debug=True)
