"""
GramSetu AI - Language Detection & Separation Engine
Separates INPUT LANGUAGE from REQUESTED OUTPUT LANGUAGE.
"""
import re

HINDI_CHAR_REGEX = re.compile(r'[\u0900-\u097F]')
PUNJABI_CHAR_REGEX = re.compile(r'[\u0A00-\u0A7F]')

HINGLISH_KEYWORDS = {
    'mera', 'meri', 'mere', 'naam', 'kya', 'hai', 'hain', 'h', 'kaise', 'kese', 'karo', 'kar', 'karna',
    'bhai', 'yaar', 'zameen', 'khet', 'fasal', 'gehu', 'dhan', 'sarson', 'kitna', 'kitni',
    'chahiye', 'bol', 'bolo', 'batao', 'bataye', 'bata', 'baat', 'samjhao', 'mujhe', 'mujha', 'merko',
    'humko', 'apna', 'isme', 'isko', 'usme', 'usko', 'kisi', 'kuch', 'hoga', 'raha', 'rahi', 'wale',
    'wala', 'wali', 'namaste', 'namaskar', 'pranam', 'hal', 'chal', 'theek', 'thik', 'accha', 'achha',
    'kr', 'kro', 'ho', 'bhi', 'toh', 'to', 'se', 'ko', 'par', 'pe', 'me', 'mai', 'mein', 'aur', 'ya',
    'kare', 'karen', 'dena', 'lene', 'pani', 'paani', 'khad', 'keeda', 'bukhar', 'dawa', 'dawai',
    'naki', 'na', 'ulta', 'sidha', 'jawab', 'jwab', 'sawal', 'bhaiya', 'chale', 'chalo', 'suno'
}

PUNJABI_LATIN_KEYWORDS = {
    'tussi', 'tusi', 'saada', 'sada', 'kiven', 'kidda', 'kiddan', 'chahida', 'dasso', 'naam',
    'mera', 'vich', 'pind', 'kheti'
}

def detect_input_language(text: str) -> str:
    if not text:
        return "english"
    
    clean = text.strip()
    
    # 1. Direct Script Check
    if PUNJABI_CHAR_REGEX.search(clean):
        return "punjabi"
    if HINDI_CHAR_REGEX.search(clean):
        return "hindi"

    # 2. Token Keyword Matching
    tokens = re.findall(r'[a-zA-Z]+', clean.lower())
    if not tokens:
        return "english"
    
    hinglish_count = sum(1 for t in tokens if t in HINGLISH_KEYWORDS)
    punjabi_count = sum(1 for t in tokens if t in PUNJABI_LATIN_KEYWORDS)

    if punjabi_count >= 2:
        return "punjabi_latin"
    if hinglish_count >= 1 or (len(tokens) <= 3 and hinglish_count > 0):
        return "hinglish"

    return "english"

def detect_requested_output_language(text: str, default_lang: str = None) -> str:
    lower = text.lower()

    # Punjabi request detection
    if re.search(r'\b(punjabi|panjabi|ਪੰਜਾਬੀ)\b', lower):
        if re.search(r'\b(m|me|mai|mein|vich|in|to|likh|likho|batao|translate|convert)\b', lower):
            return "punjabi"

    # Hindi request detection
    if re.search(r'\b(hindi|हिंदी)\b', lower):
        if re.search(r'\b(m|me|mai|mein|in|to|likh|likho|batao|bol|bolo|baat|translate|convert)\b', lower):
            return "hindi"

    # English request detection
    if re.search(r'\b(english|angrezi)\b', lower):
        if re.search(r'\b(m|me|mai|mein|in|to|write|speak|talk|reply|convert|translate)\b', lower):
            return "english"

    # Hinglish request detection
    if re.search(r'\b(hinglish)\b', lower):
        return "hinglish"

    return default_lang or detect_input_language(text)
