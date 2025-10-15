"""Script to test the Chatbot API endpoints."""
import requests
import json
import sys
from time import sleep

BASE_URL = "http://localhost:8000"


def print_separator(title=""):
    """Print a separator line."""
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)


def test_health():
    """Test health endpoint."""
    print_separator("1. Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_root():
    """Test root endpoint."""
    print_separator("2. Testing Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_create_conversation():
    """Test creating a conversation."""
    print_separator("3. Testing Create Conversation")
    try:
        data = {"title": "Test Conversation"}
        response = requests.post(
            f"{BASE_URL}/api/v1/conversations",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 201:
            return response.json()
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_list_conversations():
    """Test listing conversations."""
    print_separator("4. Testing List Conversations")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/conversations")
        print(f"Status: {response.status_code}")
        conversations = response.json()
        print(f"Found {len(conversations)} conversation(s)")
        print(f"Response: {json.dumps(conversations, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_send_message(conversation_id):
    """Test sending a message."""
    print_separator("5. Testing Send Message (with AI response)")
    try:
        data = {"content": "Bonjour! Peux-tu me dire une blague sur Python?"}
        response = requests.post(
            f"{BASE_URL}/api/v1/conversations/{conversation_id}/messages",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")

        if response.status_code == 201:
            message = response.json()
            print(f"AI Response:")
            print(f"  Role: {message['role']}")
            print(f"  Content: {message['content']}")
            return True
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_get_messages(conversation_id):
    """Test getting conversation messages."""
    print_separator("6. Testing Get Conversation Messages")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/conversations/{conversation_id}/messages"
        )
        print(f"Status: {response.status_code}")
        messages = response.json()
        print(f"Found {len(messages)} message(s)")

        for i, msg in enumerate(messages, 1):
            print(f"\nMessage {i}:")
            print(f"  Role: {msg['role']}")
            print(f"  Content: {msg['content'][:100]}...")

        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    print_separator("Supabase Chatbot API Test Suite")
    print(f"Testing API at: {BASE_URL}")
    print("\nMake sure the server is running with:")
    print("  PYTHONPATH=. python main.py")

    # Wait for user confirmation
    input("\nPress Enter to start tests...")

    # Test 1: Health check
    if not test_health():
        print("\n❌ Health check failed. Is the server running?")
        sys.exit(1)

    # Test 2: Root endpoint
    if not test_root():
        print("\n❌ Root endpoint failed.")
        sys.exit(1)

    # Test 3: Create conversation
    conversation = test_create_conversation()
    if not conversation:
        print("\n❌ Failed to create conversation. Check database migrations.")
        sys.exit(1)

    conversation_id = conversation["id"]
    print(f"\n✅ Created conversation with ID: {conversation_id}")

    # Test 4: List conversations
    if not test_list_conversations():
        print("\n❌ Failed to list conversations.")
        sys.exit(1)

    # Test 5: Send message (with AI response)
    print("\n⚠️  Next test will call OpenRouter API (costs credits)")
    input("Press Enter to continue or Ctrl+C to stop...")

    if not test_send_message(conversation_id):
        print("\n❌ Failed to send message. Check OpenRouter API key.")
        sys.exit(1)

    # Small delay to ensure message is saved
    sleep(1)

    # Test 6: Get messages
    if not test_get_messages(conversation_id):
        print("\n❌ Failed to get messages.")
        sys.exit(1)

    # Final summary
    print_separator("Test Summary")
    print("✅ All tests passed!")
    print(f"✅ Conversation ID: {conversation_id}")
    print(f"✅ API is working correctly")
    print("\nYou can now:")
    print(f"  - View API docs: {BASE_URL}/docs")
    print(f"  - Test more endpoints manually")
    print(f"  - Use the conversation ID: {conversation_id}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
