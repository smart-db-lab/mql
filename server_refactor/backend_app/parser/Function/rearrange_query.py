import re

def clean_text(input_text):
    # Replace non-breaking spaces and other non-printable characters with whitespace
    cleaned_text = re.sub(r'[\xa0\u200b\u2028\u2029]', ' ', input_text)
    cleaned_text = re.sub(r'\/n', ' ', cleaned_text)
    cleaned_text = re.sub(r'\/r', ' ', cleaned_text)
    cleaned_text = re.sub(r'\/r\/n', ' ', cleaned_text)
    cleaned_text = re.sub('WHERE ', ' ', cleaned_text)
    cleaned_text = re.sub('BASED ON', ' ', cleaned_text)
    return cleaned_text


def find_earliest_position(query, operation_types, start_pos):
    min_pos = len(query)
    for word in operation_types:
        pos = query.find(word, start_pos)
        if pos != -1 and pos < min_pos:
            min_pos = pos
    return min_pos

def rearrange_query(query):
    clean_text(query)
    print(query)

    # Split the query into parts based on "WHERE" and "BASED ON"
    # parts = query.split(" WHERE ")
    # generate_construct_part = parts[0].strip()
    # construct_basedon_part = parts[1].strip().split(" BASED ON ")

    # construct_part = construct_basedon_part[0].strip()
    # inspect_part = construct_basedon_part[1].strip()
    inspect_part=''
    construct_part=''
    generate_part = ''
    inspect_pos = query.find("INSPECT")
    construct_pos = query.find("CONSTRUCT")
    generate_pos = query.find("GENERATE")
    if inspect_pos == -1 and construct_pos == -1 and generate_pos == -1:
        return query
    # Extract the INSPECT part
    inspect_start = query.find("INSPECT")
    if inspect_start != -1:
        inspect_end = find_earliest_position(query,  ["CONSTRUCT", "GENERATE"], inspect_start + len("INSPECT"))
        inspect_part = query[inspect_start:inspect_end].strip()

    # Extract the CONSTRUCT part
    construct_start = query.find("CONSTRUCT")
    if construct_start != -1:
        construct_end = find_earliest_position(query,  ["INSPECT", "GENERATE"], construct_start + len("CONSTRUCT"))
        construct_part = query[construct_start:construct_end].strip()

    # Extract the GENERATE part
    generate_start = query.find("GENERATE")
    if generate_start != -1:
        generate_end = find_earliest_position(query,  ["CONSTRUCT", "INSPECT"], generate_start + len("GENERATE"))
        generate_part = query[generate_start:generate_end].strip()

    # Create the final array in the required order
    result = [inspect_part, construct_part, generate_part]
    print(result)
    return result
