def clean_names(lines):
    """Strip surrounding whitespace and omit blank names, preserving order."""
    result = []
    for line in lines:
        name = line.strip()
        if name:
            result.append(name)
    return result
