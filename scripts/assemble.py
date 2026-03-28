#!/usr/bin/env python3
"""
assemble.py — Assembla i file markdown in un singolo HTML per WeasyPrint.
Uso: python3 assemble.py <module> [--output <file>]
  module: modulo-base | pregenerati | supplemento | all
"""
import argparse, os, re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SCRIPTS = ROOT / "scripts"

MODULES = {
    "modulo-base": {
        "dir": "modulo-base",
        "title": "I Lupi dell'Assia: Modulo Base",
        "output": "I_Lupi_dell_Assia_MODULO_BASE.pdf",
    },
    "pregenerati": {
        "dir": "pregenerati",
        "title": "I Lupi dell'Assia: Townsfolk Pregenerati",
        "output": "I_Lupi_dell_Assia_PREGENERATI.pdf",
    },
    "supplemento": {
        "dir": "supplemento",
        "title": "I Lupi dell'Assia: Supplemento Cronista",
        "output": "I_Lupi_dell_Assia_SUPPLEMENTO_CRONISTA.pdf",
    },
}

def strip_frontmatter(text):
    """Remove YAML frontmatter from markdown."""
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[end + 3:].strip()
    return text

def assemble_markdown(module_key):
    """Concatenate all markdown files for a module in order."""
    mod = MODULES[module_key]
    content_dir = CONTENT / mod["dir"]
    
    # Get all .md files sorted by name
    md_files = sorted(content_dir.glob("*.md"))
    
    combined = []
    for f in md_files:
        text = f.read_text(encoding="utf-8")
        text = strip_frontmatter(text)
        combined.append(text)
    
    return "\n\n---\n\n".join(combined)

def md_to_html(markdown_text, title):
    """Convert markdown to HTML via pandoc."""
    result = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html5",
         "--standalone", "--metadata", f"title={title}",
         "--toc", "--toc-depth=2"],
        input=markdown_text, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Errore pandoc: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout

def inject_css(html, css_path):
    """Inject CSS into HTML <head>."""
    css = css_path.read_text(encoding="utf-8")
    # Replace </head> with <style>CSS</style></head>
    return html.replace("</head>", f"<style>\n{css}\n</style>\n</head>")

def html_to_pdf(html_text, output_path):
    """Convert HTML to PDF via WeasyPrint."""
    try:
        from weasyprint import HTML
        HTML(string=html_text).write_pdf(str(output_path))
    except ImportError:
        # Fallback: write HTML and use weasyprint CLI
        tmp_html = output_path.with_suffix('.html')
        tmp_html.write_text(html_text, encoding='utf-8')
        subprocess.run(["weasyprint", str(tmp_html), str(output_path)], check=True)
        tmp_html.unlink()

def build_module(module_key):
    """Build a single module PDF."""
    mod = MODULES[module_key]
    print(f"\n{'='*60}")
    print(f"  Building: {mod['title']}")
    print(f"{'='*60}")
    
    # 1. Assemble markdown
    print("  [1/3] Assemblaggio markdown...")
    md = assemble_markdown(module_key)
    
    # 2. Convert to HTML
    print("  [2/3] Markdown → HTML (pandoc)...")
    html = md_to_html(md, mod["title"])
    
    # 3. Inject CSS
    css_path = SCRIPTS / "pdf-style.css"
    html = inject_css(html, css_path)
    
    # 4. Convert to PDF
    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / mod["output"]
    
    print(f"  [3/3] HTML → PDF (WeasyPrint)...")
    html_to_pdf(html, output_path)
    
    print(f"  ✓ Output: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Assembla e genera PDF per I Lupi dell'Assia")
    parser.add_argument("module", choices=["modulo-base", "pregenerati", "supplemento", "all"],
                       help="Quale modulo generare")
    args = parser.parse_args()
    
    if args.module == "all":
        for key in MODULES:
            build_module(key)
    else:
        build_module(args.module)
    
    print("\n✓ Build completata.")

if __name__ == "__main__":
    main()
