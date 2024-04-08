from openai import OpenAI

def generate_llm_response(messages):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=messages,
        temperature=0
    )
    answer = response.choices[0]
    return answer.message.content#, answer.usage