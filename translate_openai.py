import os
import json
import logging
import time
import random
import datetime
from dotenv import load_dotenv
from jinja2 import Template
from openai import OpenAIError
import openai


# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


openai.api_key = OPENAI_API_KEY


# Load Prompt Template
def load_prompt_template(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return Template(f.read())


title_prompt_template = load_prompt_template("prompts/title_translation.prompt")
content_prompt_template = load_prompt_template("prompts/content_translation.prompt")


# Translation Function
def translate_text(text, template: Template):
    prompt = template.render(text=text)

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
        )
        content = response.choices[0].message.content.strip()
        if "Result:" in content:
            return content.split("Result:", 1)[1].strip()
        else:
            return content
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI API Error: {str(e)}")


# Main Logic
def fetch_and_translate_column(cleaning_data=None, output_dir=None):
    try:

        data = cleaning_data

        result = []

        for i, row in enumerate(data):
            id = row.get("id", f"debug_{i}")
            title = row.get("title")
            title_zh = row.get("title_zh")
            content = row.get("content")
            content_zh = row.get("content_zh")

            translated_title = title_zh
            translated_content = content_zh

            try:
                if not translated_title and title:
                    translated_title = translate_text(title, title_prompt_template)

                if not translated_content and content:
                    translated_content = translate_text(
                        content, content_prompt_template
                    )

                status = (
                    "translated"
                    if translated_title and translated_content
                    else (
                        "title failed"
                        if not translated_title
                        else (
                            "content failed" if not translated_content else "All failed"
                        )
                    )
                )

                item = {
                    "id": id,
                    "link": row.get("link"),
                    "title": title,
                    "title_zh": translated_title or "null",
                    "content": content,
                    "content_zh": translated_content or "null",
                    "translation_status": status,
                }
                result.append(item)

                print(f"[{i+1}/{len(data)}] ✅ ID {id} translated. Status: {status}")
                time.sleep(random.uniform(10, 20))

            except Exception as e:
                logging.error(
                    f"Translation failed for ID {id}: {str(e)}", extra={"id": id}
                )
                print(f"[{i+1}/{len(data)}] ❌ ID {id} failed: {e}")

            executed_at = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

            os.makedirs(output_dir, exist_ok=True)
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fetch_path = os.path.join(
                output_dir, f"all_translated_data_{executed_at}.json"
            )
            with open(fetch_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

        return result

    except Exception as e:
        logging.error(
            f"Critical error in translation: {str(e)}", extra={"id": "system"}
        )
        return None
