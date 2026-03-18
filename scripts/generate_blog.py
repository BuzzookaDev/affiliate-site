import openai
import csv
import os
import re

# Initialize Client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_post(row):
    product = row['Product Name']
    link = row['Amazon Link']
    
    # Updated Prompt for Hugo logic
    prompt = f"Write a professional, aesthetic affiliate blog post for {product}. Focus on solving {row['Primary Pain Point']} for {row['Target Audience']}. Start with an affiliate disclosure."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content
    # Create a URL-friendly slug
    slug = re.sub(r'[^a-z0-9]+', '-', product.lower()).strip('-')

    # Ensure the directory exists
    os.makedirs("content/posts", exist_ok=True)
    
    # Save as Hugo Markdown with Frontmatter
    with open(f"content/posts/{slug}.md", "w", encoding="utf-8") as f:
        f.write(f"---\ntitle: \"{product}\"\ndate: 2026-03-17\naffiliate_link: \"{link}\"\ndraft: false\n---\n\n")
        f.write(content)

# Process your uploaded CSV
csv_path = 'products/products.csv'
if os.path.exists(csv_path):
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            create_post(row)
