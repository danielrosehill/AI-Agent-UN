#!/usr/bin/env python3
"""
PDF Report Generator

Generates professional PDF reports from UN motion analysis results.
Supports multiple report types:
- Vote analysis reports
- Bilateral impact analysis reports
- Custom markdown to PDF conversion

Usage:
    python scripts/generate_pdf_report.py <markdown_file> [--output output.pdf]

Example:
    python scripts/generate_pdf_report.py analysis/01_gaza_ceasefire_resolution_analysis_REVISED.md
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import markdown
        import weasyprint
        return True
    except ImportError as e:
        print(f"Missing dependencies: {e}")
        print("\nInstall with:")
        print("  pip install markdown weasyprint")
        return False


def markdown_to_pdf(markdown_file: Path, output_pdf: Optional[Path] = None):
    """
    Convert markdown file to PDF with professional styling

    Args:
        markdown_file: Path to markdown file
        output_pdf: Optional output PDF path (default: same name as markdown with .pdf)
    """
    import markdown
    from weasyprint import HTML, CSS

    # Read markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'extra',
        'codehilite',
        'toc',
        'tables',
        'fenced_code'
    ])
    html_content = md.convert(md_content)

    # Generate styled HTML document
    styled_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{markdown_file.stem}</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm 2cm;
            @top-right {{
                content: "Page " counter(page);
                font-size: 9pt;
                color: #666;
            }}
        }}

        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }}

        h1 {{
            color: #1a5490;
            font-size: 24pt;
            font-weight: bold;
            margin-top: 0;
            margin-bottom: 10pt;
            border-bottom: 3px solid #1a5490;
            padding-bottom: 10pt;
        }}

        h2 {{
            color: #2c5f8d;
            font-size: 18pt;
            font-weight: bold;
            margin-top: 20pt;
            margin-bottom: 10pt;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5pt;
        }}

        h3 {{
            color: #34495e;
            font-size: 14pt;
            font-weight: bold;
            margin-top: 15pt;
            margin-bottom: 8pt;
        }}

        h4 {{
            color: #555;
            font-size: 12pt;
            font-weight: bold;
            margin-top: 12pt;
            margin-bottom: 6pt;
        }}

        p {{
            margin: 8pt 0;
            text-align: justify;
        }}

        ul, ol {{
            margin: 10pt 0;
            padding-left: 25pt;
        }}

        li {{
            margin: 5pt 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15pt 0;
            font-size: 10pt;
        }}

        th {{
            background-color: #1a5490;
            color: white;
            font-weight: bold;
            padding: 8pt;
            text-align: left;
            border: 1px solid #ddd;
        }}

        td {{
            padding: 6pt 8pt;
            border: 1px solid #ddd;
        }}

        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        code {{
            background-color: #f4f4f4;
            padding: 2pt 4pt;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            border-radius: 3pt;
        }}

        pre {{
            background-color: #f4f4f4;
            padding: 10pt;
            border-left: 3px solid #1a5490;
            overflow-x: auto;
            font-size: 9pt;
            line-height: 1.4;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
        }}

        blockquote {{
            margin: 15pt 0;
            padding: 10pt 15pt;
            background-color: #f9f9f9;
            border-left: 4px solid #1a5490;
            font-style: italic;
        }}

        hr {{
            border: none;
            border-top: 2px solid #ccc;
            margin: 20pt 0;
        }}

        .warning {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10pt;
            margin: 15pt 0;
        }}

        .error {{
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 10pt;
            margin: 15pt 0;
        }}

        .success {{
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            padding: 10pt;
            margin: 15pt 0;
        }}

        .metadata {{
            background-color: #e9ecef;
            padding: 10pt;
            margin-bottom: 20pt;
            border-radius: 5pt;
            font-size: 10pt;
        }}

        a {{
            color: #1a5490;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
{html_content}
<div style="margin-top: 30pt; padding-top: 10pt; border-top: 1px solid #ccc; font-size: 9pt; color: #666;">
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</div>
</body>
</html>
"""

    # Determine output path
    if output_pdf is None:
        output_pdf = markdown_file.parent / "pdf" / f"{markdown_file.stem}.pdf"

    # Create output directory
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Convert HTML to PDF
    print(f"Generating PDF: {output_pdf}")
    HTML(string=styled_html).write_pdf(output_pdf)
    print(f"✓ PDF generated successfully")

    return output_pdf


def generate_bilateral_impact_pdf(json_file: Path, output_pdf: Optional[Path] = None):
    """
    Generate PDF report from bilateral impact analysis JSON

    Args:
        json_file: Path to JSON analysis results
        output_pdf: Optional output PDF path
    """
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Generate markdown report
    md_content = f"""# Israel Bilateral Relationship Impact Analysis

**Motion:** {data['motion_id']}
**Analysis Date:** {data['timestamp']}
**Model:** {data['model']}
**Countries Analyzed:** {data['total_analyzed']}

---

## Executive Summary

This report analyzes how the Gaza ceasefire resolution vote affects Israel's bilateral relationships with {data['total_analyzed']} UN member states.

### Impact Distribution

"""

    # Add impact summary table
    md_content += "| Impact Category | Count | Percentage |\n"
    md_content += "|----------------|-------|------------|\n"

    total = data['total_analyzed']
    for category, count in data['impact_summary'].items():
        pct = (count / total * 100) if total > 0 else 0
        md_content += f"| {category.replace('_', ' ').title()} | {count} | {pct:.1f}% |\n"

    md_content += "\n---\n\n"

    # Group analyses by impact category
    by_category = {}
    for analysis in data['analyses']:
        category = analysis['impact_analysis']['impact_category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(analysis)

    # Add detailed analyses by category
    category_order = [
        'strengthened_significantly',
        'strengthened_moderately',
        'strengthened_slightly',
        'neutral',
        'strained_slightly',
        'strained_moderately',
        'strained_significantly'
    ]

    for category in category_order:
        if category not in by_category or not by_category[category]:
            continue

        md_content += f"## {category.replace('_', ' ').title()}\n\n"

        for analysis in by_category[category]:
            md_content += f"### {analysis['country']}\n\n"
            md_content += f"**Vote:** {analysis['vote'].upper()}  \n"
            md_content += f"**Confidence:** {analysis['impact_analysis']['confidence']}  \n\n"

            md_content += f"**Analysis:**  \n"
            md_content += f"{analysis['impact_analysis']['reasoning']}\n\n"

            md_content += f"**Key Factors:**\n"
            for factor in analysis['impact_analysis']['key_factors']:
                md_content += f"- {factor}\n"

            md_content += f"\n**Country Statement:**  \n"
            md_content += f"> {analysis['statement']}\n\n"
            md_content += "---\n\n"

    # Save markdown temporarily
    temp_md = json_file.parent / f"{json_file.stem}_report.md"
    with open(temp_md, 'w', encoding='utf-8') as f:
        f.write(md_content)

    # Convert to PDF
    pdf_path = markdown_to_pdf(temp_md, output_pdf)

    # Clean up temp markdown
    temp_md.unlink()

    return pdf_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate professional PDF reports from analysis results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert markdown to PDF
  python scripts/generate_pdf_report.py analysis/report.md

  # Convert JSON bilateral impact to PDF
  python scripts/generate_pdf_report.py analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json

  # Specify output path
  python scripts/generate_pdf_report.py analysis/report.md --output custom_report.pdf
        """
    )

    parser.add_argument(
        "input_file",
        type=Path,
        help="Input file (.md or .json)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output PDF file (optional)"
    )

    args = parser.parse_args()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Validate input file
    if not args.input_file.exists():
        print(f"Error: Input file not found: {args.input_file}")
        sys.exit(1)

    try:
        # Determine file type and process accordingly
        if args.input_file.suffix == '.json':
            print("Processing bilateral impact JSON...")
            pdf_path = generate_bilateral_impact_pdf(args.input_file, args.output)
        elif args.input_file.suffix == '.md':
            print("Processing markdown file...")
            pdf_path = markdown_to_pdf(args.input_file, args.output)
        else:
            print(f"Error: Unsupported file type: {args.input_file.suffix}")
            print("Supported types: .md, .json")
            sys.exit(1)

        print(f"\n✓ PDF report generated: {pdf_path}")
        print(f"  Size: {pdf_path.stat().st_size / 1024:.1f} KB")

    except Exception as e:
        print(f"\n❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
