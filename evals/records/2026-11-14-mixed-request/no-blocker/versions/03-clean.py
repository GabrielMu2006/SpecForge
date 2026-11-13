def clean_names(lines):
    """Strip surrounding whitespace and drop blanks, preserving order and repeats."""
    result = []
    for line in lines:
        name = line.strip()
        if name:
            result.append(name)
    return result
