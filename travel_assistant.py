from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
from memory_management import JSONMemoryManager
import os
from dotenv import load_dotenv

load_dotenv()

class TravelAssistant:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.memory_manager = JSONMemoryManager()
        self.conversation_id = "default_user"  # In a real app, this would be user-specific
        
        # Define the system prompt
        self.system_prompt = """You are a knowledgeable and friendly Travel Assistant. Your role is to:
        - Provide helpful travel recommendations
        - Suggest itineraries based on user preferences
        - Offer packing tips for different destinations
        - Share insights about local cultures and customs
        - Help with travel planning and logistics
        
        Always be polite, enthusiastic, and provide detailed, personalized responses.
        If you don't know something, admit it and try to guide the user to find the information."""
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}")
        ])
        
    def format_messages(self, messages):
        formatted = []
        for msg in messages:
            if msg["role"] == "user":
                formatted.append(HumanMessage(content=msg["content"]))
            else:
                formatted.append(AIMessage(content=msg["content"]))
        return formatted
    
    def chat(self, user_input: str):
        # Retrieve conversation history
        history = self.memory_manager.get_conversation(self.conversation_id)
        
        # Create the chain
        chain = self.prompt_template | self.llm
        
        # Format the chat history for the prompt
        chat_history = self.format_messages(history)
        
        # Invoke the chain
        response = chain.invoke({
            "chat_history": chat_history,
            "input": user_input
        })
        
        # Update conversation history
        history.extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response.content}
        ])
        self.memory_manager.update_conversation(self.conversation_id, history)
        
        return response.content