import os
from openai import AsyncOpenAI
# from exceptions.exceptions import MissingEnvironmentVariable


class OpenAIInterface():

    def __init__(self, gpt_model):
        self.client = AsyncOpenAI()
        self.GPT_MODEL = gpt_model
        self.messages = []
    

    async def start_chat(self, system_message: str, user_message: str, json: bool = False):
        try:
            self.messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]

            response_format = {"type": "json_object"} if json else None
            
            response = await self.client.chat.completions.create(
                model=self.GPT_MODEL,
                messages=self.messages,
                max_tokens=4095,
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format=response_format
            )

            response_content = response.choices[0].message.content
            print("Total tokens:", response.usage.total_tokens)
            print("Number of prompt tokens:", response.usage.prompt_tokens)
            print("Number of completion tokens:", response.usage.completion_tokens)
            return {'content': response_content, 'tokens_used': response.usage.total_tokens}
        except Exception as e:
            print(f"An error has occured: {e}")
            return None

    def add_chat(self, user_message: str):
        try:
            self.messages.append(user_message)
            
            response = self.client.chat.completions.create(
                model=self.GPT_MODEL,
                messages=self.messages,
                max_tokens=4095,
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={"type": "json_object"}
            )

            response_content = response.choices[0].message.content
            # print(response_content)
            print("Total tokens:", response.usage.total_tokens)
            print("Number of prompt tokens:", response.usage.prompt_tokens)
            print("Number of completion tokens:", response.usage.completion_tokens)
            return response_content
        except Exception as e:
            print(f"An error has occured: {e}")
            return None
    