import re
import unicodedata

def slugify(text: str) -> str:
    """
    Convert a string/ Blog title to a slug.
    """
    # Convert text to lowercase
    text = text.lower()
    
    # Normalize unicode characters (e.g., é → e)
    text = unicodedata.normalize("NFKD", text)
    
    # Remove special characters, keeping only letters, numbers, and spaces
    text = re.sub(r"[^\w\s-]", "", text)
    
    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)
    
    # Remove leading/trailing hyphens
    text = text.strip("-")
    
    return text
