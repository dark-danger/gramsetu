"""
GramSetu AI - Advanced Conversational Continuity & Context Engine
Handles:
1. Elliptical follow-ups (e.g. "tractor ke piche crops katne ke liye kya lagaye" -> "sweet corn katni h")
2. Anaphoric pronoun resolution (isme, isko, usme, yeh, woh, that, this)
3. Topic & Subject inheritance across multi-turn chats
4. Context-aware prompt rewriting for RAG & LLM precision
"""

import re
from core.database import get_recent_messages, get_memory

PRONOUN_PATTERNS = [
    r'\bisme\b', r'\bisko\b', r'\busme\b', r'\busko\b', r'\biska\b', r'\biski\b',
    r'\byeh\b', r'\bye\b', r'\bwoh\b', r'\bwo\b', r'\bthis\b', r'\bthat\b',
    r'\bprevious\s+one\b', r'\bsame\s+wala\b', r'\bispar\b', r'\bispe\b',
    r'\bdono\s+me\s+se\b', r'\bwhich\s+one\b', r'\buska\s+naam\b'
]

ELLIPTICAL_PREFIXES = [
    r'^(?:aur|and|or|to|fir|phir|lekin|par|but|agar|if|bhi|fir\s+bhi|toh)\b',
    r'^(?:kitna|kitni|kab|kaha|kahan|how\s+much|when|where|why|price|cost|daam|rate|kharcha)\b'
]

def extract_topic_from_text(text: str) -> dict:
    """Extracts core subject and operational action from previous conversation turns."""
    lower = text.lower()
    
    action = None
    subject = None
    domain = None

    # Machinery / Implements
    if re.search(r'\b(tractor|auzar|yantra|cutter|harvester|rotavator|plow|seeder|sprayer|equipment|machinery|katna|harvest|harvesting|picha|piche)\b', lower):
        action = "machinery_implement_harvesting"
        domain = "agriculture_machinery"
        m_mach = re.search(r'\b(tractor|rotavator|harvester|cutter|seeder|sprayer|mower|plough|hal)\b', lower)
        subject = m_mach.group(1) if m_mach else "tractor harvesting machinery"

    # Disease / Pest / Spray
    elif re.search(r'\b(bimari|rog|keeda|sundi|fungus|rust|rot|spray|dawai|chhidkaw|treatment|cure|pest|yellow)\b', lower):
        action = "disease_pest_cure"
        domain = "agriculture_disease"
        m_dis = re.search(r'\b(yellow rust|peela ratua|rust|fungus|termite|dimak|aphid|mahu|chepa|sundi|keeda)\b', lower)
        subject = m_dis.group(1) if m_dis else "crop pest/disease treatment"

    # Fertilizer / Soil
    elif re.search(r'\b(khad|fertilizer|dap|urea|potash|zinc|npk|mitti|soil|sinchai|irrigation|pani)\b', lower):
        action = "fertilizer_irrigation"
        domain = "agriculture_fertilizer"
        m_fert = re.search(r'\b(dap|urea|potash|zinc|npk|irrigation|sinchai)\b', lower)
        subject = m_fert.group(1) if m_fert else "fertilizer and irrigation"

    # Hardware / IoT
    elif re.search(r'\b(arduino|esp32|sensor|relay|wiring|code|pin|iot)\b', lower):
        action = "hardware_iot_interfacing"
        domain = "tech_hardware"
        m_hw = re.search(r'\b(arduino|esp32|flame|dht11|dht22|relay|oled)\b', lower)
        subject = m_hw.group(1) if m_hw else "microcontroller IoT interface"

    # Schemes
    elif re.search(r'\b(pm kisan|kcc|ayushman|yojana|subsidy|portal|document)\b', lower):
        action = "scheme_benefits"
        domain = "government_scheme"
        m_sch = re.search(r'\b(pm kisan|kcc|ayushman|kusum|samman nidhi)\b', lower)
        subject = m_sch.group(1) if m_sch else "government welfare scheme"

    return {
        "action": action,
        "subject": subject,
        "domain": domain,
        "raw_text": text
    }

def resolve_context_references(current_prompt: str, session_id: str = "default", recent_messages: list = None) -> dict:
    """
    Deep Context Resolution Engine:
    Inspects previous user & assistant conversation turns to resolve:
    1. Pronouns (isme, woh, that, this)
    2. Elliptical follow-ups ("sweet corn katni h" following "tractor k picha kya use kru")
    3. Topic continuation
    Returns rich dictionary with resolved_prompt, previous_topic, inherited_intent.
    """
    clean = current_prompt.strip()
    lower = clean.lower()

    # Get conversation history
    if recent_messages is None:
        recent = get_recent_messages(session_id, limit=6)
    else:
        recent = list(recent_messages)

    # Filter out current prompt if it is already at the tail of recent
    if recent and recent[-1].get("content", "").strip().lower() == lower:
        recent = recent[:-1]

    if not recent:
        return {
            "resolved_prompt": clean,
            "has_context_link": False,
            "previous_topic": None,
            "inherited_intent": None
        }

    # Analyze last user message and assistant message
    last_user_msg = None
    last_asst_msg = None
    for msg in reversed(recent):
        if msg.get("role") == "user" and not last_user_msg:
            last_user_msg = msg.get("content", "")
        elif msg.get("role") == "assistant" and not last_asst_msg:
            last_asst_msg = msg.get("content", "")
        if last_user_msg and last_asst_msg:
            break

    # Determine if current prompt is an elliptical follow-up or pronoun reference
    word_count = len(clean.split())
    has_pronoun = any(re.search(pat, lower) for pat in PRONOUN_PATTERNS)
    is_elliptical_prefix = any(re.search(pat, lower) for pat in ELLIPTICAL_PREFIXES)
    
    # Check if prompt is a short follow-up (e.g. <= 7 words like "sweet corn katni h", "makka ke liye", "aur spray kab kare")
    is_short_followup = word_count <= 7 and not re.search(r'\b(who are you|hello|hi|namaste|mera naam|my name)\b', lower)

    # Extract topic from previous turns
    prev_topic = None
    if last_user_msg:
        prev_topic = extract_topic_from_text(last_user_msg)
    if (not prev_topic or not prev_topic["action"]) and last_asst_msg:
        prev_topic = extract_topic_from_text(last_asst_msg)

    # Context Resolution Logic
    resolved = clean
    inherited_intent = None

    if (has_pronoun or is_elliptical_prefix or is_short_followup) and prev_topic and prev_topic["action"]:
        
        # Scenario A: Machinery Follow-up (e.g. Prev = Tractor crops cutting -> Curr = "sweet corn katni h")
        if prev_topic["action"] == "machinery_implement_harvesting":
            inherited_intent = "agriculture"
            resolved = f"{clean} (Follow-up Context: Tractor attachments, implements, cutter, or harvester machinery for cutting/harvesting: {prev_topic['subject']})"

        # Scenario B: Disease / Pest Follow-up (e.g. Prev = Yellow rust -> Curr = "dawai ka dose kitna h" or "sweet corn me")
        elif prev_topic["action"] == "disease_pest_cure":
            inherited_intent = "agriculture"
            resolved = f"{clean} (Follow-up Context: Chemical/organic spray dosage and pest/disease control for: {prev_topic['subject']})"

        # Scenario C: Fertilizer / Irrigation Follow-up
        elif prev_topic["action"] == "fertilizer_irrigation":
            inherited_intent = "agriculture"
            resolved = f"{clean} (Follow-up Context: Fertilizer schedule, NPK/DAP dosage, and irrigation timing for: {prev_topic['subject']})"

        # Scenario D: Hardware / IoT Follow-up
        elif prev_topic["action"] == "hardware_iot_interfacing":
            inherited_intent = "tech_hardware"
            resolved = f"{clean} (Follow-up Context: Arduino/ESP32 pin connections and microcontroller code for: {prev_topic['subject']})"

        # Scenario E: Schemes Follow-up
        elif prev_topic["action"] == "scheme_benefits":
            inherited_intent = "government_scheme"
            resolved = f"{clean} (Follow-up Context: Eligibility, subsidy, application process for: {prev_topic['subject']})"

        return {
            "resolved_prompt": resolved,
            "has_context_link": True,
            "previous_topic": prev_topic,
            "inherited_intent": inherited_intent
        }

    return {
        "resolved_prompt": clean,
        "has_context_link": False,
        "previous_topic": prev_topic,
        "inherited_intent": None
    }
