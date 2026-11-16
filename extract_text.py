import os
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_script = False
        self.in_style = False
        self.in_title = False
        self.in_meta = False
        self.skip_tags = {'script', 'style', 'noscript'}
        self.current_tag = None
        self.attrs_dict = {}
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.attrs_dict = dict(attrs)
        if tag in self.skip_tags:
            if tag == 'script':
                self.in_script = True
            elif tag == 'style':
                self.in_style = True
        elif tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            self.in_meta = True
        elif tag == 'a':
            href = self.attrs_dict.get('href', '')
            if href and not href.startswith('#'):
                self.text_parts.append(f' [Link: {href}]')
        elif tag == 'img':
            src = self.attrs_dict.get('src', '')
            alt = self.attrs_dict.get('alt', '')
            if src:
                self.text_parts.append(f' [Image: {src}' + (f' | Alt: {alt}' if alt else '') + ']')
        elif tag == 'input':
            placeholder = self.attrs_dict.get('placeholder', '')
            if placeholder:
                self.text_parts.append(f' [Input placeholder: {placeholder}]')
        elif tag == 'button':
            self.text_parts.append(' [Button]')
        elif tag == 'option':
            self.text_parts.append(' [Option]')
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.text_parts.append(f'\n{"#" * int(tag[1])} ')
        elif tag == 'p':
            self.text_parts.append('\n\n')
        elif tag == 'br':
            self.text_parts.append('\n')
        elif tag == 'li':
            self.text_parts.append('\n- ')
        elif tag == 'tr':
            self.text_parts.append('\n')
        elif tag == 'td' or tag == 'th':
            self.text_parts.append(' | ')
        elif tag == 'hr':
            self.text_parts.append('\n---\n')
        elif tag == 'blockquote':
            self.text_parts.append('\n> ')
        elif tag == 'code':
            self.text_parts.append('`')
        elif tag == 'pre':
            self.text_parts.append('\n```\n')
        elif tag == 'strong' or tag == 'b':
            self.text_parts.append('**')
        elif tag == 'em' or tag == 'i':
            self.text_parts.append('*')
        elif tag == 'mark':
            self.text_parts.append('==')
        elif tag == 'del':
            self.text_parts.append('~~')
        elif tag == 'ins':
            self.text_parts.append('++')
        elif tag == 'small':
            self.text_parts.append(' [small] ')
        elif tag == 'sub':
            self.text_parts.append(' [sub] ')
        elif tag == 'sup':
            self.text_parts.append(' [sup] ')
        elif tag == 'time':
            datetime = self.attrs_dict.get('datetime', '')
            if datetime:
                self.text_parts.append(f' [datetime: {datetime}] ')
        elif tag == 'address':
            self.text_parts.append('\n[Address] ')
        elif tag == 'footer':
            self.text_parts.append('\n[Footer] ')
        elif tag == 'header':
            self.text_parts.append('\n[Header] ')
        elif tag == 'nav':
            self.text_parts.append('\n[Navigation] ')
        elif tag == 'main':
            self.text_parts.append('\n[Main] ')
        elif tag == 'section':
            self.text_parts.append('\n[Section] ')
        elif tag == 'article':
            self.text_parts.append('\n[Article] ')
        elif tag == 'aside':
            self.text_parts.append('\n[Aside] ')
        elif tag == 'div':
            pass
        elif tag == 'span':
            pass
        elif tag == 'label':
            self.text_parts.append(' [Label] ')
        elif tag == 'fieldset':
            self.text_parts.append('\n[Fieldset] ')
        elif tag == 'legend':
            self.text_parts.append(' [Legend] ')
        elif tag == 'textarea':
            self.text_parts.append(' [Textarea] ')
        elif tag == 'select':
            self.text_parts.append(' [Select] ')
        elif tag == 'form':
            self.text_parts.append('\n[Form] ')
        elif tag == 'table':
            self.text_parts.append('\n[Table] ')
        elif tag == 'caption':
            self.text_parts.append(' [Caption] ')
        elif tag == 'thead':
            self.text_parts.append(' [Thead] ')
        elif tag == 'tbody':
            self.text_parts.append(' [Tbody] ')
        elif tag == 'tfoot':
            self.text_parts.append(' [Tfoot] ')
        elif tag == 'ul' or tag == 'ol':
            self.text_parts.append('\n')
        elif tag == 'dl':
            self.text_parts.append('\n[Definition List] ')
        elif tag == 'dt':
            self.text_parts.append('\n[Term] ')
        elif tag == 'dd':
            self.text_parts.append(' [Definition] ')
        elif tag == 'figure':
            self.text_parts.append('\n[Figure] ')
        elif tag == 'figcaption':
            self.text_parts.append(' [Figcaption] ')
        elif tag == 'details':
            self.text_parts.append('\n[Details] ')
        elif tag == 'summary':
            self.text_parts.append(' [Summary] ')
        elif tag == 'dialog':
            self.text_parts.append('\n[Dialog] ')
        elif tag == 'menu':
            self.text_parts.append('\n[Menu] ')
        elif tag == 'progress':
            self.text_parts.append(' [Progress] ')
        elif tag == 'meter':
            self.text_parts.append(' [Meter] ')
        elif tag == 'output':
            self.text_parts.append(' [Output] ')
        elif tag == 'canvas':
            self.text_parts.append(' [Canvas] ')
        elif tag == 'audio':
            self.text_parts.append(' [Audio] ')
        elif tag == 'video':
            self.text_parts.append(' [Video] ')
        elif tag == 'source':
            pass
        elif tag == 'track':
            pass
        elif tag == 'embed':
            pass
        elif tag == 'object':
            pass
        elif tag == 'param':
            pass
        elif tag == 'iframe':
            pass
        elif tag == 'picture':
            pass
        elif tag == 'svg':
            self.text_parts.append(' [SVG] ')
        elif tag == 'math':
            self.text_parts.append(' [Math] ')
        elif tag == 'template':
            pass
        elif tag == 'slot':
            pass
        elif tag == 'datalist':
            pass
        elif tag == 'optgroup':
            pass
            
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
        elif tag == 'title':
            self.in_title = False
        elif tag == 'meta':
            self.in_meta = False
        elif tag == 'a':
            self.text_parts.append(' [/Link]')
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.text_parts.append('\n')
        elif tag == 'p':
            self.text_parts.append('\n')
        elif tag == 'li':
            self.text_parts.append('')
        elif tag == 'strong' or tag == 'b':
            self.text_parts.append('**')
        elif tag == 'em' or tag == 'i':
            self.text_parts.append('*')
        elif tag == 'mark':
            self.text_parts.append('==')
        elif tag == 'del':
            self.text_parts.append('~~')
        elif tag == 'ins':
            self.text_parts.append('++')
        elif tag == 'code':
            self.text_parts.append('`')
        elif tag == 'pre':
            self.text_parts.append('\n```\n')
        elif tag == 'blockquote':
            self.text_parts.append('\n')
        elif tag == 'address':
            self.text_parts.append('\n')
        elif tag == 'footer':
            self.text_parts.append('\n')
        elif tag == 'header':
            self.text_parts.append('\n')
        elif tag == 'nav':
            self.text_parts.append('\n')
        elif tag == 'main':
            self.text_parts.append('\n')
        elif tag == 'section':
            self.text_parts.append('\n')
        elif tag == 'article':
            self.text_parts.append('\n')
        elif tag == 'aside':
            self.text_parts.append('\n')
        elif tag == 'label':
            self.text_parts.append(' [/Label] ')
        elif tag == 'fieldset':
            self.text_parts.append('\n')
        elif tag == 'legend':
            self.text_parts.append(' [/Legend] ')
        elif tag == 'textarea':
            self.text_parts.append(' [/Textarea] ')
        elif tag == 'select':
            self.text_parts.append(' [/Select] ')
        elif tag == 'form':
            self.text_parts.append('\n')
        elif tag == 'table':
            self.text_parts.append('\n')
        elif tag == 'caption':
            self.text_parts.append(' [/Caption] ')
        elif tag == 'figure':
            self.text_parts.append('\n')
        elif tag == 'figcaption':
            self.text_parts.append(' [/Figcaption] ')
        elif tag == 'details':
            self.text_parts.append('\n')
        elif tag == 'summary':
            self.text_parts.append(' [/Summary] ')
        elif tag == 'dialog':
            self.text_parts.append('\n')
        elif tag == 'menu':
            self.text_parts.append('\n')
            
    def handle_data(self, data):
        if self.in_script or self.in_style:
            return
        if self.in_title:
            self.text_parts.append(f'[Title] {data}')
            return
        if self.in_meta:
            name = self.attrs_dict.get('name', '') or self.attrs_dict.get('property', '') or self.attrs_dict.get('http-equiv', '')
            content = self.attrs_dict.get('content', '')
            if name and content:
                self.text_parts.append(f'[Meta: {name}] {content}')
            return
        data = re.sub(r'\s+', ' ', data).strip()
        if data:
            self.text_parts.append(data)
            
    def handle_comment(self, data):
        pass
        
    def get_text(self):
        text = ''.join(self.text_parts)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\s+([.,;:!?)])', r'\1', text)
        text = re.sub(r'([({[])\s+', r'\1', text)
        return text.strip()

def extract_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    parser = TextExtractor()
    parser.feed(html)
    return parser.get_text()

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
        text = extract_from_file(filepath)
        output_lines.append(text)
        output_lines.append("")
        output_lines.append("---")
        output_lines.append("")

# Write output
output_path = os.path.join(base_dir, "WEBSITE_CONTENT.md")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Written to {output_path}")