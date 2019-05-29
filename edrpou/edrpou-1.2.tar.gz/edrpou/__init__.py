def valid8(code):

    weights = list(range(1, 8))

    if 30000000 < int(code) < 60000000:
        weights = [weights[-1]] + weights[:-1]
    digit = sum([weights[i] * int(c) for i, c in enumerate(code[:7])])

    if digit % 11 == 10:
        digit = sum([(weights[i] + 2) * int(c) for i, c in enumerate(code[:7])])

    c_digit = str(digit % 11)[-1]

    return c_digit == code[-1], c_digit


def valid10(code):
    weights = [-1, 5, 7, 9, 4, 6, 10, 5, 7]
    digit = 0
    for i, c in enumerate(code[:9]):
        digit += weights[i] * int(c)
    digit = digit % 11
    if digit == 10:
        digit = digit % 10

    return str(digit) == code[-1], str(digit)


def valid(code):
    res = False, -1
    work_code = str(code).strip()
    if work_code.isnumeric():
        work_code = str(int(work_code))
        if len(work_code) <= 8:
            work_code = work_code.zfill(8)
        else:
            work_code = work_code.zfill(10)
        if len(work_code) == 8:
            res = valid8(work_code)
        if len(work_code) == 10:
            res = valid10(work_code)

        return (*res, work_code)
