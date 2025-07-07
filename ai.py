import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def detect_subject(question):
    """
    Detect the subject of the question using AI
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a subject detection assistant. Analyze the following homework question and respond with ONLY the subject it belongs to. Possible subjects: Math, English, Science, Kiswahili, Social Studies, CRE, or Other."},
                {"role": "user", "content": question}
            ],
            temperature=0.1,
            max_tokens=10
        )
        
        subject = response.choices[0].message.content.strip()
        return subject
    except Exception as e:
        print(f"Error detecting subject: {e}")
        return "Other"

def generate_response(question, subject, step_by_step=False, simple_explanation=False):
    """
    Generate a child-friendly explanation for the homework question
    """
    try:
        # Build the system prompt based on options
        system_prompt = f"""
        You are a helpful homework assistant for Kenyan parents helping their children with CBC curriculum (Grades 4-9). 
        The subject is {subject}. 
        Provide a clear, concise explanation that a parent can use to explain to their child.
        """
        
        if simple_explanation:
            system_prompt += " Explain this to a 10-year-old using simple language and relatable examples from Kenya."
        
        if step_by_step:
            system_prompt += " Break down the solution into clear, numbered steps."
        
        system_prompt += " Use friendly, encouraging language. If it's a math problem, explain the concepts before solving."
        
        response = openai.ChatCompletion.create(
            model="gpt-4" if not simple_explanation else "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response. Please try again later."