
def clean_cell(value):
    if value is None:
        return ""

    return " ".join(value.split())

def remove_empty(cells):
    return [c for c in cells if c]

def merge_header_rows(headers, rows):
    headers=list(headers)
    while len(rows)>1 and len(remove_empty(rows[0]))==1 and len(remove_empty(rows[0])[0])<=30:
        for j,cell in enumerate(rows[0]):
            if cell:
                k=j
                while k>0 and not headers[k]:
                    k-=1
                headers[k]=f"{headers[k]} {cell}" if headers[k] else cell
        rows=rows[1:]
    return headers,rows

def merge_wrapped_rows(rows):
    merged=[]
    for row in rows:
        filled=[j for j, c in enumerate(row) if c]
        if merged and len(filled)==1 and merged[-1][filled[0]]:
            j=filled[0]
            merged[-1][j]=f"{merged[-1][j]} {row[j]}"
        else:
            merged.append(list(row))
    return merged


def clean_table(table):
    headers=[clean_cell(h) for h in table["headers"]]
    rows=[[clean_cell(c) for c in row] for row in table["data"]]
    headers,rows=merge_header_rows(headers,rows)
    rows=merge_wrapped_rows(rows)

    headers=remove_empty(headers)
    rows=[remove_empty(row) for row in rows]
    rows=[row for row in rows if row]

    return{
        **table,
        "headers": headers,
        "data": rows
    }

def add_continued_captions(tables):
    for i in range(1, len(tables)):
        prev=tables[i-1]
        t=tables[i]
        if not t["caption"] and t["source"]==prev["source"] and t["page"]==prev["page"]+1:
            t["caption"]=prev["caption"]
            t["continued"]=True
    return tables


def clean_tables(tables):
    cleaned=[clean_table(table) for table in tables]
    return add_continued_captions(cleaned)

