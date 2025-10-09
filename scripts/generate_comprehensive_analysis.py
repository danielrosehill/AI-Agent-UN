#!/usr/bin/env python3
"""
Comprehensive Analysis PDF Generator

Synthesizes all voting data and bilateral impact analysis into a single
comprehensive PDF report.

Usage:
    python scripts/generate_comprehensive_analysis.py <motion_id>

Example:
    python scripts/generate_comprehensive_analysis.py 01_gaza_ceasefire_resolution
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        return True
    except ImportError:
        print("Missing dependency: reportlab")
        print("\nInstall with: pip install reportlab")
        return False


def load_voting_results(motion_id: str) -> Dict:
    """Load voting results"""
    reactions_dir = PROJECT_ROOT / "tasks" / "reactions"
    results_file = reactions_dir / f"{motion_id}_latest.json"

    if not results_file.exists():
        raise FileNotFoundError(f"Voting results not found: {results_file}")

    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_bilateral_impact(motion_id: str) -> Dict:
    """Load bilateral impact analysis"""
    analysis_dir = PROJECT_ROOT / "tasks" / "analysis"
    impact_file = analysis_dir / f"{motion_id}_israel_bilateral_impact_latest.json"

    if not impact_file.exists():
        raise FileNotFoundError(f"Bilateral impact analysis not found: {impact_file}")

    with open(impact_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_comprehensive_pdf(motion_id: str, output_pdf: Path = None):
    """Generate comprehensive analysis PDF"""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, PageBreak, KeepTogether)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

    # Load data
    print("Loading data...")
    voting_data = load_voting_results(motion_id)
    bilateral_data = load_bilateral_impact(motion_id)

    # Output path
    if output_pdf is None:
        analysis_dir = PROJECT_ROOT / "tasks" / "analysis" / "pdf"
        analysis_dir.mkdir(parents=True, exist_ok=True)
        output_pdf = analysis_dir / f"{motion_id}_comprehensive_analysis.pdf"

    # Create PDF
    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=30,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=20,
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

    # TITLE PAGE
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph(
        "Gaza Ceasefire Resolution<br/>Comprehensive Analysis",
        styles['CustomTitle']
    ))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(
        f"Motion ID: {motion_id}",
        ParagraphStyle('centered', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12)
    ))
    elements.append(Paragraph(
        f"Analysis Date: {datetime.now().strftime('%B %d, %Y')}",
        ParagraphStyle('centered', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12)
    ))
    elements.append(Spacer(1, 0.5*inch))

    # Executive Summary
    exec_summary = f"""This report provides a comprehensive analysis of the Gaza ceasefire resolution
    voted on by {voting_data['total_votes']} UN member states. The analysis includes voting patterns,
    regional alignments, and detailed assessment of how the vote affects Israel's bilateral relationships
    with each country."""
    elements.append(Paragraph(exec_summary, styles['Justified']))

    elements.append(PageBreak())

    # SECTION 1: VOTING RESULTS
    elements.append(Paragraph("1. Voting Results Overview", styles['CustomHeading']))
    elements.append(Spacer(1, 0.2*inch))

    vote_summary = voting_data['vote_summary']
    total_votes = voting_data['total_votes']

    vote_text = f"""The resolution received {vote_summary['yes']} votes in favor
    ({vote_summary['yes']/total_votes*100:.1f}%), {vote_summary['no']} votes against
    ({vote_summary['no']/total_votes*100:.1f}%), and {vote_summary['abstain']} abstentions
    ({vote_summary['abstain']/total_votes*100:.1f}%)."""
    elements.append(Paragraph(vote_text, styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))

    # Voting table
    vote_table_data = [
        ['Vote', 'Count', 'Percentage'],
        ['YES', str(vote_summary['yes']), f"{vote_summary['yes']/total_votes*100:.1f}%"],
        ['NO', str(vote_summary['no']), f"{vote_summary['no']/total_votes*100:.1f}%"],
        ['ABSTAIN', str(vote_summary['abstain']), f"{vote_summary['abstain']/total_votes*100:.1f}%"],
        ['TOTAL', str(total_votes), '100.0%']
    ]

    vote_table = Table(vote_table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    vote_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(vote_table)
    elements.append(Spacer(1, 0.3*inch))

    # SECTION 2: BILATERAL IMPACT ANALYSIS
    elements.append(PageBreak())
    elements.append(Paragraph("2. Israel Bilateral Relationship Impact", styles['CustomHeading']))
    elements.append(Spacer(1, 0.2*inch))

    impact_summary = bilateral_data['impact_summary']
    total_analyzed = bilateral_data['total_analyzed']

    bilateral_text = f"""An analysis of how the ceasefire vote affects Israel's bilateral
    relationships with {total_analyzed} UN member states reveals a nuanced diplomatic landscape.
    The analysis categorizes relationship impacts across seven levels, from significant strengthening
    to significant strain."""
    elements.append(Paragraph(bilateral_text, styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))

    # Impact distribution table
    impact_table_data = [['Impact Category', 'Countries', 'Percentage']]

    for category, count in impact_summary.items():
        pct = (count / total_analyzed * 100) if total_analyzed > 0 else 0
        display_name = category.replace('_', ' ').title()
        impact_table_data.append([display_name, str(count), f"{pct:.1f}%"])

    impact_table = Table(impact_table_data, colWidths=[3*inch, 1.25*inch, 1.25*inch])
    impact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    elements.append(impact_table)
    elements.append(Spacer(1, 0.3*inch))

    # SECTION 3: KEY FINDINGS
    elements.append(Paragraph("3. Key Findings", styles['CustomHeading']))
    elements.append(Spacer(1, 0.2*inch))

    # Count strengthened vs strained
    strengthened = (impact_summary.get('strengthened_significantly', 0) +
                   impact_summary.get('strengthened_moderately', 0) +
                   impact_summary.get('strengthened_slightly', 0))
    strained = (impact_summary.get('strained_significantly', 0) +
               impact_summary.get('strained_moderately', 0) +
               impact_summary.get('strained_slightly', 0))
    neutral = impact_summary.get('neutral', 0)

    findings = [
        f"• {strengthened} countries ({strengthened/total_analyzed*100:.1f}%) showed strengthened relations with Israel",
        f"• {strained} countries ({strained/total_analyzed*100:.1f}%) experienced strained relations",
        f"• {neutral} countries ({neutral/total_analyzed*100:.1f}%) maintained neutral bilateral status",
        f"• The overwhelming vote in favor ({vote_summary['yes']} yes votes) indicates broad international support for humanitarian ceasefire",
    ]

    for finding in findings:
        elements.append(Paragraph(finding, styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))

    elements.append(Spacer(1, 0.2*inch))

    # SECTION 4: REGIONAL BREAKDOWN
    elements.append(PageBreak())
    elements.append(Paragraph("4. Notable Country Analyses", styles['CustomHeading']))
    elements.append(Spacer(1, 0.2*inch))

    # Group by impact category - show top examples from each
    by_category = {}
    for analysis in bilateral_data['analyses']:
        cat = analysis['impact_analysis']['impact_category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(analysis)

    # Show examples from key categories
    key_categories = [
        ('strengthened_significantly', 'Relationships Significantly Strengthened'),
        ('strengthened_moderately', 'Relationships Moderately Strengthened'),
        ('strained_moderately', 'Relationships Moderately Strained'),
        ('strained_significantly', 'Relationships Significantly Strained'),
    ]

    for cat_key, cat_title in key_categories:
        if cat_key in by_category and by_category[cat_key]:
            elements.append(Paragraph(cat_title, styles['CustomSubHeading']))
            elements.append(Spacer(1, 0.1*inch))

            # Show up to 5 examples
            for analysis in by_category[cat_key][:5]:
                country_text = f"<b>{analysis['country']}</b> (Voted: {analysis['vote'].upper()})"
                elements.append(Paragraph(country_text, styles['Normal']))

                reasoning = analysis['impact_analysis']['reasoning']
                if len(reasoning) > 300:
                    reasoning = reasoning[:300] + "..."
                elements.append(Paragraph(reasoning, styles['Justified']))
                elements.append(Spacer(1, 0.15*inch))

            elements.append(Spacer(1, 0.2*inch))

    # Footer
    elements.append(PageBreak())
    elements.append(Paragraph("Methodology", styles['CustomHeading']))
    elements.append(Spacer(1, 0.2*inch))

    methodology = f"""This analysis was generated using AI-powered diplomatic analysis.
    Voting data was collected from {voting_data['total_votes']} UN member states.
    Bilateral impact assessments were conducted using {bilateral_data['model']}, analyzing
    each country's vote, official statement, and historical relationship context with Israel.

    Impact categories range from 'strengthened significantly' to 'strained significantly' based on
    factors including: historical relationship baseline, vote alignment, diplomatic tone, strategic
    implications, regional dynamics, and economic/security ties."""

    elements.append(Paragraph(methodology, styles['Justified']))
    elements.append(Spacer(1, 0.3*inch))

    footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elements.append(Paragraph(footer_text, ParagraphStyle('footer', parent=styles['Normal'],
                                                           fontSize=8, textColor=colors.grey)))

    # Build PDF
    print(f"Generating comprehensive PDF: {output_pdf}")
    doc.build(elements)
    print(f"✓ PDF generated successfully")

    return output_pdf


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive analysis PDF from voting and bilateral impact data"
    )
    parser.add_argument("motion_id", help="Motion ID (e.g., 01_gaza_ceasefire_resolution)")
    parser.add_argument("--output", type=Path, help="Output PDF path (optional)")

    args = parser.parse_args()

    if not check_dependencies():
        sys.exit(1)

    try:
        pdf_path = generate_comprehensive_pdf(args.motion_id, args.output)
        print(f"\n✓ Comprehensive analysis PDF: {pdf_path}")
        print(f"  Size: {pdf_path.stat().st_size / 1024:.1f} KB")
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
