import os
import csv
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

csv_name = 'products.csv'
if not os.path.exists(csv_name):
    print("❌ ERROR: products.csv not found!")
    exit(1)

def generate_post(name, link, category, target, pain_point):
    print(f"🚀 AI is writing for: {name}...")
    try:
        # We combine your columns into a prompt for the AI
        prompt_context = f"Category: {category}. Target Audience: {target}. Solving this problem: {pain_point}."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional product reviewer."},
                {"role": "user", "content": f"Write a 300-word SEO affiliate review for: {name}. {prompt_context} End with a call to action to check it out here: {link}"}
            ]
        )
        content = response.choices[0].message.content
        
        os.makedirs("content/posts", exist_ok=True)
        filename = f"content/posts/{name.lower().replace(' ', '-')}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"---\ntitle: '{name}'\ndate: 2026-03-18\ndraft: false\n---\n\n{content}")
        print(f"✅ Success: {filename}")
    except Exception as e:
        print(f"❌ OpenAI Error: {e}")

# Read CSV and run
with open(csv_name, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    # Cleaning headers to match your CSV screenshot exactly
    reader.fieldnames = [field.strip().lower().replace(" ", "_") for field in reader.fieldnames]
    
    for row in reader:
        name = row.get('product_name')
        link = row.get('amazon_link')
        cat = row.get('category')
        target = row.get('target_audience')
        pain = row.get('primary_pain_point')
        
        if name:
            generate_post(name, link, cat, target, pain)
        else:
            print(f"⚠️ Skipping row: {row}")
