#!/usr/bin/env python3
"""
Simple PDF Report Generator using reportlab

Generates professional PDF reports from UN motion analysis results without
requiring heavy dependencies like weasyprint.

Usage:
    python scripts/generate_simple_pdf.py <input_file> [--output output.pdf]

Example:
    python scripts/generate_simple_pdf.py analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        return True
    except ImportError as e:
        print(f"Missing dependency: reportlab")
        print("\nInstall with:")
        print("  pip install reportlab")
        return False


def generate_bilateral_impact_pdf(json_file: Path, output_pdf: Optional[Path] = None):
    """
    Generate PDF report from bilateral impact analysis JSON

    Args:
        json_file: Path to JSON analysis results
        output_pdf: Optional output PDF path
    """
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Determine output path
    if output_pdf is None:
        output_pdf = json_file.parent / "pdf" / f"{json_file.stem}.pdf"

    # Create output directory
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Create PDF
    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c5f8d'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name='CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=6,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name='Justified',
        parent=styles['Normal'],
        alignment=TA_JUSTIFY,
        fontSize=10,
        leading=14
    ))

    # Title
    title = Paragraph("Israel Bilateral Relationship Impact Analysis", styles['CustomTitle'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))

    # Metadata
    metadata = [
        f"<b>Motion:</b> {data['motion_id']}",
        f"<b>Analysis Date:</b> {data['timestamp']}",
        f"<b>Model:</b> {data['model']}",
        f"<b>Countries Analyzed:</b> {data['total_analyzed']}"
    ]
    for line in metadata:
        elements.append(Paragraph(line, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    # Executive Summary
    elements.append(Paragraph("Executive Summary", styles['CustomHeading']))
    summary_text = f"This report analyzes how the Gaza ceasefire resolution vote affects Israel's bilateral relationships with {data['total_analyzed']} UN member states."
    elements.append(Paragraph(summary_text, styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))

    # Impact Distribution Table
    elements.append(Paragraph("Impact Distribution", styles['CustomSubHeading']))

    impact_data = [['Impact Category', 'Count', 'Percentage']]
    total = data['total_analyzed']
    for category, count in data['impact_summary'].items():
        pct = (count / total * 100) if total > 0 else 0
        impact_data.append([
            category.replace('_', ' ').title(),
            str(count),
            f"{pct:.1f}%"
        ])

    impact_table = Table(impact_data, colWidths=[3.5*inch, 1*inch, 1*inch])
    impact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    elements.append(impact_table)
    elements.append(Spacer(1, 0.3*inch))

    # Detailed Analyses by Category
    elements.append(PageBreak())
    elements.append(Paragraph("Detailed Country Analyses", styles['CustomHeading']))
    elements.append(Spacer(1, 0.2*inch))

    # Group analyses by impact category
    by_category = {}
    for analysis in data['analyses']:
        category = analysis['impact_analysis']['impact_category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(analysis)

    # Category order
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

        # Category heading
        elements.append(Paragraph(
            category.replace('_', ' ').title(),
            styles['CustomHeading']
        ))
        elements.append(Spacer(1, 0.1*inch))

        for i, analysis in enumerate(by_category[category]):
            # Country name
            elements.append(Paragraph(
                f"<b>{analysis['country']}</b>",
                styles['CustomSubHeading']
            ))

            # Vote and confidence
            info_text = f"<b>Vote:</b> {analysis['vote'].upper()} | <b>Confidence:</b> {analysis['impact_analysis']['confidence']}"
            elements.append(Paragraph(info_text, styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))

            # Analysis reasoning
            elements.append(Paragraph("<b>Analysis:</b>", styles['Normal']))
            reasoning = analysis['impact_analysis']['reasoning']
            elements.append(Paragraph(reasoning, styles['Justified']))
            elements.append(Spacer(1, 0.1*inch))

            # Key factors
            elements.append(Paragraph("<b>Key Factors:</b>", styles['Normal']))
            for factor in analysis['impact_analysis']['key_factors']:
                elements.append(Paragraph(f"• {factor}", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))

            # Country statement
            elements.append(Paragraph("<b>Country Statement:</b>", styles['Normal']))
            statement = analysis['statement']
            if len(statement) > 500:
                statement = statement[:500] + "..."
            elements.append(Paragraph(statement, styles['Justified']))

            # Separator between countries
            if i < len(by_category[category]) - 1:
                elements.append(Spacer(1, 0.2*inch))

        # Space between categories
        elements.append(Spacer(1, 0.3*inch))

    # Footer
    footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(footer_text, styles['Normal']))

    # Build PDF
    print(f"Generating PDF: {output_pdf}")
    doc.build(elements)
    print(f"✓ PDF generated successfully")

    return output_pdf


def generate_markdown_pdf(md_file: Path, output_pdf: Optional[Path] = None):
    """
    Generate PDF from markdown file

    Args:
        md_file: Path to markdown file
        output_pdf: Optional output PDF path
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Determine output path
    if output_pdf is None:
        output_pdf = md_file.parent / "pdf" / f"{md_file.stem}.pdf"

    # Create output directory
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Create PDF
    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Add custom styles
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=20,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name='Justified',
        parent=styles['Normal'],
        alignment=TA_JUSTIFY,
        fontSize=10,
        leading=14
    ))

    # Simple markdown parsing (basic headers and paragraphs)
    lines = md_content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            elements.append(Spacer(1, 0.1*inch))
            continue

        if line.startswith('# '):
            elements.append(Paragraph(line[2:], styles['CustomTitle']))
        elif line.startswith('## '):
            elements.append(Paragraph(line[3:], styles['Heading2']))
        elif line.startswith('### '):
            elements.append(Paragraph(line[4:], styles['Heading3']))
        elif line.startswith('**') or line.startswith('*'):
            elements.append(Paragraph(line, styles['Normal']))
        elif line.startswith('---'):
            elements.append(Spacer(1, 0.2*inch))
        else:
            elements.append(Paragraph(line, styles['Justified']))

    # Build PDF
    print(f"Generating PDF: {output_pdf}")
    doc.build(elements)
    print(f"✓ PDF generated successfully")

    return output_pdf


def main():
    parser = argparse.ArgumentParser(
        description="Generate PDF reports from analysis results (lightweight version)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert JSON bilateral impact to PDF
  python scripts/generate_simple_pdf.py tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json

  # Convert markdown to PDF
  python scripts/generate_simple_pdf.py analysis/report.md

  # Specify output path
  python scripts/generate_simple_pdf.py analysis/report.md --output custom.pdf
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
        # Determine file type and process
        if args.input_file.suffix == '.json':
            print("Processing bilateral impact JSON...")
            pdf_path = generate_bilateral_impact_pdf(args.input_file, args.output)
        elif args.input_file.suffix == '.md':
            print("Processing markdown file...")
            pdf_path = generate_markdown_pdf(args.input_file, args.output)
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
