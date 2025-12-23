"""
Utility functions for input validation and sanitization
"""

import re
from typing import Optional, Dict, Any

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number (basic validation)"""
    # Remove spaces, dashes, and plus signs
    cleaned = re.sub(r'[\s\-+]', '', phone)
    # Check if it's all digits and reasonable length
    return cleaned.isdigit() and 10 <= len(cleaned) <= 15

def sanitize_string(value: str, max_length: int = 255) -> str:
    """Sanitize string input"""
    if not value:
        return ""
    # Remove null bytes and trim
    cleaned = value.replace('\x00', '').strip()
    # Limit length
    return cleaned[:max_length]

def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))

def validate_telegram_id(telegram_id: str) -> bool:
    """Validate Telegram ID format"""
    return telegram_id.isdigit() and len(telegram_id) >= 5

def validate_product_data(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate product creation/update data"""
    required_fields = ['product_name', 'category', 'product_link', 'product_price']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Field '{field}' is required"
    
    # Validate price
    try:
        price = float(data['product_price'])
        if price < 0:
            return False, "Price must be positive"
    except (ValueError, TypeError):
        return False, "Price must be a valid number"
    
    # Validate URL
    if not validate_url(data['product_link']):
        return False, "Product link must be a valid URL"
    
    return True, None

def validate_user_data(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate user registration/update data"""
    if 'email' in data and data['email']:
        if not validate_email(data['email']):
            return False, "Invalid email format"
    
    if 'whatsapp' in data and data['whatsapp']:
        if not validate_phone(data['whatsapp']):
            return False, "Invalid phone number format"
    
    if 'telegram_id' in data and data['telegram_id']:
        if not validate_telegram_id(str(data['telegram_id'])):
            return False, "Invalid Telegram ID format"
    
    return True, None

