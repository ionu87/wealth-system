"""
AI Customer Support Agent - Your First Agent
"""

import anthropic
import os
from datetime import datetime

class SupportAgent:
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("❌ No API key found. Run: echo $ANTHROPIC_API_KEY")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        
        # Simple knowledge base
        self.knowledge = {
            "shipping": "Free shipping on orders over $50. Standard: 3-5 days. Express: 1-2 days.",
            "returns": "30-day return policy. Items must be unused in original packaging.",
            "tracking": "Tracking number sent within 24 hours via email.",
            "payment": "We accept Visa, Mastercard, PayPal, Apple Pay."
        }
    
    def get_context(self, query):
        """Find relevant info"""
        query_lower = query.lower()
        
        for topic, info in self.knowledge.items():
            if topic in query_lower:
                return info
        
        return "For detailed help, contact support@store.com"
    
    def respond(self, customer_query):
        """Generate AI response"""
        
        context = self.get_context(customer_query)
        
        prompt = f"""You are a helpful customer support agent.

Context: {context}

Customer: {customer_query}

Respond in 2-3 friendly, helpful sentences."""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def chat(self):
        """Interactive chat loop"""
        print("\n" + "="*60)
        print("🤖 AI SUPPORT AGENT - LIVE")
        print("="*60)
        print("Type 'quit' to exit\n")
        
        while True:
            query = input("Customer: ")
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if not query.strip():
                continue
            
            print("\nAgent: ", end="", flush=True)
            response = self.respond(query)
            print(response + "\n")

# Run it
if __name__ == "__main__":
    try:
        agent = SupportAgent()
        agent.chat()
    except ValueError as e:
        print(str(e))
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your API key is set correctly.")
