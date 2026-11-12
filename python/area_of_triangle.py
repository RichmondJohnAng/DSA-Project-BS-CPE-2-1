def calculate_area_of_triangle(base: float, height: float) -> float:
    return 0.5 * float(base) * float(height)

def area_of_triangle(base: float, height: float) -> float:
    return calculate_area_of_triangle(base, height)

def process_triangle_area(base_input: str, height_input: str):
    clean_b = str(base_input or "").strip()
    clean_h = str(height_input or "").strip()
    
    if not clean_b or not clean_h:
        return None, "Please enter both base and height values."
    
    try:
        b = float(clean_b)
        h = float(clean_h)
        if b <= 0 or h <= 0:
            return None, "Invalid input: Base and height must be positive numbers greater than 0."
        
        area = calculate_area_of_triangle(b, h)
        result = round(area, 4) if not area.is_integer() else int(area)
        return result, None
    except (ValueError, TypeError):
        return None, "Invalid input: Letters and special characters are not accepted. Please enter valid numbers."
