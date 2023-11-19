import speech_recognition as sr
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from voice import Voice

# load the environment variables
load_dotenv()

# Initialise the Large Language Model
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=1, 
    model_name='gpt-4'
    )

# Create a prompt template
template = """You are a chatbot that is friendly and has a great sense of humor.
Don't give long responses and always feel free to ask interesting questions that keeps someone engages.
You should also be a bit entertaining and not boring to talk to. Use informal language
and be curious.

Previous conversation:
{chat_history}

New human question: {question}
Response:"""

# Create a prompt template
prompt = PromptTemplate.from_template(template)

# Create some memory for the agent
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialise the conversation chain
conversation_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True, 
    memory=memory
)

# initialize the voice instance
model_voice = Voice()

# initialise the voice recognizer
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)
        
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)   # speech to text
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        print("Recognizing...")

def prompt_model(text):
    # Prompt the LLM chain
    response = conversation_chain.run({"question": text})
    return response

def respond(model_response):
    # Run the speech synthesis
    response_id = model_voice.generate_voice(model_response)
    model_voice.play_voice(response_id)   

def conversation():
    user_input = ""
    
    while True:
        user_input = listen()
        if user_input is None:
            user_input = listen()

        elif "bye" in user_input.lower():
            respond(conversation_chain.run({"question": "Send a friendly goodbye question and give a nice short sweet compliment based on the conversation."}))
            return
        
        else:
            model_response = prompt_model(user_input)
            respond(model_response)
        

if __name__ == "__main__":
    respond(conversation_chain.run({"question": "Greet me in a friendly way."}))
    conversation()