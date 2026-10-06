import os
from openai import OpenAI


def ask_business_chatbot(question, business_context=""):

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")

    # Do not crash the whole project if no key exists
    if not api_key:
        return (
            "Chatbot is currently unavailable because "
            "OPENAI_API_KEY has not been configured."
        )

    try:

        # Create client only when chatbot is actually used
        client = OpenAI(
            api_key=api_key
        )

        # Create prompt using business information
        prompt = f"""
You are an AI assistant for a Business Analytics Platform.

Use the business information below to answer the user's question.

BUSINESS DATA:
{business_context}

USER QUESTION:
{question}

Give a clear and concise business-focused answer.
"""

        response = client.responses.create(
            model="gpt-5.6",
            input=prompt
        )

        return response.output_text

    except Exception as error:

        return (
            "Chatbot error: "
            + str(error)
        )