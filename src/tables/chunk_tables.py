#column:value
def row_to_text(headers, row):
    if len(headers) == len(row):
        return "; ".join(f"{h}: {r}" for h,r, in zip(headers, row))
    if len(row)==len(headers)+1:
        return f"{row[0]}: "+"; ".join(f"{h}: {r}" for h,r in zip(headers, row[1:]))
    return f"Columns: {' | '.join(headers)}. Values: {' | '.join(row)}"

COUNTRY_NAMES={"RS": "Serbia", "RO": "Romania"}

def table_to_chunks(tables, country):
    chunks=[]
    name=COUNTRY_NAMES.get(country, country)
    for table in tables:
        for i, row in enumerate(table["data"]):
            chunks.append({
                "id": f"{table['source']}_{table['table_id']}_r{i}",
                "country": country,
                "source": table["source"],
                "page": table["page"],
                "section": table["caption"],
                "text": f"{name}. {table['caption']}. {row_to_text(table['headers'], row)}",
            })
    return chunks
