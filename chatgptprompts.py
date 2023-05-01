import requests
import json
import openai
import os


class ChatBot:
    def __init__(self) -> None:
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        self.messages = [
            {"role": "system", "content": "You are a kind helpful social media assistant."},
        ]


    def querychatgpt(self, initmessage,stat):
        message = f"You are a helpful social media assistant. A user asks '{initmessage}'. The answer to this question is '{str(stat)}'. Please write a response to that."
        # print(message)

        self.messages.append(  {"role": "user", "content": message},)

        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)

        reply = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply
    
# c = ChatBot()

# print(c.querychatgpt( "what was the average amount of likes i got in the last month?",12))