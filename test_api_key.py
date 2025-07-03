import os
from dotenv import load_dotenv
from openai import OpenAI
import sys

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
model = os.getenv('DEFAULT_MODEL', 'deepseek/deepseek-chat')

print(f'Testing OpenRouter API with model: {model}')

# Check if API key is valid
if not api_key or not api_key.startswith('sk-or-'):
    print(f'API Key from environment: {api_key}')
    print('\nWARNING: The API key does not appear to be a valid OpenRouter API key.')
    print('Valid OpenRouter keys should start with "sk-or-"')
    
    # Use the hardcoded key from .env file
    api_key = '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'
    print(f'\nUsing hardcoded API key instead: {api_key[:10]}...{api_key[-5:]}')
else:
    print(f'API Key from environment: {api_key[:10]}...{api_key[-5:]}')

print(f'API Key length: {len(api_key) if api_key else 0}')

try:
    # Initialize OpenAI client with OpenRouter base URL
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://toolswebsite.com",  # Required by OpenRouter
            "X-Title": "Tools Website"  # Optional, but helps OpenRouter identify your app
        }
    )
    
    # Make a simple test request
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, are you working?"}
        ],
        max_tokens=50
    )
    
    print('\nAPI Response:')
    print(response.choices[0].message.content)
    print('\nAPI Key is working correctly!')
except Exception as e:
    print(f'\nError: {str(e)}')
    print('\nAPI Key may not be valid or there might be connection issues.')
    sys.exit(1)