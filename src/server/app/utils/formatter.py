def to_abnum(x: int):
    abbrs = ['', 'K', 'M', 'B', 'T', 'Qd', 'Qn', 'Sx', 'Sp']
    if x >= 10 ** 27:
        return 'INF'
    else:
        for i in range(len(abbrs)):
            unit = 10 ** (i * 3)
            limit = 10 ** ((i + 1) * 3)
            if abs(x) < limit:
                n = int(round((x / unit) * 100)) // 100
                return f'{n:g}{abbrs[i]}'