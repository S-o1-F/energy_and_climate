import re

def is_year(text):
    return re.fullmatch(r"(19|20)\d\d", text.strip()) is not None

def has_letters(text):
    return re.search(r"[A-Za-z]", text) is not None

def has_digits(text):
    return re.search(r"\d", text) is not None

def clean_numbers(text):
    number=re.sub(r"[^\d.,%]", "", text)
    if "%" in text and text.strip().startswith("-"):
        number="-"+number
    return number

def split_numbers(text):
    glued=re.findall(r"\d{1,3}\.\d{3}", text)
    if len(glued)>1:
        return glued
    return [clean_numbers(text)]

def center(box):
    #[x,y,width,height] od ocr
    x,y,width,height=box
    #centar
    return x+width/2,y+height/2

def closest_year(x, years):
    best_year=None
    best_distance=None
    for year, year_x in years:
        distance=abs(year_x-x)
        if best_distance is None or distance < best_distance:
            best_year=year
            best_distance=distance
    return best_year

#chart7, how to sort the values
def order_top_to_bottom(values):
    values = sorted(values, key=lambda v: v[1], reverse=True) #v[1] e y
    return [number for x, y, number in values]

def order_left_to_right(values):
    values = sorted(values, key=lambda v: v[0]) #v[0] e x
    return [number for x, y, number in values]

#same x->stacked bar, different x->grouped bars
def type_of_chart(values):
    '''rounded=[round(x,2) for x, y, number in values]
    most_common=0
    for position in rounded:
        if rounded.count(position)>most_common:
            most_common=rounded.count(position)
    return most_common<=len(rounded)/2'''
    xs=sorted(x for x,y,number in values)
    middle=xs[len(xs)//2]
    same_column=0
    for x in xs:
        if abs(x-middle)<=0.025:
            same_column+=1
    return same_column<=len(xs)/2

def is_short_label(text):
    return has_letters(text) and len(text.strip())<=6

def labels_on_bottom_line(labels):
    ys=sorted(y for label,x,y in labels)
    middle=ys[len(ys)//2]
    result=[]
    for label,x,y in labels:
        if abs(y-middle)<=0.03:
            result.append((label,x))
    return result

def find_x_axis_labels(ocr_results):
    years=[]
    words=[]
    for text, confidence, box in ocr_results:
        x,y=center(box)
        if is_year(text):
            years.append((text.strip(), x,y))
        elif is_short_label(text):
            words.append((text.strip(), x,y))
    if years:
        return labels_on_bottom_line(years)
    if words:
        return labels_on_bottom_line(words)
    return []


def values_per_label(ocr_results):
    #year or word
    labels=find_x_axis_labels(ocr_results)
    if not labels:
        return None
    first_x=min(x for label,x in labels)

    #numbers on y-axis
    left_numbers=0
    for text, confidence, box in ocr_results:
        x,y=center(box)
        if has_digits(text) and not has_letters(text) and x<first_x-0.04:
            left_numbers+=1
    has_y_axis=left_numbers>=3

    #put number under the closest year
    groups={}
    for text, confidence, box in ocr_results:
        if is_year(text) or has_letters(text) or not has_digits(text):
            continue
        x,y=center(box)
        if has_y_axis and x<first_x-0.04:
            continue
        label=closest_year(x, labels)
        if label not in groups:
            groups[label]=[]
        for number in split_numbers(text):
            if not number.startswith("."):
                groups[label].append((x,y,number))


    lines=[]
    for label, x in sorted(labels, key=lambda l:l[1]):
        if label not in groups:
            continue
        if type_of_chart(groups[label]):
            numbers=order_left_to_right(groups[label])
            direction="left to right"
        else:
            numbers=order_top_to_bottom(groups[label])
            direction="top to bottom"
        lines.append(f"{label} ({direction}): {', '.join(numbers)}")
    return "\n".join(lines)
