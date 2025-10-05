import os
import requests
from flask import current_app

def call_gemini_api(text):
    """
    Call Gemini API to analyze journal entry.
    Returns dict with 'mood' and 'reflection' keys.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        current_app.logger.warning('GEMINI_API_KEY not found')
        return {
            'mood': 'neutral',
            'reflection': 'Unable to generate reflection (API key missing)'
        }
    
    # Gemini REST API endpoint
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}'
    
    # Prompt template
    prompt = f"""Analyze this journal entry and provide:
1. Mood: Describe the emotional state in 2-3 words (e.g., "stressed but hopeful", "happy and excited")
2. Reflection: Brief supportive reflection and recommendation if applicable (1-2 sentences maximum)

Journal entry: {text}

Format your response exactly as:
MOOD: <mood here>
REFLECTION: <reflection here>"""
    
    # Request payload
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        generated_text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Extract mood and reflection
        mood = 'neutral'
        reflection = 'Keep writing to track your journey.'
        
        lines = generated_text.strip().split('\n')
        for line in lines:
            if line.startswith('MOOD:'):
                mood = line.replace('MOOD:', '').strip()
            elif line.startswith('REFLECTION:'):
                reflection = line.replace('REFLECTION:', '').strip()
        
        return {
            'mood': mood,
            'reflection': reflection
        }
    
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f'Gemini API error: {e}')
        return {
            'mood': 'neutral',
            'reflection': 'Unable to generate reflection at this time.'
        }
    except (KeyError, IndexError) as e:
        current_app.logger.error(f'Error parsing Gemini response: {e}')
        return {
            'mood': 'neutral',
            'reflection': 'Unable to parse AI response.'
        }