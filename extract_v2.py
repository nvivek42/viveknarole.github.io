import os
import re
from bs4 import BeautifulSoup

def extract_text_from_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    
    # Get title
    title = soup.title.string if soup.title else ""
    
    # Get meta description
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_desc = meta.get("content", "")
    
    # Get all text, preserving structure
    text_parts = []
    
    if title:
        text_parts.append(f"=== TITLE: {title} ===")
    if meta_desc:
        text_parts.append(f"=== META DESCRIPTION: {meta_desc} ===")
    
    # Process body
    body = soup.body
    if body:
        text_parts.append(extract_element_text(body, 0))
    
    return "\n".join(text_parts)

def extract_element_text(element, depth=0):
    """Extract text from element preserving structure"""
    texts = []
    
    # Handle different tags
    if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        level = int(element.name[1])
        prefix = '#' * level + ' '
        text = element.get_text(strip=True)
        if text:
            texts.append(f"{prefix}{text}")
    elif element.name == 'p':
        text = element.get_text(strip=True)
        if text:
            texts.append(text)
    elif element.name == 'a':
        href = element.get('href', '')
        text = element.get_text(strip=True)
        if text and href and not href.startswith('#'):
            texts.append(f"{text} [Link: {href}]")
        elif text:
            texts.append(text)
    elif element.name == 'li':
        text = element.get_text(strip=True)
        if text:
            texts.append(f"  • {text}")
    elif element.name == 'blockquote':
        text = element.get_text(strip=True)
        if text:
            texts.append(f"> {text}")
    elif element.name == 'code' and element.parent.name != 'pre':
        text = element.get_text(strip=True)
        if text:
            texts.append(f"`{text}`")
    elif element.name == 'pre':
        text = element.get_text(strip=True)
        if text:
            texts.append(f"```\n{text}\n```")
    elif element.name == 'strong' or element.name == 'b':
        text = element.get_text(strip=True)
        if text:
            texts.append(f"**{text}**")
    elif element.name == 'em' or element.name == 'i':
        text = element.get_text(strip=True)
        if text:
            texts.append(f"*{text}*")
    elif element.name == 'hr':
        texts.append("---")
    elif element.name == 'br':
        texts.append("\n")
    elif element.name in ['div', 'section', 'article', 'main', 'header', 'footer', 'nav', 'aside', 'span']:
        # Process children
        for child in element.children:
            if child.name:
                texts.append(extract_element_text(child, depth + 1))
            elif isinstance(child, str):
                text = child.strip()
                if text:
                    texts.append(text)
    else:
        # For other elements, get text directly
        text = element.get_text(strip=True)
        if text:
            texts.append(text)
    
    return "\n".join(filter(None, texts))

# Main extraction
base_dir = "E:/play/personal-os/public-site-work"
output_lines = []

html_files = [
    "index.html",
    "portfolio/index.html",
    "portfolio/projects/index.html",
    "portfolio/projects/_template.html",
    "portfolio/projects/naval-wealth-framework-stress-test.html",
    "portfolio/projects/goal-clarity-engine.html",
    "portfolio/projects/pune-industrial-hubs.html",
    "portfolio/projects/career-decision-framework.html",
    "portfolio/projects/ai-debugging-infrastructure.html",
    "portfolio/projects/odyssey-plans.html",
    "portfolio/experiences/index.html",
    "portfolio/experiences/manufacturing-org-psychology.html",
    "portfolio/experiences/flow-and-vedanta.html",
    "portfolio/lessons/index.html",
    "portfolio/lessons/you-were-never-lost.html",
    "portfolio/lessons/flow-is-a-system.html",
    "portfolio/lessons/ticket-that-kept-coming-back.html",
    "portfolio/lessons/industrial-hubs-pune.html",
    "portfolio/goal-clarity/index.html",
]

output_lines.append("# Complete Website Content - viveknarole.com")
output_lines.append("")
output_lines.append("Extracted from all HTML pages in textual format.")
output_lines.append("")

for html_file in html_files:
    filepath = os.path.join(base_dir, html_file)
    if os.path.exists(filepath):
        output_lines.append(f"## {html_file}")
        output_lines.append("")
        text = extract_text_from_html(filepath)
        output_lines.append(text)
        output_lines.append("")
        output_lines.append("---")
        output_lines.append("")

# Write output
output_path = os.path.join(base_dir, "WEBSITE_CONTENT.md")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Written to {output_path}")
