"""Proportions, record-clustered bootstrap intervals, and paired sign-flip permutation tests."""
from collections import defaultdict

B_BOOT = 2000
B_PERM = 10000


def proporsi(baris, kunci="benar"):
    n = sum(len(b["besaran"]) for b in baris)
    k = sum(sum(1 for x in b["besaran"] if x[kunci]) for b in baris)
    return k, n


def ci_bootstrap(baris, kunci="benar", rng=None):
    """95 % percentile interval, resampling records with replacement."""
    per = defaultdict(lambda: [0, 0])
    for b in baris:
        for x in b["besaran"]:
            per[b["rekaman"]][0] += bool(x[kunci])
            per[b["rekaman"]][1] += 1
    gugus = list(per.values())
    if not gugus:
        return None
    nilai = []
    for _ in range(B_BOOT):
        s = [gugus[rng.randrange(len(gugus))] for _ in gugus]
        nilai.append(sum(a for a, _ in s) / sum(n for _, n in s))
    nilai.sort()
    return nilai[int(0.025 * B_BOOT)], nilai[int(0.975 * B_BOOT) - 1]


def per_tugas(baris):
    per = defaultdict(lambda: [0, 0])
    for b in baris:
        for x in b["besaran"]:
            per[b["tugas"]][0] += bool(x["benar"])
            per[b["tugas"]][1] += 1
    return {t: a / n for t, (a, n) in per.items()}


def uji_permutasi(a, b, rng):
    """Two-sided paired test flipping the sign per task; statistic = mean difference in proportion."""
    sama = sorted(set(a) & set(b))
    beda = [a[t] - b[t] for t in sama]
    if not beda:
        return None, None, 0
    obs = sum(beda) / len(beda)
    if all(d == 0 for d in beda):
        return obs, 1.0, len(beda)
    lebih = 0
    for _ in range(B_PERM):
        s = sum(d if rng.random() < 0.5 else -d for d in beda) / len(beda)
        lebih += abs(s) >= abs(obs) - 1e-12
    return obs, (lebih + 1) / (B_PERM + 1), len(beda)
