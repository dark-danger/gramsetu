"""
GramSetu AI - Advanced Reasoning, Multi-Dialect & Adaptive Conciseness Engine
Default Mode: Strict To-The-Point, Crisp & Direct (40-80 words max)
Explanation Mode: Triggered ONLY when explicitly asked ("explain", "detail", "vistar", "samjhao", "kyu")
"""

import re

def build_messages_for_ollama(routing_info: dict, recent_history: list) -> list:
    out_lang = routing_info.get("output_language", "english")
    tone_style = routing_info.get("style_prompt", "")
    memories = routing_info.get("relevant_memories", {})
    tool_results = routing_info.get("tool_results", [])
    intent = routing_info.get("intent", "general_discussion")
    raw_prompt = routing_info.get("original_prompt", "")
    clean_lower = raw_prompt.lower()

    # Detect if user explicitly requested deep explanation
    wants_explanation = bool(re.search(
        r'\b(explain|detail|vistar|samjhao|samjha|pura batao|step by step detail|describe|elaborate|deep|kyu|kyon|why|reason|bataiye detail me)\b',
        clean_lower
    ))

    # ==================== 1. LANGUAGE & DIALECT DIRECTIVE ====================
    if out_lang == "hinglish":
        lang_rule = (
            "LANGUAGE & DIALECT DIRECTIVE: Natural, crisp Conversational Hinglish (Roman Hindi).\n"
            "• Tone: Direct, practical, relatable (like a wise agricultural/technical expert).\n"
            "• Keep technical/drug terms in clear English (e.g., 'Chlorpyrifos', 'DAP', 'ESP32', 'Reaper')."
        )
    elif out_lang == "hindi":
        lang_rule = (
            "LANGUAGE & DIALECT DIRECTIVE: स्पष्ट, सरल एवं प्रामाणिक देवनागरी हिंदी।\n"
            "• भाषा अत्यंत सीधी, स्पष्ट और समझने योग्य होनी चाहिए।"
        )
    elif out_lang == "punjabi":
        lang_rule = (
            "LANGUAGE DIRECTIVE: Output strictly in natural Punjabi (ਪੰਜਾਬੀ / Gurmukhi script).\n"
            "• ਸੰਖੇਪ ਅਤੇ ਸਪੱਸ਼ਟ ਜਵਾਬ ਦਿਓ।"
        )
    else:
        lang_rule = (
            "LANGUAGE DIRECTIVE: Polished, concise, direct English."
        )

    # ==================== 2. STRICT CONCISENESS VS EXPLANATION RULE ====================
    if wants_explanation:
        length_rule = (
            "LENGTH & REASONING MODE: DETAILED EXPLANATION REQUESTED.\n"
            "• Provide a comprehensive, in-depth explanation with step-by-step logic, background cause, and clear recommendations.\n"
            "• Use structured sections with emojis (🌾, ⚙️, 🧪, 💡)."
        )
    else:
        length_rule = (
            "LENGTH & REASONING MODE: STRICT TO-THE-POINT (DEFAULT).\n"
            "1. ULTRA-CRISP & DIRECT: Give the direct, exact answer/dosage/equipment in the very first sentence.\n"
            "2. MAXIMUM 2-3 BULLET POINTS: Total response length should be under 50 to 80 words.\n"
            "3. NO ESSAYS OR FLUFF: Do NOT give long textbook introductions, background lectures, or unnecessary filler.\n"
            "4. STOP IMMEDIATELY once the practical action is stated."
        )

    # ==================== 3. CONVERSATIONAL CONTINUITY ====================
    continuity_rule = (
        "CONVERSATIONAL CONTINUITY:\n"
        "• This is an active ongoing dialogue. The user's message is a direct follow-up.\n"
        "• If previous turns were discussing tractor harvesting and user says 'sweet corn katni h', directly name the specific tractor implement for sweet corn (e.g. Corn Forage Harvester / Rotary Cutter) without resetting the topic."
    )

    # ==================== 4. DOMAIN GROUNDING ====================
    if intent == "simple_transformation":
        intent_rule = "TASK: Output ONLY the requested transformed text/translation directly."
    elif intent == "greeting":
        intent_rule = "TASK: Give a warm, ultra-brief (1 sentence) greeting."
    elif intent == "coding_technical":
        intent_rule = "TASK: [Software/Code] Provide clean code snippet with 1-2 brief bullet points."
    elif intent == "tech_hardware":
        intent_rule = "TASK: [IoT/Hardware] Provide exact pinout and concise connection instruction."
    elif intent == "agriculture":
        intent_rule = "TASK: [Agriculture] State the exact implement name, seed rate, or chemical dosage directly."
    elif intent == "medical" or intent == "first_aid":
        intent_rule = "TASK: [Health/First Aid] Give immediate, safe emergency action and standard dosage with doctor warning."
    elif intent == "government_scheme":
        intent_rule = "TASK: [Welfare Schemes] State benefit amount, eligibility, and portal in 2-3 crisp points."
    else:
        intent_rule = "TASK: Provide a direct, concise, and accurate response."

    # ==================== 5. CONTEXT & KNOWLEDGE ====================
    mem_parts = [f"{k}: {v}" for k, v in memories.items()]
    mem_str = f"\n[User Profile: {', '.join(mem_parts)}]" if mem_parts else ""

    lora_info = routing_info.get("lora_adapter", {})
    lora_str = f"\n{lora_info['adapter_context_str']}" if lora_info.get("adapter_context_str") else ""

    tool_str = ""
    if tool_results:
        tool_blocks = [f"--- {t['tool_name']} ---\n{t['result']}" for t in tool_results]
        tool_str = "\n\n[Verified Ground Truth Data]:\n" + "\n\n".join(tool_blocks)

    system_prompt = (
        f"You are GramSetu AI, an expert, razor-sharp, to-the-point assistant.\n\n"
        f"{length_rule}\n\n"
        f"{lang_rule}\n\n"
        f"{continuity_rule}\n\n"
        f"{intent_rule}"
        f"{lora_str}"
        f"{mem_str}"
        f"{tool_str}"
    )

    messages = [{"role": "system", "content": system_prompt}]

    # Append recent conversation turns
    for turn in recent_history[-6:]:
        messages.append({
            "role": turn.get("role", "user"),
            "content": turn.get("content", "")
        })

    # Append current prompt
    messages.append({
        "role": "user",
        "content": routing_info.get("resolved_prompt", raw_prompt)
    })

    return messages
