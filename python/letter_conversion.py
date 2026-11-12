def to_uppercase(text: str) -> str:
    return text.upper() if text else ""

def process_letter_conversion(input_string: str):
    if not input_string or not input_string.strip():
        return None, "Please enter some text."
    
    if not all(c.isalpha() or c.isspace() for c in input_string):
        return None, "Invalid input: Numbers and special characters are not accepted. Only letters (A-Z, a-z) are allowed."
    
    return input_string.upper(), None
