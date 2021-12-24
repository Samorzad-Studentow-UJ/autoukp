UJ = 'Uniwersytetu Jagiellońskiego'
SS = f'Samorządu Studentów'
WRSS = 'Wydziałowej Radzie'
WRSSy = {f'WRSS W{k}': f'{WRSS} {SS} Wydziału {v} {UJ}' for k, v in {
    'PiA': 'Prawa i Administracji',
    'L': 'Lekarskiego',
    'Farm': 'Farmaceutycznego',
    'NoZ': 'Nauk o Zdrowiu',
    'Fz': 'Filozoficznego',
    'Fl': 'Filologicznego',
    'H': 'Historycznego',
    'P': 'Polonistyki',
    'FAIS': 'Fizyki, Astronomii i Informatyki Stosowanej',
    'MiI': 'Matematyki i Informatyki',
    'Chem': 'Chemii',
    'B': 'Biologii',
    'ZiKS': 'Zarządzania i Komunikacji Społecznej',
    'SMiP': 'Studiów Międzynarodowych i Politycznych',
    'BBiB': 'Biochemii, Biofizyki i Biotechnologii',
    'GiG': 'Geografii i Geologii'
}.items()}

WRSSy['RSS MISH'] = f'Radzie {SS} Międzywydziałowych Indywidualnych Studiów Humanistycznych {UJ}'
SSUJ = f'{SS} {UJ}'


def expand_name(name: str):
    if name in WRSSy:
        return WRSSy[name]
    return name.replace('SSUJ', SSUJ)
