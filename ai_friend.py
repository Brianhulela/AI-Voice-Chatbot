import speech_recognition as sr
import os
from dotenv import load_dotenv
import pyttsx3
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
import pygame

# Initialize pygame
pygame.init()

# Load a sound file
prompt_sound_file = "mixkit-high-tech-bleep-confirmation.wav"
ai_thinking_sound_file = "mixkit-futuristic-sci-fi-computer-ambience.wav"
ai_response_sound_file =  "mixkit-robotic-glitch.wav"

ai_thinking_sound = pygame.mixer.Sound(ai_thinking_sound_file)
prompt_sound = pygame.mixer.Sound(prompt_sound_file)
ai_response_sound = pygame.mixer.Sound(ai_response_sound_file)

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

engine = pyttsx3.init()

# Configure voice (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Set properties (optional)
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        # Play the sound
        prompt_sound.play()

        # Allow the sound to play for a while before quitting
        pygame.time.wait(500)

        # Quit pygame
        #pygame.quit()
        ai_thinking_sound.stop()
        print("Say something...")
        audio = recognizer.listen(source)
    try:
        ai_thinking_sound.play()
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
    engine.say(model_response)
    engine.runAndWait()
       

def conversation():
    user_input = ""
    while True:
        user_input = listen()
        if user_input is None:
            user_input = listen()

        elif "bye" in user_input.lower():
            ai_response_sound.play()
            pygame.time.wait(1000)
            respond(conversation_chain.run({"question": "Send a friendly goodbye question and give a nice short sweet compliment based on the conversation."}))
            return
        
        else:
            model_response = prompt_model(user_input)
            ai_thinking_sound.stop()
            ai_response_sound.play()
            pygame.time.wait(1000)
            respond(model_response)
        

if __name__ == "__main__":
    respond(conversation_chain.run({"question": "Greet me in a friendly way"}))
    conversation()