import sys

def _format_attr(attr, width):
    s = ''
    a = attr[0]
    len_a = len(a)
    start = int(width / 2) - int(len_a / 2)
    for i in range(0, start):
        s += ' '
    s += a
    for i in range(0, width - start - len_a):
        s += ' '
    return s

def _maxlen(lines):
    m = 0
    for l in lines:
        len_l = len(l)
        if len_l > m:
            m = len_l
    return m

def _rstrip_lines(lines):
    newlines = []
    for l in lines:
        newlines.append(l.rstrip())
    return newlines

def _format_row(row, attrs, width):
    s = ''
    # Count number of lines
    rowlines = []
    maxlen = []
    maxlines = 1
    for i, data in enumerate(row):
        lines = ['']
        if data is not None:
            lines = _rstrip_lines(str(data).splitlines())
        maxlen.append(_maxlen(lines))
        rowlines.append(lines)
        lines_len = len(lines)
        if lines_len > maxlines:
            maxlines = lines_len
    # Write lines
    for i in range(0, maxlines):
        for j, lines in enumerate(rowlines):
            s += ' ' if j == 0 else '| '
            if attrs[j][1] == 'NUMBER':
                start = width[j] - maxlen[j]
            else:
                start = 0
            for k in range(0, start):
                s += ' '
            if i < len(lines):
                s += lines[i]
            else:
                s += ' '
            for k in range(0, width[j] - start - maxlen[j]):
                s += ' '
            s += ' '
        s += '\n'
    return s

def _select(db, table, limit=None, file=sys.stdout):
    query = 'SELECT * FROM "'+table+'"'
    if limit is not None:
        query += ' LIMIT '+str(limit)
    cur = db.cursor()
    cur.execute(query)
    attrs = []
    width = []
    for a in cur.description:
        attrs.append( (a[0], a[1]) )
        width.append(len(a[0]))
    ncols = len(attrs)
    while True:
        row = cur.fetchone()
        if row is None:
            break
        for i, v in enumerate(row):
            lines = ['']
            if v is not None:
                lines = str(v).splitlines()
            for j, l in enumerate(lines):
                len_l = len(l.rstrip())
                if len_l > width[i]:
                    width[i] = len_l
    cur = db.cursor()
    cur.execute(query)
    # Attribute names
    s = ''
    for i, v in enumerate(attrs):
        s += ' ' if i == 0 else '| '
        s += _format_attr(attrs[i], width[i])
        s += ' '
    print(s, file=file)
    # Header bar
    s = ''
    for i in range(0, ncols):
        s += '' if i == 0 else '+'
        s += '-'
        for j in range(0, width[i]):
            s += '-'
        s += '-'
    print(s, file=file)
    # Data rows
    row_i = 0
    while True:
        row = cur.fetchone()
        if row is None:
            break
        s = _format_row(row, attrs, width)
        print(s, end ='', file=file)
        row_i += 1
    print('('+str(row_i)+' '+('row' if row_i == 1 else 'rows')+')', file=file)
    print('', file=file)

