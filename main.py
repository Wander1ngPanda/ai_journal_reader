from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(completion.choices[0].message.content)