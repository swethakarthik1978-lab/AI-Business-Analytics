# ==================================================
# IMPORTS
# ==================================================

import os

from openai import OpenAI


# ==================================================
# BUSINESS CHATBOT
# ==================================================

def ask_business_chatbot(
    question,
    business_context
):

    # ==================================================
    # GET API KEY
    # ==================================================

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    # ==================================================
    # NO API KEY
    # ==================================================

    if not api_key:

        return (
            "I could not answer that question using "
            "the built-in dashboard calculations. "
            "More advanced AI questions require "
            "an OPENAI_API_KEY."
        )

    # ==================================================
    # OPENAI REQUEST
    # ==================================================

    try:

        client = OpenAI(
            api_key=api_key
        )

        prompt = f"""
You are an AI Business Assistant for a
business analytics dashboard.

Answer the user's question using only the
business information provided below.

Do not invent numbers or statistics.

If the requested information cannot be determined
from the provided data, clearly say that there is
not enough information.

BUSINESS INFORMATION:

{business_context}

USER QUESTION:

{question}

Provide a concise and clear business answer.
"""

        response = (
            client.responses.create(
                model=os.getenv(
                    "OPENAI_MODEL",
                    "gpt-4.1-mini"
                ),
                input=prompt
            )
        )

        return (
            response.output_text
        )

    except Exception as error:

        return (
            "The AI assistant could not complete "
            "the request. "
            f"Error: {error}"
        )