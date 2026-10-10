"""
GramSetu AI - Advanced Reasoning & Multilingual Style Engine
Masters fluent Hinglish, English, and Hindi with structured step-by-step reasoning.
"""

def build_messages_for_ollama(routing_info: dict, recent_history: list) -> list:
    out_lang = routing_info.get("output_language", "english")
    tone_style = routing_info.get("style_prompt", "")
    memories = routing_info.get("relevant_memories", {})
    tool_results = routing_info.get("tool_results", [])
    intent = routing_info.get("intent", "general_discussion")

    # ==================== 1. LANGUAGE & STYLE DIRECTIVE ====================
    if out_lang == "hinglish":
        lang_rule = (
            "LANGUAGE DIRECTIVE: Reply in clear, natural conversational Hinglish (Roman Hindi).\n"
            "• Keep sentences short, crisp, and grammatically correct.\n"
            "• Keep technical and formal terms in standard English (e.g. 'crop', 'fertilizer', 'loan', 'sensor', 'database').\n"
            "• Do NOT use repetitive filler phrases or awkward broken words."
        )
    elif out_lang == "hindi":
        lang_rule = (
            "LANGUAGE DIRECTIVE: Output in pure, natural, fluent Hindi (हिंदी - देवनागरी लिपि).\n"
            "• स्पष्ट, शुद्ध और सरल हिंदी में सीधा उत्तर दें।\n"
            "• मुख्य जानकारी को बुलेट पॉइंट्स (•) में संक्षिप्त रूप से प्रस्तुत करें।"
        )
    elif out_lang == "punjabi":
        lang_rule = (
            "LANGUAGE DIRECTIVE: Output strictly in Punjabi (ਪੰਜਾਬੀ / Gurmukhi script).\n"
            "• ਪੰਜਾਬੀ ਭਾਸ਼ਾ ਵਿੱਚ ਸਪੱਸ਼ਟ ਅਤੇ ਸਰਲ ਜਵਾਬ ਦਿਓ।"
        )
    else:
        lang_rule = (
            "LANGUAGE DIRECTIVE: Output in clear, polished, concise English.\n"
            "• Provide high-clarity, logical explanations with bullet points and code blocks."
        )

    # ==================== 2. STRICT TO-THE-POINT REASONING DIRECTIVE ====================
    reasoning_rule = (
        "CRITICAL RULES (TO-THE-POINT REASONING):\n"
        "1. DIRECT ANSWER: Give the direct, factual answer immediately in the first sentence. No intro filler, no pleasantries.\n"
        "2. CONCISE & STRUCTURED: Use 2 to 4 crisp, actionable bullet points or steps. Maximum 80-120 words total.\n"
        "3. ZERO REPETITION: NEVER repeat the same sentence, phrase, point, or concept. Each line must give new, useful facts.\n"
        "4. NO HALLUCINATIONS: State only verified facts, exact quantities, or code. Do not invent fictional details.\n"
        "5. STOP IMMEDIATELY after giving the points. No conclusion summaries or filler."
    )

    # ==================== 3. INTENT-SPECIFIC TASKS & DOMAIN GROUNDING ====================
    if intent == "simple_transformation":
        intent_rule = "TASK: Output ONLY the requested transformed text/translation. Do not add any explanations."
    elif intent == "greeting":
        intent_rule = "TASK: Give a warm, brief (1-2 sentences max), natural greeting."
    elif intent == "coding_technical":
        intent_rule = "TASK: [Domain: Software] Provide clean, syntax-highlighted code with 2-3 concise bullet points explaining logic."
    elif intent == "tech_hardware":
        intent_rule = "TASK: [Domain: Electronics & IoT] Provide exact pin wiring and crisp microcontroller code."
    elif intent == "agriculture":
        intent_rule = "TASK: [Domain: Agriculture/Farming] Provide practical farming steps, seed rates, fertilizer dosages, or irrigation timing. ('Pani' = crop irrigation)."
    elif intent == "medical" or intent == "first_aid":
        intent_rule = "TASK: [Domain: Health & First Aid] Provide immediate, safe, step-by-step first aid or dosage guidance, with caution to consult doctor."
    elif intent == "government_scheme":
        intent_rule = "TASK: [Domain: Government Welfare] State eligibility, benefits (subsidy/interest rate), and application process directly."
    elif intent == "formal_professional":
        intent_rule = "TASK: Draft a high-quality, professional, well-structured document or proposal."
    else:
        intent_rule = "TASK: Provide a direct, helpful, and accurate response to the specific question asked."

    # ==================== 4. GROUND TRUTH & MEMORY CONTEXT ====================
    mem_parts = [f"{k}: {v}" for k, v in memories.items()]
    mem_str = f"\n[Confirmed User Facts: {', '.join(mem_parts)}]" if mem_parts else ""

    tool_str = ""
    if tool_results:
        tool_blocks = [f"--- {t['tool_name']} ---\n{t['result']}" for t in tool_results]
        tool_str = "\n\n[Verified Ground Truth Data]:\n" + "\n\n".join(tool_blocks)

    system_prompt = (
        f"You are GramSetu AI, an expert, razor-sharp, to-the-point AI assistant.\n"
        f"{lang_rule}\n"
        f"{reasoning_rule}\n"
        f"{tone_style}\n"
        f"{intent_rule}"
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
        "content": routing_info.get("resolved_prompt", routing_info.get("original_prompt"))
    })

    return messages
