import math

PI_CONSTANT = 3.141592653589793

def calculate_area_of_circle(radius: float) -> float:
    return PI_CONSTANT * (float(radius) ** 2)

def area_of_circle(radius: float) -> float:
    return calculate_area_of_circle(radius)

def process_circle_area(radius_input: str):
    if radius_input is None:
        return None, "Please enter a radius value."
    
    clean_val = str(radius_input).strip()
    if not clean_val:
        return None, "Please enter a radius value."
    
    try:
        r = float(clean_val)
        if r <= 0:
            return None, "Invalid input: Radius must be a positive number greater than 0."
        
        area = calculate_area_of_circle(r)
        result = round(area, 4) if not area.is_integer() else int(area)
        return result, None
    except (ValueError, TypeError):
        return None, "Invalid input: Letters and special characters are not accepted. Please enter a valid number."
