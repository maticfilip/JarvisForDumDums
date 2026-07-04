import requests
import json
import os
import re

OLLAMA_URL="http://localhost:11434"
SETTINGS_FILE="data/llm_settings.json"
DEFAULT_MODEL="phi3:mini"

VALID_CATEGORIES = [
    "Algorithms", "Data Structures", "String Manipulation",
    "Mathematics", "Language Features", "Other"
]

def get_selected_model():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_MODEL
    with open(SETTINGS_FILE, "r") as f:
        content=f.read().strip()
        if not content:
            return DEFAULT_MODEL
        data=json.loads(content)
        return data.get("model", DEFAULT_MODEL)
    
def set_selected_model(model):
    os.makedirs("data", exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"model":model}, f, indent=2)

def is_ollama_running():
    try:
        response=requests.get(OLLAMA_URL, timeout=2)
        return response.status_code==200
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False

def get_available_models():
    try:
        response=requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        data=response.json()
        return [m["name"] for m in data.get("models", [])]
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return []
    
def generate(prompt:str, on_complete, on_error=None):
    import threading

    def worker():
        try:
            model=get_selected_model()
            response=requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model":model, "prompt":prompt, "stream":False},
                timeout=120
            )
            response.raise_for_status()
            text=response.json().get("response","")
            on_complete(text)
        except Exception as e:
            if on_error:
                on_error(str(e))
        
    threading.Thread(target=worker, daemon=True).start()




def parse_json_response(raw:str):
    print(f"[DEBUG RAW LLM OUTPUT]\n{raw}\n")
    
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        return {"topic": "Unknown", "category": "Other", "explanation": raw}

    try:
        pairs = []
        decoder = json.JSONDecoder(object_pairs_hook=lambda p: p)
        pairs = decoder.decode(match.group())
        
        data = {}
        for key, value in pairs:
            if key not in data:
                data[key] = value

        if data.get("category") not in VALID_CATEGORIES:
            data["category"] = "Other"

        topic_lower = data.get("topic", "").lower()
        explanation_lower = data.get("explanation", "").lower()

        keyword_map = {
            "String Manipulation": ["string", "character", "regex", "text", "format", "camel", "split", "join"],
            "Mathematics":         ["math", "prime", "fibonacci", "number theory", "arithmetic"],
            "Data Structures":     ["tree", "graph", "linked list", "stack", "queue", "hash"],
            "Language Features":   ["comprehension", "generator", "decorator", "lambda", "built-in"],
        }

        for category, keywords in keyword_map.items():
            if any(kw in topic_lower for kw in keywords):
                data["category"] = category
                break

        return data

    except (json.JSONDecodeError, ValueError):
        return {"topic": "Unknown", "category": "Other", "explanation": raw}


def explain_topic(kata_name, difficulty, description, code, on_complete, on_error=None):
    prompt = f"""You are an experienced software engineering mentor writing reference material for a developer learning platform.

A student just solved this Codewars kata:

Kata: {kata_name} ({difficulty})
Description: {description}
Their solution:
{code}

Use this kata only as context to identify the underlying topic. Then write a general, reusable explanation of that topic.

Structure your explanation with these exact section headers:

## What is it?
## How does it work?
## Common use cases
## Common mistakes
## How it appears in your solution

Write 2-4 sentences per section in plain prose.

IMPORTANT — Category selection rules:
- If the topic involves strings, text, characters, formatting, regex → category MUST be "String Manipulation"
- If the topic involves lists, trees, graphs, dictionaries, stacks → category MUST be "Data Structures"  
- If the topic involves numbers, arithmetic, primes, geometry → category MUST be "Mathematics"
- If the topic involves Python built-ins, comprehensions, generators → category MUST be "Language Features"
- If the topic involves sorting, searching, recursion, dynamic programming → category MUST be "Algorithms"
- Otherwise → "Other"

Respond ONLY in this exact JSON format. Do not repeat any key. No text before or after:
{{
  "topic": "short topic name, 2-4 words",
  "category": "exactly one of the categories listed above",
  "explanation": "your full explanation with ## headers, sections separated by double newlines"
}}"""

    def handle_raw(raw: str):
        on_complete(parse_json_response(raw))

    generate(prompt, on_complete=handle_raw, on_error=on_error)

def explain_topic_delta(existing_topic, existing_explanation, 
                        kata_name, difficulty, description, 
                        code, on_complete, on_error=None):
    prompt = f"""You are a coding mentor maintaining a student's personal knowledge base.

The student already has these notes on "{existing_topic}":

---
{existing_explanation}
---

They just solved a new kata that touches the same topic:

Kata: {kata_name} ({difficulty})
Description: {description}
Their solution:
{code}

Your job is to identify what this new kata teaches that is NOT already covered in the existing notes above.

Write ONLY the new information — do not repeat or summarise anything already written.
If the existing notes already cover everything this kata demonstrates, respond with exactly: "NOTHING_NEW"

Format your addition with a section header like:
## From: {kata_name}
Then 2-3 sentences of genuinely new insight.

Respond with just the new text, no JSON, no preamble."""

    generate(prompt, on_complete=on_complete, on_error=on_error)


def get_code_feedback(kata_name, difficulty, code, on_complete, on_error=None):
    prompt=f"""You are a coding mentor reviewing a CodeWars solution.
    Kata: {kata_name} ({difficulty})

Solution:
{code}

Give brief, constructive feedback covering:
1. Code readability
2. Efficiency or edge cases missed
3. One alternative approach if applicable

Keep it concise and encouraging. Write 2-3 short paragraphs, no headers or bullet points."""

    generate(prompt, on_complete=on_complete, on_error=on_error)

def generate_weekly_review(entries,on_complete,on_error=None):
    if not entries:
        on_complete("No kata logged this week, nothing to review yet.")
        return
    summary_lines=[]
    for e in entries:
        line=f"-{e["kata_name"]}({e["difficulty"]}, {e.get("language","unknown")})-{e["status"]}"
        if e.get("notes"):
            line+=f". Notes: {e["notes"]}"
        summary_lines.append(line)
    week_summary="\n".join(summary_lines)

    prompt = f"""You are a coding mentor reviewing a student's week of Codewars practice.

This week's kata:
{week_summary}

Write a short, encouraging weekly review covering:
1. What they practiced and any patterns you notice
2. Any difficulty or topic they seemed to struggle with
3. One concrete suggestion for next week

Keep it warm and concise, 3-4 short paragraphs, no headers or bullet points."""

    generate(prompt, on_complete=on_complete, on_error=on_error)
