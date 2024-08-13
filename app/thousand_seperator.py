# format is in lakhs and crores
def thousand_seperator_func(n):
    """
    Thousand seperator for indian system 100000.99 => 1,00,000.99
    """
    s = str(n)
    c = 2
    new_s = ''
    i = 0
    if '.' in s:
        s, int_part = s.split('.')
    else:
        int_part = ''
    while i < len(s):
        if i == c and not len(s)-i < 2:
            new_s = ',' + s[len(s)-1-i] + new_s
            c += 2
        else:
            new_s = s[len(s)-1-i] + new_s
        i += 1
    return new_s + '.' + int_part

#         if i == 3 or (i > 3 and (i - 3) % 2 == 0):
#  could have used this logic also
