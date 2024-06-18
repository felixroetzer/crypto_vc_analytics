import json
from collections import defaultdict


POSTFIXES = [
    'capital',
    'ventures',
    'venture',
    'trading',
    'labs',
    'lab',
    'digital',
    'holdings',
    'group',
    'research',
    'management',
    'holding',
    'assets'
    'fund',
]


success_projects = set()
vc_stats = defaultdict(lambda: {'lead': [], 'non_lead': [], 'non_success': []})


with open('/Users/felixrotzer/downloads/success_projects.txt', 'r') as f:
    for project in f:
        success_projects.add(project.strip().lower())

with open('/Users/felixrotzer/downloads/fundraises.json', 'r') as f:
    fundraise_data = json.load(f)['raises']


for fundraise in fundraise_data:
    name = fundraise['name'].strip().lower()
    level = fundraise['round']

    if not level:
        continue
    else:
        level = level.strip().lower()

    if 'seed' in level or 'angel' in level:
        date = fundraise['date']
        amount = fundraise['amount']
        chains = fundraise['chains']
        sector = fundraise['sector']
        category = fundraise['category']
        valuation = fundraise['valuation']
        all_investors = {'lead': fundraise['leadInvestors'], 'non_lead': fundraise['otherInvestors']}
        is_success_project = name in success_projects

        for investor_type, investors in all_investors.items():
            for investor in investors:
                investor = investor.strip().lower()

                for postfix in POSTFIXES:
                    investor = investor.replace(f' {postfix}', '')
                investor = investor.replace('.io', '').strip()

                if is_success_project:
                    vc_stats[investor][investor_type].append(name)
                else:
                    vc_stats[investor]['non_success'].append(name)


vc_stats_list = []

for vc, stats in vc_stats.items():
    vc_stats_list.append({
        'name': vc,
        'lead': stats['lead'],
        'non_lead': stats['non_lead'],
        'non_success': stats['non_success'],
        'num_lead': len(stats['lead']),
        'num_non_lead': len(stats['non_lead']),
        'num_non_success': len(stats['non_success']),
        'total_num': len(stats['lead']) + len(stats['non_lead']),
    })

vc_stats_list.sort(key=lambda x: x['total_num'], reverse=True)


for stats in vc_stats_list:
    if stats["total_num"]:
        total = stats["total_num"] + stats["num_non_success"]
        hit_rate = round(stats["total_num"] / total * 100, 2)
        print(f'{stats["name"]}: {stats["total_num"]} ({stats["num_lead"]} as lead), {stats["num_non_success"]} non success, {hit_rate}% hit rate')
        if stats["lead"]:
            print(f'Lead: {", ".join(stats["lead"])}')
        if stats["non_lead"]:
            print(f'Non-Lead: {", ".join(stats["non_lead"])}')
        print()
