"""
List available models for the routing API key
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

routing_key = os.environ.get('API_GUESSING_MODELKEY')

print("="*70)
print("CHECKING AVAILABLE MODELS FOR ROUTING KEY")
print("="*70)
print(f"\nRouting API Key: {routing_key[:20]}...\n")

genai.configure(api_key=routing_key)

print("Available models:")
print("-" * 70)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"✅ {m.name}")
        print(f"   Display Name: {m.display_name}")
        print(f"   Description: {m.description[:80]}..." if len(m.description) > 80 else f"   Description: {m.description}")
        print()

print("="*70)
