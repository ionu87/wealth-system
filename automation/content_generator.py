"""
LinkedIn Content Generator
Automated weekly post creation
"""

import anthropic
import os
from datetime import datetime

class ContentGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
    
    def generate_post(self, topic):
        """Generate single post"""
        
        prompt = f"""Create a professional LinkedIn post about: {topic}

Requirements:
- 120-150 words
- Start with an attention-grabbing hook
- Provide 1 actionable insight
- End with an engagement question
- Professional but conversational tone
- No emojis, no hashtags

Write the post:"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def generate_week(self):
        """Generate 5 posts for the week"""
        
        topics = [
            "How AI reduces customer support costs by 60%",
            "Why small businesses need AI automation in 2026",
            "3 AI tools every e-commerce store should use",
            "The future of customer service is hybrid (AI + human)",
            "How I'm building AI agents for businesses"
        ]
        
        print("\n" + "="*60)
        print("📝 GENERATING WEEKLY LINKEDIN CONTENT")
        print("="*60 + "\n")
        
        for i, topic in enumerate(topics, 1):
            print(f"Generating Post {i}/5...")
            post = self.generate_post(topic)
            
            print(f"\n{'='*60}")
            print(f"POST {i} - {topic}")
            print(f"{'='*60}")
            print(post)
            print(f"\nSuggested hashtags: #AI #Automation #BusinessGrowth")
            print(f"{'='*60}\n")
        
        print("✅ All 5 posts generated!")
        print("⏱️  Review and schedule on LinkedIn")

# Run it
if __name__ == "__main__":
    generator = ContentGenerator()
    generator.generate_week()

