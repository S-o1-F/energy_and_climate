
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

            if prev["caption"].startswith("Policy measure") or header_is_data(t, prev):
                t["data"]=[t["headers"]]+t["data"]
                t["headers"]=prev["headers"]
    return tables

def add_measure_captions(tables):
    for t in tables:
        if t["headers"] and t["headers"][0].startswith("Policy measure code"):
            if t["data"] and len(t["data"][0])==1:
                t["headers"][-1]=t["headers"][-1]+" "+t["data"][0][0]
                t["data"]=t["data"][1:]
            t["caption"]="Policy measure "+" ".join(t["headers"][1:])
    return tables

def use_manual_tables(tables, manual_tables):
    manual_ids={t["table_id"] for t in manual_tables}
    return [t for t in tables if t["table_id"] not in manual_ids]+manual_tables


def header_is_data(t, prev):
    return (len(t["headers"]) == len(prev["headers"])
            and t["headers"][0] != prev["headers"][0]
            and t["headers"][1:] != prev["headers"][1:])



def clean_tables(tables):
    cleaned=[clean_table(table) for table in tables]
    for t in cleaned:
        t["caption"]=t["caption"].replace("Error! No text of specified style in document.", "")
    cleaned=add_measure_captions(cleaned)
    return add_continued_captions(cleaned)

