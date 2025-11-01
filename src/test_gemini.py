import google.generativeai as genai
import os
from dotenv import load_dotenv
import pathlib

# Load .env file
env_path = pathlib.Path(__file__).parent.parent / '.env'
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

# Get API key
api_key = os.getenv('SECRET_KEY')
print(f"\nAPI Key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key: {api_key[:20]}...\n")

# Test Gemini API
try:
    print("Configuring Gemini...")
    genai.configure(api_key=api_key)
    
    print("Creating model...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("Testing simple query...")
    response = model.generate_content("Say 'Hello, I am working!'")
    
    print("\n" + "="*60)
    print("SUCCESS! Gemini API is working!")
    print("="*60)
    print(f"Response: {response.text}")
    print("="*60)
    
except Exception as e:
    print("\n" + "="*60)
    print("ERROR! Gemini API failed!")
    print("="*60)
    print(f"Error: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    print("="*60)
    
    import traceback
    traceback.print_exc()
