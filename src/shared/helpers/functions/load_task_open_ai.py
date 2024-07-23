import openai
from src.shared.environments import Environments

def load_openai(system_prompt, user_prompt):
    api_key = Environments.get_envs().open_ai_api_key
    if not api_key:
        raise ValueError("API Key for OpenAI not found in environment variables.")

    openai.api_key = api_key
    model = Environments.get_envs().open_ai_model
    prompt = Environments.get_envs().prompt

    try:
        response = openai.ChatCompletion.create(
            model=model,
            system_prompt=prompt,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=200,
        )
        response_text = response['choices'][0]['message']['content']
        print(response_text)

    except Exception as e:
        print(f"An error occurred: {e}")

system_prompt = "Your system prompt here"
user_prompt = "Your user prompt here"
load_openai(system_prompt, user_prompt)
