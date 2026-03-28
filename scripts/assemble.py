#!/usr/bin/env python3
"""
assemble.py — Assembla i file markdown in un singolo HTML e genera PDF.
Uso: python3 assemble.py <module>
  module: modulo-base | pregenerati | supplemento | all
"""
import argparse, os, re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SCRIPTS = ROOT / "scripts"
ASSETS = ROOT / "assets"

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
    md_files = sorted(content_dir.glob("*.md"))
    combined = []
    for f in md_files:
        text = f.read_text(encoding="utf-8")
        text = strip_frontmatter(text)
        combined.append(text)
    return "\n\n".join(combined)


def md_to_html(markdown_text, title):
    """Convert markdown to HTML body fragment via pandoc."""
    result = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html5", "--wrap=none"],
        input=markdown_text, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Errore pandoc: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def build_full_html(body_html, title):
    """Wrap body HTML in a full HTML document with CSS."""
    css_path = SCRIPTS / "pdf-style.css"
    css_text = css_path.read_text(encoding="utf-8")

    # Resolve font paths to absolute file:// URIs
    fonts_dir = ASSETS / "fonts"
    css_text = css_text.replace(
        "url('../assets/fonts/",
        f"url('file://{fonts_dir}/"
    )

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{css_text}
</style>
</head>
<body>
{body_html}
</body>
</html>"""


def html_to_pdf(html_text, output_path):
    """Convert HTML to PDF via WeasyPrint."""
    from weasyprint import HTML
    HTML(string=html_text, base_url=str(ROOT)).write_pdf(str(output_path))


def build_module(module_key):
    """Build a single module PDF."""
    mod = MODULES[module_key]
    print(f"\n{'='*60}")
    print(f"  {mod['title']}")
    print(f"{'='*60}")

    print("  [1/4] Assemblaggio markdown...")
    md = assemble_markdown(module_key)

    print("  [2/4] Markdown -> HTML (pandoc)...")
    body = md_to_html(md, mod["title"])

    print("  [3/4] Assemblaggio HTML completo...")
    html = build_full_html(body, mod["title"])

    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / mod["output"]

    # Save HTML for debug
    debug_html = output_dir / mod["output"].replace(".pdf", ".html")
    debug_html.write_text(html, encoding="utf-8")

    print(f"  [4/4] HTML -> PDF (WeasyPrint)...")
    html_to_pdf(html, output_path)

    size_kb = output_path.stat().st_size // 1024
    print(f"  -> {output_path.name} ({size_kb} KB)")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Assembla e genera PDF per I Lupi dell'Assia")
    parser.add_argument(
        "module",
        choices=["modulo-base", "pregenerati", "supplemento", "all"],
        help="Quale modulo generare")
    args = parser.parse_args()

    if args.module == "all":
        for key in MODULES:
            build_module(key)
    else:
        build_module(args.module)

    print("\n  Build completata.")


if __name__ == "__main__":
    main()
