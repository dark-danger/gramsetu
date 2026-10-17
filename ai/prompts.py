"""
GramSetu AI - Master Cognitive Reasoning & Chain-of-Thought (CoT) Engine
Delivers high-accuracy, deeply reasoned, multidisciplinary intelligence across all domains.
Features:
- Step-by-step reasoning architecture (Soch-Vichar & Problem Deconstruction)
- Zero-hallucination factual grounding for Agriculture, IoT/Hardware, Coding, Medicine, and Governance
- Adaptive multi-dialect fluency (Hindi, Hinglish, Punjabi, English)
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

    # Detect greeting / trivial interaction vs substantive query
    is_greeting = intent == "greeting" or bool(re.search(r'^(hi|hello|hey|namaste|pranam|ram ram|sat sri akal|kya haal|kese ho|kaise ho)\b', clean_lower))

    # ==================== 1. LANGUAGE & DIALECT DIRECTIVE ====================
    if out_lang == "hinglish":
        lang_rule = (
            "LANGUAGE & DIALECT DIRECTIVE: Natural, fluent Conversational Hinglish (Roman Hindi).\n"
            "• Tone: Respectful, knowledgeable, practical, and highly empathetic (like a senior expert agricultural & tech mentor).\n"
            "• Keep technical/botanical/drug/code terms in precise English (e.g., 'Propiconazole', 'DAP', 'ESP32', 'FastAPI', 'Time Complexity').\n"
            "• Use clear sentences that a common citizen as well as a technical person can easily follow."
        )
    elif out_lang == "hindi":
        lang_rule = (
            "LANGUAGE & DIALECT DIRECTIVE: स्पष्ट, शुद्ध, प्रामाणिक एवं सरल देवनागरी हिंदी।\n"
            "• शैली: आदरणीय, मार्गदर्शक, वैज्ञानिक एवं व्यावहारिक।\n"
            "• तकनीकी व दवाइयों के नाम देवनागरी के साथ कोष्ठक में अंग्रेजी में भी लिखें ताकि किसान/उपयोगकर्ता को स्पष्ट रहे।"
        )
    elif out_lang == "punjabi":
        lang_rule = (
            "LANGUAGE DIRECTIVE: Strictly natural, polite Punjabi in Gurmukhi script (ਪੰਜਾਬੀ).\n"
            "• ਸ਼ੈਲੀ: ਸਤਿਕਾਰਯੋਗ, ਸਪੱਸ਼ਟ, ਵਿਗਿਆਨਕ ਅਤੇ ਲਾਭਦਾਇਕ।"
        )
    else:
        lang_rule = (
            "LANGUAGE DIRECTIVE: Polished, authoritative, highly articulative, and structured English."
        )

    # ==================== 2. MASTER REASONING & DEPTH DIRECTIVE ====================
    if is_greeting:
        reasoning_rule = (
            "REASONING & FORMATTING MODE: WARM COURTEOUS GREETING.\n"
            "• Respond warmly and respectfully in 1-2 sentences.\n"
            "• Ask how you can help them today with farming, technology, government schemes, or calculations."
        )
    else:
        reasoning_rule = (
            "REASONING & FORMATTING MODE: DEEP REASONING & HIGH-ACCURACY KNOWLEDGE (SOCH-VICHAR):\n"
            "1. THINK STEP-BY-STEP: Thoroughly deconstruct the question, determine root cause, requirements, and optimal solution.\n"
            "2. DIRECT ACTIONABLE SOLUTION: State the primary answer, recommendation, chemical dose, pinout, or algorithm right at the start.\n"
            "3. STEP-BY-STEP BREAKDOWN: Explain *how* and *why* it works in clear numbered steps or structured sections with emojis (🌾, ⚙️, 🧪, 💡, ⚠️).\n"
            "4. EXACT SPECIFICATIONS: Always give exact quantities (kg/acre, ml/L of water, GPIO pin numbers, syntax, eligibility criteria, portal names).\n"
            "5. PRECAUTIONS & SAFETY: Conclude with practical warnings, safety tips, optimal timings, or doctor/expert disclaimers where relevant.\n"
            "6. NO HALF-ANSWERS: Never give incomplete or vague answers. Deliver a thoroughly satisfying, complete master-grade response."
        )

    # ==================== 3. CONVERSATIONAL CONTINUITY ====================
    continuity_rule = (
        "CONVERSATIONAL CONTINUITY:\n"
        "• This is an active ongoing dialogue. Seamlessly connect with previous turns if the user asks a follow-up or uses pronouns ('isme', 'isko', 'that').\n"
        "• If the user switches to a completely new topic, transition immediately to the new topic with full focus."
    )

    # ==================== 4. DOMAIN GROUNDING ====================
    if intent == "simple_transformation":
        intent_rule = "TASK: Output the exact requested transliteration, translation, or text transformation."
    elif intent == "coding_technical":
        intent_rule = "TASK: [Software/Coding] Provide robust, production-ready code with step-by-step logic, complexity analysis, and edge cases."
    elif intent == "tech_hardware":
        intent_rule = "TASK: [IoT/Electronics] Provide exact pin-to-pin wiring (VCC, GND, GPIO), circuit logic, and complete working code."
    elif intent == "agriculture":
        intent_rule = "TASK: [Agriculture/Agronomy] Provide scientific seed rate, fertilizer schedule (Basal & Top dressing), irrigation stages, and pest control with exact trade names & dosages."
    elif intent in ["medical", "first_aid"]:
        intent_rule = "TASK: [Emergency First Aid & Health] Provide immediate life-saving first-aid protocol, standard adult OTC doses, red-flag symptoms, and mandatory doctor consultation warning."
    elif intent == "government_scheme":
        intent_rule = "TASK: [Government Schemes] State exact financial benefit, eligibility conditions, required documents, and official application portal step-by-step."
    elif intent == "math_calculation":
        intent_rule = "TASK: [Mathematics & Conversions] Show complete step-by-step calculations with exact conversion formulas and regional standards."
    else:
        intent_rule = "TASK: Provide a comprehensive, accurate, step-by-step reasoned answer covering all dimensions of the query."

    # ==================== 5. CONTEXT & MEMORY INTEGRATION ====================
    mem_parts = [f"{k}: {v}" for k, v in memories.items()]
    mem_str = f"\n[User Profile Context: {', '.join(mem_parts)}]" if mem_parts else ""

    lora_info = routing_info.get("lora_adapter", {})
    lora_str = f"\n{lora_info['adapter_context_str']}" if lora_info.get("adapter_context_str") else ""

    tool_str = ""
    if tool_results:
        tool_blocks = [f"--- {t['tool_name']} ---\n{t['result']}" for t in tool_results]
        tool_str = "\n\n[Verified Ground Truth Knowledge Matrix]:\n" + "\n\n".join(tool_blocks)

    system_prompt = (
        f"You are GramSetu AI (ग्रामसेतु एआई), an elite, deeply thoughtful, multidisciplinary artificial intelligence assistant.\n"
        f"You serve farmers, students, rural innovators, engineers, and citizens with uncompromising accuracy and deep reasoning.\n\n"
        f"{reasoning_rule}\n\n"
        f"{lang_rule}\n\n"
        f"{continuity_rule}\n\n"
        f"{intent_rule}"
        f"{lora_str}"
        f"{mem_str}"
        f"{tool_str}"
    )

    messages = [{"role": "system", "content": system_prompt}]

    # Append recent conversation turns
    for turn in recent_history[-8:]:
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
