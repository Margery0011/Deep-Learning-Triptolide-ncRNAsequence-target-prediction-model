import pandas as pds


def load_sequence(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    data = [line for line in lines if line != '\n']
    seq_lines = data[1::2]
    name_lines = data[0::2]
    idx = [i for i in range(len(seq_lines)) if len(seq_lines[i]) < 25]
    seq = [seq_lines[i].strip() for i in idx]
    name = [name_lines[i].strip().split()[-1] for i in idx]
    return seq, name


def load_affinity(file):
    sheet = pds.read_excel(file, sheet_name='result')
    affinity_t = sheet.values[:, 2]
    affinity_t = [a for a in affinity_t]
    name_t = sheet.values[:, 0]
    name_t = [n.split('.')[0] for n in name_t]
    affi = []
    name = []
    idx_same = []
    for i, n in enumerate(name_t):
        if i not in idx_same:
            affi_t = [affinity_t[i]]
            for j in range(i + 1, len(name_t)):
                if name_t[j] == n:
                    affi_t.append(affinity_t[j])
                    idx_same.append(j)
            affi.append(sorted(affi_t)[0])
            name.append(n)
        else:
            continue
    return affi, name


def load_affinity_mean(file):
    sheet = pds.read_excel(file, sheet_name='result')
    affinity_t = sheet.values[:, 2]
    affinity_t = [a for a in affinity_t]
    name_t = sheet.values[:, 0]
    name_t = [n.split('.')[0] for n in name_t]
    num = sheet.values[:, 1]
    num = [n for n in num]
    affi = []
    name = []
    idx_same = []
    for i, n in enumerate(name_t):
        if i not in idx_same:
            affi_t = [affinity_t[i]]
            num_t = num[i]
            for j in range(i + 1, len(name_t)):
                if name_t[j] == n:
                    affi_t.append(affinity_t[j])
                    idx_same.append(j)
                    num_t += num[j]
            affi.append(sum(affi_t)/num_t)
            name.append(n)
        else:
            continue
    return affi, name


def load_affinity_rich(file):
    sheet = pds.read_excel(file, sheet_name='result')
    affinity_t = sheet.values[:, 2]
    affinity_t = [a for a in affinity_t]
    name_t = sheet.values[:, 0]
    name_t = [n.split('.')[0] for n in name_t]
    max_affi = max(affinity_t)
    min_affi = min(affinity_t)
    affi = []
    name = []
    idx_same = []
    for i, n in enumerate(name_t):
        if i not in idx_same:
            affi_t = [affinity_t[i]]
            for j in range(i + 1, len(name_t)):
                if name_t[j] == n:
                    affi_t.append(affinity_t[j])
                    idx_same.append(j)
            affi_sorted = sorted(affi_t)
            if (affi_sorted[0]-min_affi)/(max_affi-min_affi) > 0.75:
                for _ in range(6):
                    for af in affi_sorted:
                        affi.append(af)
                        name.append(n)
            elif (affi_sorted[0] - min_affi) / (max_affi - min_affi) < 0.25:
                for _ in range(10):
                    for af in affi_sorted:
                        affi.append(af)
                        name.append(n)
            elif (affi_sorted[0]-min_affi)/(max_affi-min_affi) > 0.6:
                for _ in range(2):
                    for af in affi_sorted:
                        affi.append(af)
                        name.append(n)
            elif (affi_sorted[0] - min_affi) / (max_affi - min_affi) < 0.4:
                for _ in range(2):
                    for af in affi_sorted:
                        affi.append(af)
                        name.append(n)
            else:
                for af in affi_sorted:
                    affi.append(af)
                    name.append(n)
        else:
            continue
    return affi, name


def load_affinity_smooth(file):
    sheet = pds.read_excel(file, sheet_name='result')
    affinity_t = sheet.values[:, 2]
    affinity_t = [a for a in affinity_t]
    name_t = sheet.values[:, 0]
    name_t = [n.split('.')[0] for n in name_t]
    max_affi = max(affinity_t)
    min_affi = min(affinity_t)
    affi = []
    name = []
    idx_same = []
    for i, n in enumerate(name_t):
        if i not in idx_same:
            affi_t = [affinity_t[i]]
            for j in range(i + 1, len(name_t)):
                if name_t[j] == n:
                    affi_t.append(affinity_t[j])
                    idx_same.append(j)
            affi_sorted = sorted(affi_t)
            if ((affi_sorted[0]-min_affi)/(max_affi-min_affi) > 0.7) | \
                    ((affi_sorted[0]-min_affi)/(max_affi-min_affi) < 0.35):
                for af in affi_sorted:
                    affi.append(af)
                    name.append(n)
            elif ((affi_sorted[0]-min_affi)/(max_affi-min_affi) > 0.55) | \
                    ((affi_sorted[0]-min_affi)/(max_affi-min_affi) < 0.45):
                for af in affi_sorted[:len(affi_sorted) // 2]:
                    affi.append(af)
                    name.append(n)
            else:
                affi.append(sorted(affi_t)[0])
                name.append(n)
        else:
            continue
    return affi, name


def cross_search(seq, name_seq, affi, name_affi):
    seq_res = []
    affi_res = []
    name_res = [n for n in name_seq if n in name_affi]
    for name in name_res:
        seq_res.append(seq[name_seq.index(name)])
        affi_res.append(affi[name_affi.index(name)])

    return seq_res, affi_res, name_res


def cross_search_smooth(seq, name_seq, affi, name_affi):
    seq_res = []
    affi_res = []
    name_res = []
    name_t = [n for n in name_seq if n in name_affi]
    for name in name_t:
        idx = [i for i, v in enumerate(name_affi) if v == name]
        for i in idx:
            name_res.append(name)
            seq_res.append(seq[name_seq.index(name)])
            affi_res.append(affi[i])

    return seq_res, affi_res, name_res


def load_mi(seq_file, affi_file):
    affi, name_affi = load_affinity(affi_file)
    seq, name_seq = load_sequence(seq_file)
    seq_res, affi_res, name_res = cross_search(seq, name_seq, affi, name_affi)
    return seq_res, affi_res, name_res


def load_mi_mean(seq_file, affi_file):
    affi, name_affi = load_affinity_mean(affi_file)
    seq, name_seq = load_sequence(seq_file)
    seq_res, affi_res, name_res = cross_search(seq, name_seq, affi, name_affi)
    return seq_res, affi_res, name_res


def load_mi_smooth(seq_file, affi_file):
    affi, name_affi = load_affinity_smooth(affi_file)
    seq, name_seq = load_sequence(seq_file)
    seq_res, affi_res, name_res = cross_search_smooth(seq, name_seq, affi, name_affi)
    return seq_res, affi_res, name_res


def load_mi_rich(seq_file, affi_file):
    affi, name_affi = load_affinity_rich(affi_file)
    seq, name_seq = load_sequence(seq_file)
    seq_res, affi_res, name_res = cross_search_smooth(seq, name_seq, affi, name_affi)
    return seq_res, affi_res, name_res


def load_pi(addr):
    with open(addr, 'r') as f:
        lines = f.readlines()
    data = [line for line in lines if line != '\n']
    seq = data[1::2]
    seq = [s.strip() for s in seq]
    name = data[0::2]
    name = [s.strip().split('|')[0] for s in name]
    name_pi = []
    for n in name:
        if n not in name_pi:
            name_pi.append(n)
    seq_pi = [seq[name.index(n)] for n in name_pi]
    return seq_pi, name_pi


def check(seq, affi, name):
    with open('homo-miRNA.txt', 'r') as f:
        lines = f.readlines()
    data = [line for line in lines if line != '\n']
    seq_lines = data[1::2]
    name_lines = data[0::2]
    sheet = pds.read_excel('original.xls', sheet_name='result')
    affinity_t = sheet.values[:, 2]
    affinity_t = [a for a in affinity_t]
    name_t = sheet.values[:, 0]
    name_t = [n.split('.')[0] for n in name_t]
    if (affi == affinity_t[name_t.index(name+'.pdb')]) & (seq == seq_lines[name_lines.index(name)]):
        return True
    else:
        return False
