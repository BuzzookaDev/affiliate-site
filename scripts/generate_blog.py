import os
import csv
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

csv_name = 'products.csv'
if not os.path.exists(csv_name):
    print("❌ ERROR: products.csv not found!")
    exit(1)

def generate_post(name, desc):
    print(f"🚀 AI is writing for: {name}...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional product reviewer."},
                {"role": "user", "content": f"Write a 300-word SEO affiliate review for: {name}. Context: {desc}"}
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

# SMART CSV READER: Fixes header typos automatically
with open(csv_name, mode='r', encoding='utf-8-sig') as file:
    # This line cleans the headers (removes spaces and makes them lowercase)
    reader = csv.DictReader(file)
    reader.fieldnames = [field.strip().lower().replace(" ", "_") for field in reader.fieldnames]
    
    for row in reader:
        # Now we look for 'product_name' or 'productname' or 'name'
        name = row.get('product_name') or row.get('name') or row.get('productname')
        desc = row.get('description') or row.get('desc')
        
        if name and desc:
            generate_post(name, desc)
        else:
            print(f"⚠️ Skipping row: Missing name or description. Found: {list(row.keys())}")
