#label config

base_label_name = {
    'provinsi': 'PROV',
    'kabupaten': 'KAB',
    'nik': 'NIK',
    'nama': 'NAMA',
    'ttl': 'TTL',
    'gender': 'GDR',
    'goldar': 'GLD',
    'alamat': 'ADR',
    'rtrw': 'RTW',
    'kelurahan': 'KLH',
    'kecamatan': 'KCM',
    'agama': 'RLG',
    'perkawinan': 'KWN',
    'pekerjaan': 'KRJ',
    'kewarganegaraan': 'WRG',
    'berlaku': 'BLK',
    'sign_place': 'SGP',
    'sign_date': 'SGD'
}

label_colors = {
 'PROV': (0, 255, 0),
 'KAB': (209, 1, 246),
 'NIK': (255, 127, 0),
 'NAMA': (0, 255, 255),
 'TTL': (0, 0, 255),
 'GDR': (127, 255, 127),
 'GLD': (83, 126, 46),
 'ADR': (251, 126, 187),
 'RTW': (131, 90, 236),
 'KLH': (255, 255, 0),
 'KCM': (0, 255, 255),
 'RLG': (63, 30, 136),
 'KWN': (131, 90, 236),
 'KRJ': (255, 127, 0),
 'WRG': (139, 211, 2),
 'BLK': (0, 255, 127),
 'SGP': (236, 212, 128),
 'SGD': (255, 0, 127),
  "O" : (0,0,0)
}
 

label_to_name = dict((v,k) for k,v in base_label_name.items())

base_label_type = {
    'field': "FLD",
    'value': "VAL",
    "delimiter": "O"
}

line_number = ['L0','L1','L2']

def labels_map_process(label_name, label_type):
    labels=[]
    for kn, vn in label_name.items():
        for kt, vt in label_type.items():
            if kt!='delimiter':
                for bil in "BILU":
                    name = f'{bil}-{vt}_{vn}'
                    labels.append(name)
    labels.append("O")
    
    nlabels = []
    for idx, txt in enumerate(labels):
        for ln in line_number:
            if "VAL" in txt: nlabels.append(f'{ln}-{txt}')
        if not ("VAL" in txt): nlabels.append(txt)


    sorter = lambda x: (x.split("-")[-1].split("_")[0])
    nlabels = sorted(nlabels, key=sorter)
    
    sorter = lambda x: (x.split("-")[-1].split("_")[-1])
    nlabels = sorted(nlabels, key=sorter)
    
    return nlabels


label_map = labels_map_process(base_label_name, base_label_type)
label_to_idx = dict((label,idx) for idx, label in enumerate(label_map))
idx_to_label = dict((idx, label) for idx, label in enumerate(label_map))
idx_to_label[-100] = "Unknown" 
num_labels = len(label_map)