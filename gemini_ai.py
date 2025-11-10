import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class GeminiFinancialAdvisor:
    def __init__(self, api_key):
        """Initialize the Gemini AI financial advisor"""
        os.environ["GOOGLE_API_KEY"] = api_key
        
        # Initialize the Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-002",
            temperature=0.7,
            max_output_tokens=1024
        )
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        # Create the chain
        self.chain = self.prompt | self.llm
        
        # Create memory store
        self.memory_store = {}
    
    def get_financial_advice(self, user_message, user_data):
        """Get financial advice from Gemini AI based on user data and message"""
        
        # Create system prompt with user's financial data
        system_prompt = f"""You are a professional financial advisor AI assistant. You have access to the user's financial data:

**User's Financial Profile:**
- Current Balance: ${user_data['balance']:.2f}
- Total Expenses: ${user_data['total_expenses']:.2f}
- Average Daily Spending: ${user_data['avg_daily_spending']:.2f}
- Number of Expenses Tracked: {user_data['expense_count']}
- Top Spending Category: {user_data['top_category'][0] if user_data['top_category'] else 'N/A'} (${user_data['top_category'][1]:.2f} if user_data['top_category'] else 0)

**Your Role:**
- Provide personalized financial advice based on their actual data
- Be conversational and helpful
- Use emojis and formatting to make responses engaging
- Give specific, actionable advice
- Consider their spending patterns and financial situation
- If they mention a location (like India), provide location-specific advice
- Always be encouraging and supportive

**Response Guidelines:**
- Keep responses concise but informative
- Use bullet points and formatting for clarity
- Include specific numbers and percentages when relevant
- Provide step-by-step guidance when appropriate
- Be empathetic to their financial situation
- Use a friendly, professional tone

Remember: You are talking to a real person who wants genuine financial help. Be helpful, accurate, and encouraging."""

        try:
            # Get response from Gemini
            response = self.chain.invoke({
                "system_prompt": system_prompt,
                "chat_history": [],  # For now, no memory - can be enhanced later
                "input": user_message
            })
            return response.content
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request right now. Please try again in a moment. Error: {str(e)}"
    
    def clear_memory(self):
        """Clear the conversation memory"""
        self.memory_store.clear()

# Global instance
gemini_advisor = None

def initialize_gemini(api_key):
    """Initialize the global Gemini advisor"""
    global gemini_advisor
    gemini_advisor = GeminiFinancialAdvisor(api_key)
    return gemini_advisor

def get_gemini_advice(user_message, user_data):
    """Get advice from the global Gemini advisor"""
    global gemini_advisor
    if gemini_advisor is None:
        raise Exception("Gemini advisor not initialized")
    return gemini_advisor.get_financial_advice(user_message, user_data)

def clear_gemini_memory():
    """Clear the global Gemini memory"""
    global gemini_advisor
    if gemini_advisor:
        gemini_advisor.clear_memory()
