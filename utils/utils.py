from datetime import datetime

def parse_date(input_string):
    # Danh sách các định dạng có thể
    formats = [
        "%Y-%m-%d",    # YYYY-MM-DD
        "%d/%m/%Y",    # DD/MM/YYYY
        "%m-%d-%Y",    # MM-DD-YYYY
        "%Y.%m.%d",    # YYYY.MM.DD
        "%d %B %Y",    # DD Month YYYY (ví dụ: 20 October 2023)
        "%Y/%m/%d"
    ]
    
    for fmt in formats:
        try:
            # Cố gắng phân tích theo định dạng hiện tại
            date_object = datetime.strptime(input_string, fmt)
            # Trả về định dạng YYYY-MM-DD
            return date_object.strftime("%Y-%m-%d")
        except ValueError:
            continue  # Nếu không khớp, thử định dạng tiếp theo
    
    return None

def day_compare(day1: str, day2: str):
    """
        Return True if day1 >= day2
    """
    parsed_day1 = parse_date(day1)
    parsed_day2 = parse_date(day2)

    return parsed_day1 >= parsed_day2