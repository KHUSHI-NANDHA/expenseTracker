import os
import google.generativeai as genai

class SimpleGeminiFinancialAdvisor:
    def __init__(self, api_key):
        """Initialize the Gemini AI financial advisor"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def get_financial_advice(self, user_message, user_data):
        """Get financial advice from Gemini AI based on user data and message"""
        
        # Format expense data for the prompt
        expenses_text = ""
        if user_data.get('expenses'):
            expenses_text = "\n**Detailed Expense List (with dates):**\n"
            for exp in user_data['expenses'][:100]:  # Limit to first 100 for prompt size
                expenses_text += f"- {exp['date']}: ${exp['amount']:.2f} - {exp['description']} ({exp['category']})\n"
        
        # Format year-based spending
        year_breakdown = ""
        if user_data.get('expenses_by_year'):
            year_breakdown = "\n**Spending by Year:**\n"
            for year in sorted(user_data['expenses_by_year'].keys(), reverse=True):
                year_breakdown += f"- {year}: ${user_data['expenses_by_year'][year]:.2f}\n"
        
        # Format month-based spending
        month_breakdown = ""
        if user_data.get('expenses_by_year_month'):
            month_breakdown = "\n**Spending by Year-Month:**\n"
            for ym in sorted(user_data['expenses_by_year_month'].keys(), reverse=True):
                month_breakdown += f"- {ym}: ${user_data['expenses_by_year_month'][ym]:.2f}\n"
        
        # Create system prompt with user's financial data
        system_prompt = f"""You are a professional financial advisor AI assistant. You have access to the user's detailed financial data:

**User's Financial Profile:**
- Current Balance: ${user_data['balance']:.2f}
- Total Expenses (All Time): ${user_data['total_expenses']:.2f}
- Average Daily Spending: ${user_data['avg_daily_spending']:.2f}
- Number of Expenses Tracked: {user_data['expense_count']}
- Top Spending Category: {user_data['top_category'][0] if user_data['top_category'] else 'N/A'} (${user_data['top_category'][1]:.2f} if user_data['top_category'] else 0)
{year_breakdown}{month_breakdown}{expenses_text}

**IMPORTANT - You have access to detailed expense data with dates!**
- You can answer questions about spending in specific years (e.g., "how much did I spend in 2021?")
- You can answer questions about spending in specific months (e.g., "what did I spend last month?")
- You can analyze spending patterns over time
- Use the detailed expense list and year/month breakdowns to provide accurate answers
- If asked about a specific year, calculate the total from expenses_by_year or filter expenses by date

**Your Role:**
- Provide personalized financial advice based on their actual data
- Answer specific questions about spending by year, month, or time period
- Be conversational and helpful
- Use emojis and formatting to make responses engaging
- Give specific, actionable advice with actual numbers from their data
- Consider their spending patterns and financial situation
- If they mention a location (like India), provide location-specific advice
- Always be encouraging and supportive

**Response Guidelines:**
- Keep responses concise but informative
- Use bullet points and formatting for clarity
- Include specific numbers and percentages when relevant
- When asked about spending in a specific year/month, provide the exact amount from the data
- Provide step-by-step guidance when appropriate
- Be empathetic to their financial situation
- Use a friendly, professional tone

Remember: You are talking to a real person who wants genuine financial help. Be helpful, accurate, and encouraging. Use the detailed expense data to answer their questions precisely.

User's question: {user_message}"""

        try:
            # Get response from Gemini
            response = self.model.generate_content(system_prompt)
            if response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")  # Debug print
            return f"I apologize, but I'm having trouble processing your request right now. Please try again in a moment. Error: {str(e)}"
    
    def clear_memory(self):
        """Clear the conversation memory"""
        pass

# Global instance
gemini_advisor = None

def initialize_gemini(api_key):
    """Initialize the global Gemini advisor"""
    global gemini_advisor
    gemini_advisor = SimpleGeminiFinancialAdvisor(api_key)
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
