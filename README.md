# Conversational AI Chatbot with Speech Recognition

For more detailed instructions on how to build the chatbot, check out my article on [Medium](https://medium.com/@brianhulela/create-a-python-ai-voice-chatbot-with-speechrecognition-langchain-and-openai-gpt-3-5-turbo-c60f92f4a47c)

This project implements a conversational AI chatbot that uses the [Whisper](https://platform.openai.com/docs/guides/speech-to-text) model to transcribe user speech to text. It utilizes the OpenAI GPT-3.5-turbo/GPT-4 LLM for generating human-like responses. It then synthesizes the output into human-like audio speech output using [Text-to-speech](https://platform.openai.com/docs/guides/text-to-speech).

## Features

- Speech recognition: The chatbot listens to user speech input and converts it into text.
- Interactive responses: The chatbot uses the [Langchain](https://www.langchain.com/), GPT-3.5-turbo/GPT-4 model to generate context-aware and engaging responses.
- Voice output: The chatbot's responses are synthesized into speech using OpenAI [Text-to-speech](https://platform.openai.com/docs/guides/text-to-speech)
- Interactive conversation: The chatbot maintains a memory of past conversations to create a context-rich interaction.

## Usage

1. **Clone the repository to your local machine:**

    ```bash
    git clone https://github.com/Brianhulela/AI-Voice-Chatbot
    ```

2. **Navigate to the project directory:**

    ```bash
    cd AI-Voice-Chatbot
    ```

3. **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your OpenAI API key:**

    In the project directory, create a `.env` file and add the following line:
    
    ```
    YOUR_OPENAI_API_KEY='your-openai-api-key'
    ```
    
    Replace `'your-openai-api-key'` with your actual OpenAI API key in the `.env` file.

5. **Run the chatbot:**

    ```bash
    python ai_friend.py
    ```

    The chatbot will initiate a conversation by greeting you in a friendly manner. You can respond to the chatbot's prompts using your voice. To exit the conversation, say "bye".

## Notes

- Make sure you have an active internet connection to use the OpenAI API.
- You might need to adjust the microphone source in the `listen()` function if you have multiple audio devices.

## Acknowledgments

- This project uses the OpenAI GPT-3.5-turbo/GPT-4 model for generating responses.
