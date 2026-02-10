from openai import OpenAI
from app.config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_spec_requirements(text):

    prompt = f"""
    Extract all mandatory product requirements from this specification.
    Return valid JSON list:
    [
      {{
        "requirement_id": "",
        "requirement_text": "",
        "performance_criteria": "",
        "standards": ""
      }}
    ]
    SPEC:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)


def extract_cutsheet_data(text):

    prompt = f"""
    Extract technical product attributes.
    Return JSON:
    {{
      "manufacturer": "",
      "model": "",
      "dimensions": "",
      "performance": "",
      "materials": "",
      "certifications": ""
    }}
    CUTSHEET:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)


def run_compliance(spec_json, cut_json):

    prompt = f"""
    Compare product data to specification requirements.
    Return JSON:
    [
      {{
        "requirement_id": "",
        "status": "Compliant | Non-Compliant | Not Addressed | Exceeds",
        "reasoning": ""
      }}
    ]

    SPEC: {spec_json}
    PRODUCT: {cut_json}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)
