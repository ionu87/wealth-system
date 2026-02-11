"""
Advanced AI Agent with RAG
Loads knowledge from files and uses it to answer questions
"""

import anthropic
import os
import json
from datetime import datetime
from pathlib import Path

class AdvancedSupportAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        
        self.conversation_history = []
        self.knowledge_base = self.load_knowledge_from_files()
        
    def load_knowledge_from_files(self):
        """Load all knowledge base files"""
        knowledge = {}
        kb_path = Path("knowledge_base")
        
        if not kb_path.exists():
            kb_path.mkdir()
            print("📁 Created knowledge_base folder")
            return {}
        
        for file in kb_path.glob("*.txt"):
            topic = file.stem
            with open(file, 'r') as f:
                content = f.read()
                knowledge[topic] = content
                print(f"✅ Loaded: {topic}")
        
        return knowledge
    
    def search_knowledge(self, query):
        """Search through knowledge base for relevant info"""
        query_lower = query.lower()
        relevant_docs = []
        
        # Search through all documents
        for topic, content in self.knowledge_base.items():
            # Count how many query words appear in this document
            relevance = sum(1 for word in query_lower.split() if word in content.lower())
            
            if relevance > 0:
                relevant_docs.append({
                    'topic': topic,
                    'content': content,
                    'relevance': relevance
                })
        
        # Sort by relevance (most relevant first)
        relevant_docs.sort(key=lambda x: x['relevance'], reverse=True)
        
        return relevant_docs[:3]  # Return top 3 most relevant
    
    def respond_with_context(self, customer_query):
        """Generate response using RAG"""
        
        # Step 1: RETRIEVE - Search knowledge base
        relevant_docs = self.search_knowledge(customer_query)
        
        # Step 2: Build context from retrieved documents
        context = "\n\n".join([
            f"Topic: {doc['topic']}\n{doc['content']}" 
            for doc in relevant_docs
        ])
        
        # Step 3: Include conversation history (short-term memory)
        history_context = "\n".join([
            f"Customer: {h['query']}\nAgent: {h['response']}"
            for h in self.conversation_history[-3:]  # Last 3 exchanges
        ])
        
        # Step 4: GENERATE - Create prompt with context
        prompt = f"""You are a helpful customer support agent.

KNOWLEDGE BASE (use this to answer):
{context if context else "No specific information found. Use general knowledge."}

RECENT CONVERSATION:
{history_context if history_context else "This is the start of the conversation."}

CUSTOMER QUESTION: {customer_query}

Provide a helpful, accurate response (2-3 sentences).
Use the knowledge base information when available.
If you don't have enough information, say so and offer to escalate."""

        # Step 5: Call AI to generate response
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response = message.content[0].text
        
        # Step 6: Save to conversation history
        self.conversation_history.append({
            'query': customer_query,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'context_used': [doc['topic'] for doc in relevant_docs]
        })
        
        return response, relevant_docs
    
    def save_conversation_log(self):
        """Save full conversation for analysis"""
        with open('conversation_logs.json', 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        print("💾 Conversation saved to conversation_logs.json")
    
    def chat(self):
        """Interactive chat interface"""
        print("\n" + "="*60)
        print("🤖 ADVANCED AI AGENT - WITH RAG & MEMORY")
        print("="*60)
        print("Commands: 'quit' = exit, 'history' = see conversation")
        print("         'stats' = analytics, 'reload' = refresh knowledge\n")
        
        while True:
            query = input("Customer: ")
            
            if query.lower() == 'quit':
                self.save_conversation_log()
                print("\n👋 Goodbye!\n")
                break
            
            if query.lower() == 'history':
                print(f"\n📜 Conversation History ({len(self.conversation_history)} exchanges):")
                for i, h in enumerate(self.conversation_history, 1):
                    print(f"\n{i}. Customer: {h['query']}")
                    print(f"   Agent: {h['response']}")
                    print(f"   Context: {', '.join(h['context_used'])}")
                continue
            
            if query.lower() == 'stats':
                self.show_stats()
                continue
            
            if query.lower() == 'reload':
                self.knowledge_base = self.load_knowledge_from_files()
                print("✅ Knowledge base reloaded\n")
                continue
            
            if not query.strip():
                continue
            
            # Generate response
            print("\nAgent: ", end="", flush=True)
            response, docs_used = self.respond_with_context(query)
            print(response)
            
            # Show which documents were used
            if docs_used:
                print(f"\n📚 Used knowledge from: {', '.join([d['topic'] for d in docs_used])}")
            else:
                print(f"\n⚠️  No relevant knowledge found (AI used general knowledge)")
            
            print()
    
    def show_stats(self):
        """Show conversation analytics"""
        print(f"\n📊 AGENT STATISTICS")
        print(f"="*60)
        print(f"Total conversations: {len(self.conversation_history)}")
        print(f"Knowledge base topics: {len(self.knowledge_base)}")
        
        if self.conversation_history:
            topics_used = {}
            for h in self.conversation_history:
                for topic in h.get('context_used', []):
                    topics_used[topic] = topics_used.get(topic, 0) + 1
            
            if topics_used:
                print(f"\nMost used knowledge topics:")
                for topic, count in sorted(topics_used.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"  - {topic}: {count} times")
        
        print(f"="*60 + "\n")

if __name__ == "__main__":
    agent = AdvancedSupportAgent()
    agent.chat()

