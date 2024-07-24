import openai
from src.shared.environments import Environments


def load_openai(user_prompt):
    if not user_prompt:
        raise ValueError("User prompt is required to generate response.")
    str(user_prompt)
    try:
        api_key = Environments.get_envs().open_ai_api_key
        if not api_key:
            raise ValueError(
                "API Key for OpenAI not found in environment variables.")

        openai.api_key = api_key
        model = Environments.get_envs().open_ai_model
        system_prompt = Environments.get_envs().prompt

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=4096,
        )
        response_text = response['choices'][0]['message']['content']
        return response_text

    except Exception as e:
        print(f"An error occurred: {e}")
