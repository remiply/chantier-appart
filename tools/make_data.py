"""Reconstruit data.json à partir d'un export ArtifactData (dossiers rooms/ tasks/ items/ remarks/ de fichiers <id>.json).
Usage : python3 tools/make_data.py <dossier_export> data.json"""
import json, os, sys, glob, datetime
exp, out = sys.argv[1], sys.argv[2]
MAP = {'https://claude.ai/artifact/H9vvyYSNcEPatKi2qUv87s': 'toilettes.html',
       'https://claude.ai/artifact/K21nNqPWbyu9P6ypDaasxc': 'montage-toilettes.html',
       'https://claude.ai/artifact/FTPiRMvcnm2Hi6ALYrg9zE': 'index.html'}
data = {}
for col in ['rooms', 'tasks', 'items', 'remarks']:
    rows = []
    for f in sorted(glob.glob(os.path.join(exp, col, '*.json'))):
        d = json.load(open(f)); d['id'] = os.path.splitext(os.path.basename(f))[0]
        if isinstance(d.get('link'), str):
            for a, b in MAP.items(): d['link'] = d['link'].replace(a, b)
        rows.append(d)
    data[col] = rows
if not data['rooms']: sys.exit('export vide : data.json non modifié')
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1)))
data['updated'] = now.strftime('%d/%m/%Y à %Hh%M')
json.dump(data, open(out, 'w'), ensure_ascii=False)
print('ok', {k: len(v) for k, v in data.items() if isinstance(v, list)})
