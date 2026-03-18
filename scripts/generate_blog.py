import os
import csv
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Debug: Check if file exists
if not os.path.exists('products.csv'):
    print("❌ ERROR: products.csv not found in the root directory!")
    exit(1)

def generate_post(product_name, description):
    print(f"🚀 Processing: {product_name}...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional product reviewer."},
                {"role": "user", "content": f"Write a 300-word SEO affiliate review for: {product_name}. Context: {description}"}
            ]
        )
        content = response.choices[0].message.content
        
        filename = f"content/posts/{product_name.lower().replace(' ', '-')}.md"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"---\ntitle: '{product_name}'\ndate: 2026-03-18\ndraft: false\n---\n\n{content}")
        print(f"✅ Created: {filename}")
    except Exception as e:
        print(f"❌ Failed to generate {product_name}: {e}")

# Read CSV and run
with open('products.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['product_name']:
            generate_post(row['product_name'], row['description'])
