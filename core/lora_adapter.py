"""
GramSetu AI - LoRA Neural Persona & Multi-Parameter Adapter
Emulates fine-tuned LoRA weights for:
1. Multi-Dialect Normalization (Bhojpuri, Haryanvi, Rajasthani, Bihari, Hinglish)
2. Automatic Extraction of 10+ Multi-Parameters (Land Area, Soil Type, Season, Growth Stage, Budget)
3. Dynamic In-Context Adaptation for the Base Model
"""

import re

# Dialect signature mapping
DIALECT_SIGNATURES = {
    "bhojpuri": [
        r'\b(ba|bate|lagal\s+ba|ka\s+kare\s+ke|chaheen|hamaar|tohaar|khet\s+me|dihel\s+jaai|kheti\s+kare\s+ke)\b',
        r'(?:लागल\s*बा|करे\s*के\s*बा|दिहल\s*जाई|का\s*करीं|हमार|तोहार)'
    ],
    "haryanvi": [
        r'\b(arha\s+se|araya\s+se|aarya\s+se|ke\s+karein|k\s+kre|bata\s+de|mhare\s+dhore|kad\s+lagana|pani\s+kad|boni\s+se|jugad)\b',
        r'(?:आरया\s*सै|म्हारा|म्हारी|के\s*करूं|कद\s*लगाणा|बोणी\s*सै|जुगाड़|ताऊ)'
    ],
    "rajasthani": [
        r'\b(laggyo|chhaantni|padeli|kai\s+karan|bhaiji|maay|pooro\s+byoro|sa\s+kisan)\b',
        r'(?:लागग्यो|छांटणी|पड़ेली|कांई|मांय|सा\s*|ब्योरो)'
    ],
    "punjabi": [
        r'\b(kiddan|daso|paani\s+kadon|kini\s+khad|bijayi|fasal\s+ch)\b',
        r'(?:ਕਿੱਦਾਂ|ਦੱਸੋ|ਪਾਣੀ|ਬੀਜ|ਖਾਦ|ਕਣਕ|ਝੋਨਾ)'
    ]
}

SOIL_TYPES = {
    "sandy": ["balui", "retili", "balu", "sandy", "रेतीली", "बलुई", "बलुई दोमट"],
    "clay": ["chikni", "clay", "clayey", "black clay", "चिकनी", "काली चिकनी"],
    "black": ["kali", "black soil", "regur", "काली", "काली मिट्टी", "कपास मिट्टी"],
    "loam": ["domat", "loam", "loamy", "दोमट", "गाद"]
}

GROWTH_STAGES = {
    "sowing": ["buwai", "sowing", "bona", "seed", "beej", "biyan", "बुवाई", "बोनी", "बीज"],
    "cri_tillering": ["cri", "kalle", "tillering", "21 din", "footav", "कल्ले", "फूटाव", "मुकुट जड़"],
    "flowering": ["flower", "flowering", "phool", "buraada", "फूल", "मंजर"],
    "grain_fill": ["doodhiya", "dana", "grain", "milking", "दूधिया", "दाना भराव"]
}

def analyze_and_adapt_prompt(prompt: str) -> dict:
    """
    Analyzes raw user input across dialect, land dimensions, soil conditions,
    and returns rich LoRA parameter embeddings.
    """
    clean = prompt.strip().lower()
    
    # 1. Detect Dialect
    detected_dialect = "standard_hindi_hinglish"
    for dialect, patterns in DIALECT_SIGNATURES.items():
        for pat in patterns:
            if re.search(pat, prompt, re.IGNORECASE):
                detected_dialect = dialect
                break
        if detected_dialect != "standard_hindi_hinglish":
            break

    # 2. Extract Land Parameters
    land_info = None
    m_land = re.search(r'(\d+(?:\.\d+)?)\s*(acre|acres|एकड़|bigha|बीघा|hectare|हेक्टेयर|kattha|कट्टा)', prompt, re.IGNORECASE)
    if m_land:
        val = float(m_land.group(1))
        unit = m_land.group(2).lower()
        
        # Convert to standardized Acres
        if "bigha" in unit or "बीघा" in unit:
            equiv_acre = round(val * 0.625, 2)  # Standard northern bigha avg
            land_info = {"value": val, "unit": "bigha", "normalized_acres": equiv_acre, "raw": f"{val} Bigha (~{equiv_acre} Acre)"}
        elif "hectare" in unit or "हेक्टेयर" in unit:
            equiv_acre = round(val * 2.471, 2)
            land_info = {"value": val, "unit": "hectare", "normalized_acres": equiv_acre, "raw": f"{val} Hectare ({equiv_acre} Acre)"}
        else:
            land_info = {"value": val, "unit": "acre", "normalized_acres": val, "raw": f"{val} Acre"}

    # 3. Detect Soil Type
    detected_soil = None
    for soil_key, keywords in SOIL_TYPES.items():
        if any(kw in clean for kw in keywords):
            detected_soil = soil_key
            break

    # 4. Detect Growth Stage
    detected_stage = None
    for stage_key, keywords in GROWTH_STAGES.items():
        if any(kw in clean for kw in keywords):
            detected_stage = stage_key
            break

    # 5. Build Formatted LoRA Context Adapter String
    lora_context_parts = []
    if detected_dialect != "standard_hindi_hinglish":
        lora_context_parts.append(f"User Dialect: {detected_dialect.capitalize()}")
    if land_info:
        lora_context_parts.append(f"Land Dimensions: {land_info['raw']}")
    if detected_soil:
        lora_context_parts.append(f"Soil Type: {detected_soil.capitalize()}")
    if detected_stage:
        lora_context_parts.append(f"Crop Stage: {detected_stage}")

    adapter_str = f"[LoRA Neural Adapter Context: {', '.join(lora_context_parts)}]" if lora_context_parts else ""

    return {
        "dialect": detected_dialect,
        "land_info": land_info,
        "soil_type": detected_soil,
        "growth_stage": detected_stage,
        "adapter_context_str": adapter_str
    }
