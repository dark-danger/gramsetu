"""
GramSetu AI - Deterministic Memory Engine
Handles explicit memory extraction, persistent storage in SQLite,
conflict resolution, and zero-hallucination deterministic query answers.
"""
import re
from core.database import set_memory, get_memory, get_all_memories, delete_memory

STOP_WORDS = {
    'kya', 'hai', 'h', 'is', 'are', 'was', 'were', 'bhai', 'yaar', 'crop', 'wheat', 'rice',
    'acre', 'bigha', 'namaste', 'hello', 'how', 'what', 'here', 'there', 'this', 'that',
    'none', 'help', 'good', 'fine', 'today', 'weather', 'farmer', 'kisan',
    'likh', 'likho', 'batao', 'bolo', 'karo', 'kar', 'dekh', 'dekho', 'padh', 'padho',
    'sun', 'sunao', 'translate', 'convert', 'write', 'tell', 'show', 'change', 'dasso',
    'punjabi', 'hindi', 'english', 'urdu', 'marathi', 'gujarati', 'bengali', 'tamil'
}

COMMAND_VERBS = {'likh', 'likho', 'batao', 'bolo', 'karo', 'kar', 'write', 'tell', 'show', 'translate', 'convert', 'dasso'}

def extract_and_store_memories(text: str) -> list:
    """
    Extracts explicit user statements deterministically and saves to SQLite.
    Returns list of extracted memory dicts.
    """
    if not text:
        return []

    extracted = []
    clean = text.strip()
    lower = clean.lower()

    # If the sentence is a request/instruction to write or translate, skip name extraction
    tokens = set(re.findall(r'[a-zA-Z]+', lower))
    if tokens & COMMAND_VERBS and re.search(r'\b(likh|likho|write|translate|convert|dasso)\b', lower):
        # Only skip name extraction, continue for land/crop
        pass
    else:
        # ==================== 1. USER NAME EXTRACTION ====================
        name_found = None

        # Pattern A: "yash name h mera" or "yash naam hai mera"
        m_name_a = re.search(r'\b([A-Za-z\u0900-\u097F]{2,20})\s+(?:name|naam)\s+(?:h|hai)\s*(?:mera)?\b', clean, re.IGNORECASE)
        if m_name_a:
            candidate = m_name_a.group(1).capitalize()
            if candidate.lower() not in STOP_WORDS and candidate.lower() not in {'mera', 'meri', 'my', 'apna', 'punjabi', 'hindi'}:
                name_found = candidate

        # Pattern B: "mera naam yash hai" or "my name is yash" or "mera name yash"
        if not name_found:
            m_name_b = re.search(r'\b(?:mera|meri|my)\s+(?:naam|name)\s+(?:is|hai|h)?\s*([A-Za-z\u0900-\u097F]{2,20})\b', clean, re.IGNORECASE)
            if m_name_b:
                candidate = m_name_b.group(1).capitalize()
                if candidate.lower() not in STOP_WORDS and candidate.lower() not in {'kya', 'hai', 'h', 'is', 'punjabi', 'hindi', 'english'}:
                    name_found = candidate

        # Pattern C: "i am yash" or "mein yash hu"
        if not name_found:
            m_name_c = re.search(r'\b(?:i\s*am|mein|main)\s+([A-Za-z\u0900-\u097F]{2,20})(?:\s+hu|\s+hoon)?\b', clean, re.IGNORECASE)
            if m_name_c:
                candidate = m_name_c.group(1).capitalize()
                if candidate.lower() not in STOP_WORDS and candidate.lower() not in {'a', 'the', 'farmer', 'kisan', 'fine', 'good', 'ready', 'here'}:
                    name_found = candidate

        if name_found:
            set_memory(
                key="user_name",
                value=name_found,
                memory_type="identity",
                confidence=1.0,
                importance=5,
                source="explicit_user_statement"
            )
            extracted.append({"key": "user_name", "value": name_found, "type": "identity"})

    # ==================== 2. LAND SIZE EXTRACTION ====================
    # Patterns: "mere paas 4 acre zameen hai", "4 acre zameen hai", "I have 4 acres of land", "4 bigha land"
    m_land = re.search(r'(\d+(?:\.\d+)?)\s*(acre|acres|bigha|kaccha bigha|pucca bigha|hectare|bighas|एकड़|बीघा)(?:\s*(?:zameen|khet|land|ki|mein|me))?', clean, re.IGNORECASE)
    if m_land:
        val = f"{m_land.group(1)} {m_land.group(2).lower()}"
        set_memory(
            key="land_area",
            value=val,
            memory_type="agriculture",
            confidence=1.0,
            importance=4,
            source="explicit_user_statement"
        )
        extracted.append({"key": "land_area", "value": val, "type": "agriculture"})

    # ==================== 3. PROJECT EXTRACTION ====================
    # Patterns: "My project is GenIDE", "Mera project GenIDE hai", "project name is GenIDE"
    m_proj = re.search(r'\b(?:my|mera)\s+project\s+(?:is|name\s+is|hai|h)?\s*([A-Za-z0-9_\-]+)\b', clean, re.IGNORECASE)
    if m_proj:
        proj_name = m_proj.group(1)
        if proj_name.lower() not in {'hai', 'h', 'is', 'kya'}:
            set_memory(
                key="current_project",
                value=proj_name,
                memory_type="project",
                confidence=1.0,
                importance=4,
                source="explicit_user_statement"
            )
            extracted.append({"key": "current_project", "value": proj_name, "type": "project"})

    # ==================== 4. PRIMARY CROP EXTRACTION ====================
    # Patterns: "My crop is wheat", "gehu ki kheti karta hu", "dhan boi hai", "sarson lagayi hai"
    if re.search(r'\b(gehu|wheat|gehun)\b', lower) and re.search(r'\b(kheti|boi|crop|fasal|ugata|farming)\b', lower):
        set_memory("primary_crop", "Wheat (गेहूं)", "agriculture", 1.0, 4)
        extracted.append({"key": "primary_crop", "value": "Wheat (गेहूं)", "type": "agriculture"})
    elif re.search(r'\b(dhan|rice|paddy)\b', lower) and re.search(r'\b(kheti|boi|crop|fasal|ugata|farming)\b', lower):
        set_memory("primary_crop", "Rice/Paddy (धान)", "agriculture", 1.0, 4)
        extracted.append({"key": "primary_crop", "value": "Rice/Paddy (धान)", "type": "agriculture"})
    elif re.search(r'\b(sarson|mustard)\b', lower) and re.search(r'\b(kheti|boi|crop|fasal|ugata|farming)\b', lower):
        set_memory("primary_crop", "Mustard (सरसों)", "agriculture", 1.0, 4)
        extracted.append({"key": "primary_crop", "value": "Mustard (सरसों)", "type": "agriculture"})

    # ==================== 5. PREFERRED LANGUAGE EXTRACTION ====================
    if re.search(r'\b(prefer hinglish|hinglish me bolo|hinglish m baat)\b', lower):
        set_memory("preferred_language", "Hinglish", "preference", 1.0, 4)
        extracted.append({"key": "preferred_language", "value": "Hinglish", "type": "preference"})
    elif re.search(r'\b(prefer english|english m baat kr|speak in english|talk in english)\b', lower):
        set_memory("preferred_language", "English", "preference", 1.0, 4)
        extracted.append({"key": "preferred_language", "value": "English", "type": "preference"})
    elif re.search(r'\b(prefer hindi|hindi me bolo|hindi m baat|हिंदी में बोलो)\b', lower):
        set_memory("preferred_language", "Hindi", "preference", 1.0, 4)
        extracted.append({"key": "preferred_language", "value": "Hindi", "type": "preference"})

    # ==================== 6. LOCATION EXTRACTION ====================
    m_loc = re.search(r'\b(?:from|in|me|rehta hu|se hu|district|state)\s+([A-Z][a-zA-Z]+(?:,\s*[A-Z][a-zA-Z]+)?)\b', clean)
    if m_loc:
        loc = m_loc.group(1)
        if loc.lower() not in STOP_WORDS and loc.lower() not in {'acre', 'bigha', 'wheat', 'rice', 'english', 'hindi'}:
            set_memory("location", loc, "location", 0.9, 3)
            extracted.append({"key": "location", "value": loc, "type": "location"})

    return extracted

def handle_direct_memory_query(text: str, output_lang: str = "english") -> str:
    """
    Zero-Hallucination Deterministic Memory Resolver.
    If query directly asks for a known memory, returns the verified answer directly.
    Returns None if not a direct memory query.
    """
    lower = text.lower().strip()

    # 1. User Name Query ("mera naam kya hai?", "what is my name?", "mera name")
    if re.search(r'\b(mera|meri|my|apna)\s+(?:naam|name)\s*(?:kya|batao|what)?\b', lower) or \
       re.search(r'\bwhat(?:\'s|\s+is)\s+my\s+name\b', lower):
        mem = get_memory("user_name")
        if mem and mem.get("value"):
            name = mem["value"]
            if output_lang == "punjabi":
                return name  # Will be translated/transliterated in Punjabi router
            if "kya" in lower or "naam" in lower or output_lang == "hinglish":
                return f"{name}."
            if output_lang == "hindi":
                return f"आपका नाम {name} है।"
            return f"Your name is {name}."
        else:
            if output_lang in ["hindi", "hinglish"]:
                return "आपने अभी तक मुझे अपना नाम नहीं बताया है। आपका नाम क्या है?"
            return "You haven't told me your name yet. What is your name?"

    # 2. Land Area Query ("meri zameen kitni hai?", "how much land do I have?", "meri zameen")
    if re.search(r'\b(meri|mera|my)\s+(?:zameen|khet|land|area)\s*(?:kitni|kitna|what)?\b', lower) or \
       re.search(r'\bhow\s+much\s+land\b', lower):
        mem = get_memory("land_area")
        if mem and mem.get("value"):
            land = mem["value"]
            if output_lang in ["hindi", "hinglish"]:
                return f"आपके पास {land} जमीन है।"
            return f"You have {land} of land."
        else:
            return "आपने अभी तक मुझे अपनी जमीन का क्षेत्रफल नहीं बताया है।"

    # 3. Project Query ("mera project kya hai?", "what is my project?")
    if re.search(r'\b(mera|my)\s+project\s*(?:kya|what)?\b', lower) or \
       re.search(r'\bwhat(?:\'s|\s+is)\s+my\s+project\b', lower):
        mem = get_memory("current_project")
        if mem and mem.get("value"):
            proj = mem["value"]
            if output_lang in ["hindi", "hinglish"]:
                return f"आपका प्रोजेक्ट {proj} है।"
            return f"Your project is {proj}."
        else:
            return "आपने अभी तक अपने प्रोजेक्ट के बारे में नहीं बताया है।"

    # 4. Primary Crop Query ("meri fasal konsi hai?", "what is my crop?")
    if re.search(r'\b(meri|my)\s+(?:fasal|crop)\s*(?:konsi|kya|what)?\b', lower):
        mem = get_memory("primary_crop")
        if mem and mem.get("value"):
            crop = mem["value"]
            return f"आपकी मुख्य फसल {crop} है।"
        else:
            return "आपने अभी तक अपनी मुख्य फसल के बारे में नहीं बताया है।"

    return None

def get_relevant_memories_for_prompt(prompt: str) -> dict:
    """
    Returns only memories relevant to the query to keep context compact.
    """
    all_mems = get_all_memories()
    if not all_mems:
        return {}

    mem_map = {m["key"]: m["value"] for m in all_mems}
    relevant = {}

    # Always include user_name and preferred_language if present
    if "user_name" in mem_map:
        relevant["user_name"] = mem_map["user_name"]
    if "preferred_language" in mem_map:
        relevant["preferred_language"] = mem_map["preferred_language"]

    lower = prompt.lower()
    # Add agriculture context if agri keywords present
    if re.search(r'\b(land|acre|bigha|khet|zameen|seed|khad|fertilizer|wheat|gehu|dhan|rice|crop|fasal)\b', lower):
        if "land_area" in mem_map:
            relevant["land_area"] = mem_map["land_area"]
        if "primary_crop" in mem_map:
            relevant["primary_crop"] = mem_map["primary_crop"]
        if "location" in mem_map:
            relevant["location"] = mem_map["location"]

    # Add project context if tech/project keywords present
    if re.search(r'\b(project|code|ai|app|system|ide|feature|bug|build)\b', lower):
        if "current_project" in mem_map:
            relevant["current_project"] = mem_map["current_project"]

    return relevant
