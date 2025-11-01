import google.generativeai as genai
import os
from dotenv import load_dotenv
import pathlib

# Load .env file
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key
api_key = os.getenv('SECRET_KEY')
print(f"API Key: {api_key[:20]}...\n")

try:
    genai.configure(api_key=api_key)
    
    print("="*60)
    print("AVAILABLE MODELS FOR YOUR API KEY:")
    print("="*60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"\nModel: {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print(f"  Supported: {model.supported_generation_methods}")
    
    print("\n" + "="*60)
    
except Exception as e:
    print(f"\nError listing models: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    
    # The API key might not be valid for Gemini
    print("\n" + "="*60)
    print("IMPORTANT:")
    print("="*60)
    print("Your API key might not be a valid Gemini/Google AI API key.")
    print("Please verify you got the key from: https://makersuite.google.com/app/apikey")
    print("="*60)
