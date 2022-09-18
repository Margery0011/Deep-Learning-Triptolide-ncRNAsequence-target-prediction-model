import numpy as np


def one_hot(seq):
    A_oh = [1, 0, 0, 0]
    U_oh = [0, 1, 0, 0]
    C_oh = [0, 0, 1, 0]
    G_oh = [0, 0, 0, 1]
    max_length = 0
    for rna in seq:
        if len(rna) > max_length:
            max_length = len(rna)

    seq_oh = np.zeros((4 * max_length, len(seq)))
    for i in range(len(seq)):
        j = 0
        for base in seq[i]:
            if base == 'A':
                seq_oh[4 * j:4 * (j + 1), i] = A_oh
            elif base == 'U':
                seq_oh[4 * j:4 * (j + 1), i] = U_oh
            elif base == 'C':
                seq_oh[4 * j:4 * (j + 1), i] = C_oh
            elif base == 'G':
                seq_oh[4 * j:4 * (j + 1), i] = G_oh
            j += 1

    return seq_oh


def shape2_3d(x):
    x_3d = np.zeros((x.shape[1], int(x.shape[0]/4), 4))
    for i in range(x.shape[1]):
        for j in range(int(x.shape[0]/4)):
            for k in range(4):
                x_3d[i, j, k] = x[4*j + k, i]

    return x_3d


def normalize(affi):
    max_affi = max(affi)
    min_affi = min(affi)
    affi_n = np.zeros((1, len(affi)))
    for i in range(len(affi)):
        affi_n[:, i] = (affi[i] - min_affi) / (max_affi - min_affi)
    return affi_n, max_affi, min_affi


def classify(affi):
    affi_c = np.zeros((affi.shape[0],3))
    high = [1, 0, 0]
    mid = [0, 1, 0]
    low = [0, 0, 1]
    for i in range(affi.shape[0]):
        if affi[i] > 0.6:
            affi_c[i] = high
        elif affi[i] < 0.4:
            affi_c[i] = low
        else:
            affi_c[i] = mid
    return affi_c


def classify2(affi):
    affi_c = np.zeros((affi.shape[0], 1))
    high = 1
    low = 0
    for i in range(affi.shape[0]):
        if affi[i] > 0.5:
            affi_c[i] = high
        else:
            affi_c[i] = low
    return affi_c


def choose(seq, name, affi):
    caches = []
    affi = list(affi[0])
    for i in range(len(seq)):
        caches.append((seq[i], name[i], affi[i]))
    rare = []
    mid = []
    well = []
    for cache in caches:
        if (cache[2] > 0.75) | (cache[2] < 0.25):
            rare.append(cache)
        elif (cache[2] > 0.6) | (cache[2] < 0.4):
            mid.append(cache)
        else:
            well.append(cache)

    mid_idx = np.random.choice(len(mid), len(mid), replace=True)
    well_idx = np.random.choice(len(well), len(well), replace=True)
    caches = []
    for idx in mid_idx:
        caches.append(mid[idx])
    for idx in well_idx:
        caches.append(well[idx])
    for cache in rare:
        caches.append(cache)
    np.random.shuffle(caches)
    seq_r = []
    affi_r = np.zeros((1, len(caches)))
    name_r = []
    for i, cache in enumerate(caches):
        seq_r.append(cache[0])
        name_r.append(cache[1])
        affi_r[:, i] = cache[2]

    return seq_r, name_r, affi_r