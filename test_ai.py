import asyncio
import api_client

def test_ai():
    print("Testing AI Client...")
    
    # Test message 1
    response1 = api_client.get_ai_response("12345", "Faee", "Hi, my name is Faee!")
    print(f"User: Hi, my name is Faee!")
    print(f"Bot: {response1}")
    
    # Test message 2
    response2 = api_client.get_ai_response("12345", "Faee", "What is my name?")
    print(f"User: What is my name?")
    print(f"Bot: {response2}")
    
    print("Testing done.")

if __name__ == "__main__":
    test_ai()
