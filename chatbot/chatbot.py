import os

from openai import OpenAI


def ask_business_chatbot(
    question,
    business_context
):

    # ==================================================
    # API KEY
    # ==================================================

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    # ==================================================
    # NO API KEY
    # ==================================================

    if not api_key:

        return (
            "I could not answer that question "
            "using the built-in dashboard "
            "calculations. More advanced AI "
            "questions require an "
            "OPENAI_API_KEY."
        )

    # ==================================================
    # OPENAI REQUEST
    # ==================================================

    try:

        client = OpenAI(
            api_key=api_key
        )

        prompt = f"""
You are an AI Business Assistant.

Use only the business information supplied below
to answer the user's question.

Do not invent business numbers.

If the available data does not contain enough
information to answer the question, clearly say so.

BUSINESS DATA:

{business_context}

USER QUESTION:

{question}

Give a concise and clear business-focused answer.
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
            "The AI assistant could not "
            "complete the request. "
            f"Error: {error}"
        )