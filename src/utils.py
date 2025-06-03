def get_last_text_line(filepath):
    """
    read the last non-empty line from a text file, ignoring comments and timestamps
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    # Reverse search for the last non-empty line that is not a comment
    for line in reversed(lines):
        if ']' in line:
            # Remove timestamp part
            text = line.split(']', 1)[-1].strip()
            if text:
                return text
        elif line and not line.startswith('//'):
            return line
    return ""