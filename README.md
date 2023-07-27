

# Hermetic

Hermetic is a library that makes it easy to develop, test, evaluate and deploy LLM Applications. 


# Quick start guide

These particular instructions are focused on Anyscale Endpoints, but they should generalize.  


## Prerequisites

Before you get started, you’ll need an Anyscale Endpoints key. You can get that from [https://console.endpoints.anyscale.com/credentials](https://console.endpoints.anyscale.com/credentials) (after you’ve entered your credit card). 

**Make sure you save this – it is only given once. **

You also need a clean python environment. 


### Install Hermetic, Langchain, Gradio, OpenAI libraries

To install these libraries, just install hermetic and hermetic will install the rest. Update pip first, since it seems to reduce installation time. 


### Create a .env file and put some environment variables in it

We need quite a few environment variables to get this demo working, so the easiest way is to put them in a .env file.

Add the following lines there: 

**NOTE: **It may seem weird that we are defining OPENAI_API_* variables when we want to connect to Anyscale. But this is because Anyscale offers an OpenAI compatible api. Note that you did not need to install any libraries to use Anyscale Endpoints specifically, it reuses the OpenAI python SDK. 

And now to load them


### Create a system prompt

Now  create a simple file 

resources/prompts/system_prompt.txt

That contains


### Create a Langchain-based agent that uses Anyscale Endpoints

Create a file called pirate.py that contains the following: 

Now connect to localhost:7860 in your browser and you should be able to talk to a pirate! 
