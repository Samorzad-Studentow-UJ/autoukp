import argparse
import csv
import datetime
import locale
import os.path
from dataclasses import dataclass

from abbreviations import expand_name
from jijnatex import render_pdf

locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')

parser = argparse.ArgumentParser(description='Generuj dokumenty z posiedzenia Zarządu SSUJ.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--projects', type=str, default=None, help='Lista projektów CSV')
parser.add_argument('--date', type=lambda s: datetime.date.fromisoformat(s), default=datetime.date.today())
parser.add_argument('--start_time', type=str)
parser.add_argument('--end_time', type=str)
parser.add_argument('--start_idx', type=int)
parser.add_argument('--out_dir', type=str)

args = parser.parse_args()

next_idx = args.start_idx


@dataclass
class Project:
    idx: int
    entity: str
    amountRequested: float
    amountReceived: float
    title: str
    signature: str
    category: int
    year: int
    votesFor: int
    votesAgainst: int
    votesAbstain: int
    remarks: str


projects = []

os.makedirs(args.out_dir, exist_ok=True)

with open(args.projects) as projects_file:
    projects_csv = csv.DictReader(projects_file)
    for row in projects_csv:
        projects.append(Project(
            entity=expand_name(row['komu przyznano lub nie']),
            amountRequested=float(row['kwota wnioskowana'].replace(',', '.')),
            amountReceived=float(row['kwota przyznana'].replace(',', '.')),
            title=row['tytuł'],
            signature=row['sygnatura'],
            category=int(row['kategoria']),
            year=int(row['rok budżetowy']),
            votesFor=int(row['za']),
            votesAgainst=int(row['przeciw']),
            votesAbstain=int(row['wstrzymujące']),
            idx=next_idx if row['za'] > row['przeciw'] else -1,
            remarks=row['uwagi do protokołu']
        ))
        next_idx += 1 if row['za'] > row['przeciw'] else 0

render_pdf('zarzad_ssuj_protokol', {
    'date': args.date,
    'startTime': args.start_time,
    'endTime': args.end_time,
    'projects': projects,
}, os.path.join(args.out_dir, 'Protokół.pdf'))


render_pdf('zarzad_ssuj_obecnosc', {
    'date': args.date,
}, os.path.join(args.out_dir, 'Obecność.pdf'))

for project in projects:
    if project.idx > 0:
        render_pdf('zarzad_ssuj_projekt', {
            'project': project,
            'date': args.date,
        }, os.path.join(args.out_dir, 'Z-U-17-2021-{:03}.pdf'.format(project.idx)))
