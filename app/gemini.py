import os
from flask import current_app

try:
    # LangChain + Google Generative AI integration
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:  # pragma: no cover
    ChatGoogleGenerativeAI = None


def _build_prompt(text: str) -> str:
    return (
        "Analyze this journal entry and provide:\n"
        "1. Mood: Describe the emotional state in 2-3 words (e.g., \"stressed but hopeful\", \"happy and excited\")\n"
        "2. Reflection: Brief supportive reflection and recommendation if applicable (1-2 sentences maximum)\n\n"
        f"Journal entry: {text}\n\n"
        "Format your response exactly as:\n"
        "MOOD: <mood here>\n"
        "REFLECTION: <reflection here>"
    )


essential_fallback = {
    'mood': 'neutral',
    'reflection': 'Unable to generate reflection at this time.'
}


def call_gemini_api(text):
    """
    Use LangChain's ChatGoogleGenerativeAI to call Gemini and analyze a journal entry.
    Returns dict with 'mood' and 'reflection' keys and never raises in normal flow.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')

    if not api_key:
        current_app.logger.warning('GEMINI_API_KEY not found')
        return {
            'mood': 'neutral',
            'reflection': 'Unable to generate reflection (API key missing)'
        }

    if ChatGoogleGenerativeAI is None:
        current_app.logger.error('langchain-google-genai is not installed')
        return essential_fallback

    try:
        llm = ChatGoogleGenerativeAI(model=model_name, api_key=api_key, temperature=0.3)
        prompt = _build_prompt(text)
        res = llm.invoke(prompt)
        # res.content is a string response for Chat models in LangChain
        generated_text = getattr(res, 'content', None) or str(res)

        # Extract mood and reflection with simple parsing
        mood = 'neutral'
        reflection = 'Keep writing to track your journey.'
        for line in (generated_text or '').splitlines():
            if line.strip().upper().startswith('MOOD:'):
                mood = line.split(':', 1)[1].strip() if ':' in line else mood
            elif line.strip().upper().startswith('REFLECTION:'):
                reflection = line.split(':', 1)[1].strip() if ':' in line else reflection

        return {
            'mood': mood,
            'reflection': reflection
        }
    except Exception as e:  # catch SDK/network/model errors
        current_app.logger.error(f'Gemini API error via LangChain: {e}')
        return essential_fallback
