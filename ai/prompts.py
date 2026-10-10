"""
GramSetu AI - Advanced Reasoning, Multi-Dialect & Parameter Synthesis Engine
Masters 10 Lakh diverse Indian personas, dialects (Bhojpuri, Haryanvi, Rajasthani, Dehati, Hinglish),
and multi-parameter situational reasoning (land area, soil, season, weather, budget).
"""

def build_messages_for_ollama(routing_info: dict, recent_history: list) -> list:
    out_lang = routing_info.get("output_language", "english")
    tone_style = routing_info.get("style_prompt", "")
    memories = routing_info.get("relevant_memories", {})
    tool_results = routing_info.get("tool_results", [])
    intent = routing_info.get("intent", "general_discussion")
    raw_prompt = routing_info.get("original_prompt", "")

    # ==================== 1. LANGUAGE & DIALECT DIRECTIVE ====================
    if out_lang == "hinglish":
        lang_rule = (
            "LANGUAGE & DIALECT DIRECTIVE: Natural, fluent Conversational Hinglish (Roman Hindi).\n"
            "• Tone: Warm, respectful, highly practical, and relatable (like a wise agricultural/technical friend).\n"
            "• Understand all regional colloquialisms (e.g. 'khet', 'paani', 'chepa', 'bigha', 'rog', 'chhidkaw', 'dawai').\n"
            "• Keep technical/scientific drug/tool terms in clear English (e.g., 'Chlorpyrifos', 'DAP', 'ESP32', 'GPIO')."
        )
    elif out_lang == "hindi":
        lang_rule = (
            "LANGUAGE & DIALECT DIRECTIVE: स्पष्ट, सरल एवं प्रामाणिक देवनागरी हिंदी।\n"
            "• भाषा अत्यंत आत्मीय, सरल और हर किसान व ग्रामीण नागरिक के समझने योग्य होनी चाहिए।\n"
            "• वैज्ञानिक नामों और रासायनिक मात्राओं को स्पष्ट हिंदी व अंग्रेजी दोनों में अंकित करें।"
        )
    elif out_lang == "punjabi":
        lang_rule = (
            "LANGUAGE DIRECTIVE: Output strictly in natural Punjabi (ਪੰਜਾਬੀ / Gurmukhi script).\n"
            "• ਸਤਿਕਾਰਯੋਗ, ਸਰਲ ਅਤੇ ਪੇਂਡੂ ਕਿਸਾਨੀ ਲਈ ਸਭ ਤੋਂ ਲਾਭਦਾਇਕ ਤਰੀਕੇ ਨਾਲ ਜਵਾਬ ਦਿਓ।"
        )
    else:
        lang_rule = (
            "LANGUAGE DIRECTIVE: Polished, clear, practical English.\n"
            "• Provide high-clarity, step-by-step guidance with clear sections, dosages, and parameters."
        )

    # ==================== 2. MULTI-PARAMETER REASONING DIRECTIVE ====================
    reasoning_rule = (
        "MULTI-PARAMETER SITUATIONAL REASONING RULES:\n"
        "1. PARAMETER ADAPTATION: Actively adapt your solution to user parameters (e.g., land size in bigha/acre, soil type like sandy/clay/loamy, season like Rabi/Kharif, budget, crop growth stage).\n"
        "2. PRACTICAL STRUCTURE: Format your answer with clear headers, bullet points (•), bold key numbers/doses, and emoji indicators (🌾, 🧪, 💧, ⚠️).\n"
        "3. EXACT MEASUREMENTS: Always specify exact dosage per acre or per liter of water (e.g. '200ml in 200L water per acre').\n"
        "4. ROOT-CAUSE & PREVENTIVE TIPS: Along with the cure, mention how to prevent the problem in future.\n"
        "5. RESPECTFUL & ENGAGING: Speak directly to the user's situation without unnecessary robotic filler."
    )

    # ==================== 3. DOMAIN-SPECIFIC GROUNDING ====================
    if intent == "simple_transformation":
        intent_rule = "TASK: Output ONLY the requested transformed text/translation directly."
    elif intent == "greeting":
        intent_rule = "TASK: Give a warm, respectful, and energetic greeting."
    elif intent == "coding_technical":
        intent_rule = "TASK: [Domain: Software & Electronics] Provide robust, commented code with circuit/logic breakdown and error-handling."
    elif intent == "tech_hardware":
        intent_rule = "TASK: [Domain: IoT & Automation] Provide exact pin-to-pin wiring diagram and clean firmware code."
    elif intent == "agriculture":
        intent_rule = "TASK: [Domain: Agriculture & Horticulture] Provide end-to-end crop management, precise seed rate, NPK/DAP schedule, irrigation stages, and pest control."
    elif intent == "medical" or intent == "first_aid":
        intent_rule = "TASK: [Domain: Emergency First Aid & Health] Provide safe, immediate step-by-step emergency care with standard OTC dosages and clear doctor consultation warnings."
    elif intent == "government_scheme":
        intent_rule = "TASK: [Domain: Rural & Farmer Welfare] Explain eligibility, exact subsidy percentage, required documents, and offline/online application portal."
    else:
        intent_rule = "TASK: Provide a comprehensive, accurate, and deeply helpful response."

    # ==================== 4. GROUND TRUTH & MEMORY CONTEXT ====================
    mem_parts = [f"{k}: {v}" for k, v in memories.items()]
    mem_str = f"\n[User Profile & Context: {', '.join(mem_parts)}]" if mem_parts else ""

    lora_info = routing_info.get("lora_adapter", {})
    lora_str = f"\n{lora_info['adapter_context_str']}" if lora_info.get("adapter_context_str") else ""

    tool_str = ""
    if tool_results:
        tool_blocks = [f"--- {t['tool_name']} ---\n{t['result']}" for t in tool_results]
        tool_str = "\n\n[Verified Scientific Knowledge & Calculation Data]:\n" + "\n\n".join(tool_blocks)

    system_prompt = (
        f"You are GramSetu AI (ग्रामसेतु एआई), the ultimate rural intelligence, agriculture expert, and multidisciplinary assistant.\n"
        f"You are designed to assist 10+ lakh diverse farmers, students, rural innovators, and citizens across India.\n\n"
        f"{lang_rule}\n\n"
        f"{reasoning_rule}\n\n"
        f"{tone_style}\n\n"
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
