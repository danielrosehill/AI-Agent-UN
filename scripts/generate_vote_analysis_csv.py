#!/usr/bin/env python3
"""
Generate CSV analysis from UN vote simulation results.

This script processes the JSON results from a UN vote simulation and generates
a CSV file with detailed analysis including vote distribution, regional patterns,
and statement characteristics.
"""

import json
import csv
import sys
from pathlib import Path
from collections import Counter


def load_vote_data(json_path):
    """Load vote data from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def classify_region(country):
    """Classify country into UN regional group."""
    # Regional classifications based on UN regional groups
    regions = {
        'Africa': [
            'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi',
            'Cameroon', 'Cape Verde', 'Central African Republic', 'Chad', 'Comoros',
            'Congo', 'Cote Divoire', 'Democratic Republic Of Congo', 'Djibouti',
            'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia',
            'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea Bissau', 'Kenya',
            'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali',
            'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia',
            'Niger', 'Nigeria', 'Rwanda', 'Sao Tome And Principe', 'Senegal',
            'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan',
            'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
        ],
        'Asia-Pacific': [
            'Afghanistan', 'Australia', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei',
            'Cambodia', 'China', 'East Timor', 'Fiji', 'India', 'Indonesia', 'Iran',
            'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kiribati', 'Kuwait',
            'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Marshall Islands',
            'Micronesia Country', 'Mongolia', 'Myanmar', 'Nauru', 'Nepal', 'New Zealand',
            'North Korea', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Papua New Guinea',
            'Philippines', 'Qatar', 'Samoa', 'Saudi Arabia', 'Singapore', 'Solomon Islands',
            'South Korea', 'Sri Lanka', 'Syria', 'Tajikistan', 'Thailand', 'Tonga',
            'Turkey', 'Turkmenistan', 'Tuvalu', 'United Arab Emirates', 'Uzbekistan',
            'Vanuatu', 'Vietnam', 'Yemen'
        ],
        'Eastern Europe': [
            'Albania', 'Armenia', 'Azerbaijan', 'Belarus', 'Bosnia And Herzegovina',
            'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Estonia', 'Georgia',
            'Hungary', 'Latvia', 'Lithuania', 'Moldova', 'Montenegro', 'North Macedonia',
            'Poland', 'Romania', 'Russia', 'Serbia', 'Slovakia', 'Slovenia', 'Ukraine'
        ],
        'Latin America & Caribbean': [
            'Antigua And Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia',
            'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica',
            'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala',
            'Guyana', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama',
            'Paraguay', 'Peru', 'Saint Kitts And Nevis', 'Saint Lucia',
            'Saint Vincent And The Grenadines', 'Suriname', 'Trinidad And Tobago',
            'Uruguay', 'Venezuela'
        ],
        'Western Europe & Others': [
            'Andorra', 'Austria', 'Belgium', 'Canada', 'Denmark', 'Finland', 'France',
            'Germany', 'Greece', 'Holy See', 'Iceland', 'Ireland', 'Italy', 'Liechtenstein',
            'Luxembourg', 'Malta', 'Monaco', 'Netherlands', 'Norway', 'Portugal',
            'San Marino', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom', 'United States'
        ]
    }

    for region, countries in regions.items():
        if country in countries:
            return region
    return 'Other'


def classify_income_group(country):
    """Classify country by World Bank income group (simplified)."""
    # Simplified classification - in production, use World Bank data
    high_income = [
        'United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Japan',
        'Australia', 'South Korea', 'Italy', 'Spain', 'Netherlands', 'Switzerland',
        'Sweden', 'Norway', 'Denmark', 'Finland', 'Austria', 'Belgium', 'Ireland',
        'Luxembourg', 'Singapore', 'New Zealand', 'Israel', 'United Arab Emirates',
        'Qatar', 'Kuwait', 'Saudi Arabia', 'Bahrain', 'Oman', 'Iceland', 'Portugal',
        'Greece', 'Slovenia', 'Czechia', 'Estonia', 'Slovakia', 'Lithuania', 'Latvia',
        'Poland', 'Hungary', 'Croatia', 'Chile', 'Uruguay', 'Argentina', 'Trinidad And Tobago',
        'Barbados', 'Antigua And Barbuda', 'Saint Kitts And Nevis', 'Seychelles', 'Palau'
    ]

    if country in high_income:
        return 'High Income'
    else:
        return 'Low-Middle Income'


def check_membership(country):
    """Check various organizational memberships."""
    # Major groupings
    eu_members = [
        'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark',
        'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland',
        'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland',
        'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden'
    ]

    nato_members = [
        'Albania', 'Belgium', 'Bulgaria', 'Canada', 'Croatia', 'Czechia', 'Denmark',
        'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
        'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Montenegro', 'Netherlands',
        'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia',
        'Slovenia', 'Spain', 'Turkey', 'United Kingdom', 'United States'
    ]

    oic_members = [
        'Afghanistan', 'Albania', 'Algeria', 'Azerbaijan', 'Bahrain', 'Bangladesh',
        'Benin', 'Brunei', 'Burkina Faso', 'Cameroon', 'Chad', 'Comoros',
        'Cote Divoire', 'Djibouti', 'Egypt', 'Gabon', 'Gambia', 'Guinea',
        'Guinea Bissau', 'Guyana', 'Indonesia', 'Iran', 'Iraq', 'Jordan',
        'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Lebanon', 'Libya', 'Malaysia',
        'Maldives', 'Mali', 'Mauritania', 'Morocco', 'Mozambique', 'Niger',
        'Nigeria', 'Oman', 'Pakistan', 'Palestine', 'Qatar', 'Saudi Arabia',
        'Senegal', 'Sierra Leone', 'Somalia', 'Sudan', 'Suriname', 'Syria',
        'Tajikistan', 'Togo', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda',
        'United Arab Emirates', 'Uzbekistan', 'Yemen'
    ]

    arab_league = [
        'Algeria', 'Bahrain', 'Comoros', 'Djibouti', 'Egypt', 'Iraq', 'Jordan',
        'Kuwait', 'Lebanon', 'Libya', 'Mauritania', 'Morocco', 'Oman', 'Palestine',
        'Qatar', 'Saudi Arabia', 'Somalia', 'Sudan', 'Syria', 'Tunisia',
        'United Arab Emirates', 'Yemen'
    ]

    return {
        'EU': country in eu_members,
        'NATO': country in nato_members,
        'OIC': country in oic_members,
        'Arab_League': country in arab_league
    }


def analyze_statement(statement):
    """Analyze statement for key themes."""
    if not statement:
        return {}

    statement_lower = statement.lower()

    return {
        'mentions_humanitarian': 'humanitarian' in statement_lower,
        'mentions_two_state': 'two-state' in statement_lower or 'two state' in statement_lower,
        'mentions_accountability': 'accountabil' in statement_lower,
        'mentions_international_law': 'international law' in statement_lower or 'international humanitarian law' in statement_lower,
        'mentions_civilian': 'civilian' in statement_lower,
        'mentions_reconstruction': 'reconstruction' in statement_lower or 'rebuilding' in statement_lower,
        'mentions_security': 'security' in statement_lower,
        'mentions_hamas': 'hamas' in statement_lower,
        'mentions_occupation': 'occupation' in statement_lower or 'occupied' in statement_lower,
        'mentions_blockade': 'blockade' in statement_lower or 'restrictions' in statement_lower,
        'statement_length': len(statement.split())
    }


def generate_analysis_csv(json_path, csv_path):
    """Generate detailed CSV analysis from vote JSON."""
    data = load_vote_data(json_path)

    # Prepare rows
    rows = []
    for vote_record in data['votes']:
        country = vote_record['country']
        vote = vote_record['vote']
        statement = vote_record['statement']

        # Base data
        row = {
            'Country': country,
            'Country_Slug': vote_record['country_slug'],
            'Vote': vote,
            'Region': classify_region(country),
            'Income_Group': classify_income_group(country),
        }

        # Add membership data
        memberships = check_membership(country)
        row.update(memberships)

        # Add statement analysis
        statement_analysis = analyze_statement(statement)
        row.update(statement_analysis)

        # Add statement text (last to keep it at end of CSV)
        row['Statement'] = statement

        rows.append(row)

    # Write CSV
    fieldnames = [
        'Country', 'Country_Slug', 'Vote', 'Region', 'Income_Group',
        'EU', 'NATO', 'OIC', 'Arab_League',
        'mentions_humanitarian', 'mentions_two_state', 'mentions_accountability',
        'mentions_international_law', 'mentions_civilian', 'mentions_reconstruction',
        'mentions_security', 'mentions_hamas', 'mentions_occupation', 'mentions_blockade',
        'statement_length', 'Statement'
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Generated CSV analysis: {csv_path}")
    print(f"  Total votes: {len(rows)}")

    # Print summary statistics
    vote_counts = Counter(row['Vote'] for row in rows)
    print(f"\nVote Summary:")
    print(f"  YES: {vote_counts['yes']}")
    print(f"  NO: {vote_counts['no']}")
    print(f"  ABSTAIN: {vote_counts['abstain']}")

    # Regional breakdown
    print(f"\nRegional Breakdown:")
    regions = {}
    for row in rows:
        region = row['Region']
        vote = row['Vote']
        if region not in regions:
            regions[region] = {'yes': 0, 'no': 0, 'abstain': 0}
        regions[region][vote] += 1

    for region, counts in sorted(regions.items()):
        total = sum(counts.values())
        print(f"  {region}: {counts['yes']} yes, {counts['no']} no, {counts['abstain']} abstain ({total} total)")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        # Default to latest results
        json_path = 'tasks/reactions/01_gaza_ceasefire_resolution_latest.json'

    # Determine output path
    json_file = Path(json_path)
    csv_path = json_file.parent.parent / 'analysis' / f"{json_file.stem}_analysis.csv"

    # Create analysis directory if needed
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate CSV
    generate_analysis_csv(json_path, csv_path)


if __name__ == '__main__':
    main()
