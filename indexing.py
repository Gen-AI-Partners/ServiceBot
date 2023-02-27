# This is a sample Python script.
from dotenv import load_dotenv
from pathlib import Path
from gpt_index import GPTSimpleVectorIndex,SimpleDirectoryReader
from gpt_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper
import os
import inspect
from ServiceBot import StavrosPromptTemplate
from gpt_index import (
    GPTKeywordTableIndex,
    SimpleDirectoryReader,
    LLMPredictor
)
from langchain import Cohere

def get_source_code(function_name):
    # Get the source code of the function
    return inspect.getsource(function_name)

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def get_local_auth(envpath,v):
    dotenv_path = Path(envpath)
    load_dotenv(dotenv_path=dotenv_path)
    return os.getenv(v)

def generate_index(pages, max_input_size=4096,num_output=256,max_chunk_overlap=20):
    # define LLM

    #failed attempt to use Cohere - embedding not recognizing Cohorer LLM and still calling OpenAI
    #cohere = Cohere(temperature=.5, k=5)
    #llm_predictor = LLMPredictor(llm=cohere)
    #get_local_auth('CRED.env', 'COHERE_API_KEY')
    #LLMPredictor(llm=Cohere(temperature=.5, k=5))

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
    documents = SimpleDirectoryReader('data').load_data()
    index = GPTSimpleVectorIndex(
        documents, prompt_helper=prompt_helper
    )
    index.save_to_disk('index.json')
    return index

def create_index(folder):
     # get embeddings for confluence data
    get_local_auth('CRED.env', 'OPENAI_API_KEY')
    #get_local_auth('CRED.env', 'COHERE_API_KEY')
    # construct index
    index = generate_index(folder)
    return index

def query_index(prompt):
    get_local_auth('CRED.env', 'OPENAI_API_KEY')
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(prompt)
    print(response)



def main():
    # Use a breakpoint in the code line below to debug your script.
    print('hi')  # Press ⌘F8 to toggle the breakpoint.
    create_index('data')
    sms = "What should i get for a healthy dinner?"
    StavrosPrompt = StavrosPromptTemplate(input_variables=["question"])
    prompt=(StavrosPrompt.format(question=sms))
    query_index(prompt)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
