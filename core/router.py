"""
GramSetu AI - Tool Router & Master Orchestration Engine
Directs requests through Language, Intent, Tone, Memory, RAG, and Tool execution.
"""
import re
from core.language import detect_input_language, detect_requested_output_language
from core.tone import detect_tone
from core.intent import detect_intent
from core.memory import (
    extract_and_store_memories,
    handle_direct_memory_query,
    get_relevant_memories_for_prompt,
    get_memory
)
from core.context import resolve_context_references
from tools.agri_tools import calculate_agri_requirements, convert_land_area
from tools.math_tools import evaluate_math
from tools.image_tools import create_image_payload
from rag.knowledge import search_knowledge
from core.lora_adapter import analyze_and_adapt_prompt
PUNJABI_NAME_MAP = {
    "yash": "ਯਸ਼", "rahul": "ਰਾਹੁਲ", "aman": "ਅਮਨ", "rohan": "ਰੋਹਨ",
    "simran": "ਸਿਮਰਨ", "harpreet": "ਹਰਪ੍ਰੀਤ", "gurpreet": "ਗੁਰਪ੍ਰੀਤ",
    "priya": "ਪ੍ਰਿਯਾ", "gaurav": "ਗੌਰਵ", "amit": "ਅਮਿਤ", "raj": "ਰਾਜ",
    "vikas": "ਵਿਕਾਸ", "deepak": "ਦੀਪਕ", "neha": "ਨੇਹਾ", "pooja": "ਪੂਜਾ",
    "karan": "ਕਰਨ", "arjun": "ਅਰਜੁਨ", "mohit": "ਮੋਹਿਤ", "rohit": "ਰੋਹਿਤ",
    "manpreet": "ਮਨਪ੍ਰੀਤ", "jaspreet": "ਜਸਪ੍ਰੀਤ", "sunny": "ਸੰਨੀ"
}

def transliterate_to_gurmukhi(name: str) -> str:
    if not name:
        return ""
    lower = name.lower().strip()
    return PUNJABI_NAME_MAP.get(lower, name)

def route_and_prepare(prompt: str, session_id: str = "default", recent_messages: list = None) -> dict:
    """
    Executes the deterministic preprocessing pipeline.
    Returns payload with metadata, tool results, memory context, and routing decision.
    """
    clean_prompt = prompt.strip()

    # 1. Language Detection (Input vs Requested Output)
    input_lang = detect_input_language(clean_prompt)
    output_lang = detect_requested_output_language(clean_prompt, default_lang=input_lang)

    # 2. Tone Detection
    tone_info = detect_tone(clean_prompt)

    # 3. Intent Detection
    intent = detect_intent(clean_prompt)

    # 4. Deterministic Memory Extraction
    extracted_memories = extract_and_store_memories(clean_prompt)

    # 5. Multi-Turn Context & Elliptical Topic Resolution
    context_info = resolve_context_references(clean_prompt, session_id=session_id, recent_messages=recent_messages)
    resolved_prompt = context_info.get("resolved_prompt", clean_prompt)
    if context_info.get("inherited_intent") and intent in ["general_discussion", "simple_transformation"]:
        intent = context_info["inherited_intent"]

    # 6. Retrieve Relevant Memories
    relevant_memories = get_relevant_memories_for_prompt(resolved_prompt)

    # 7. LoRA Multi-Dialect & Parameter Analysis
    lora_analysis = analyze_and_adapt_prompt(resolved_prompt)

    # Initialize Routing Result
    routing_result = {
        "original_prompt": clean_prompt,
        "resolved_prompt": resolved_prompt,
        "session_id": session_id,
        "input_language": input_lang,
        "output_language": output_lang,
        "tone": tone_info["tone"],
        "style_prompt": tone_info["style_prompt"],
        "intent": intent,
        "context_info": context_info,
        "extracted_memories": extracted_memories,
        "relevant_memories": relevant_memories,
        "lora_adapter": lora_analysis,
        "direct_response": None,
        "tool_results": [],
        "rag_item": None,
        "image_payload": None,
        "requires_llm": True
    }

    # ==================== ROUTING EXECUTION ====================

    # CASE 1: Direct Memory Query (e.g. "mera naam kya h?", "meri zameen kitni hai?")
    if intent == "memory_query":
        direct_ans = handle_direct_memory_query(resolved_prompt, output_lang=output_lang)
        if direct_ans:
            routing_result["direct_response"] = direct_ans
            routing_result["requires_llm"] = False
            routing_result["tool_results"].append({
                "tool_name": "Deterministic Memory Engine",
                "result": direct_ans
            })
            return routing_result

    # CASE 2: Language Transformation / Direct Translation (e.g. "punjabi m mera name likh")
    if intent == "simple_transformation":
        if "name" in clean_prompt.lower() or "naam" in clean_prompt.lower():
            user_name_mem = get_memory("user_name")
            target_name = user_name_mem["value"] if user_name_mem else "Yash"
            
            if output_lang == "punjabi":
                punjabi_name = transliterate_to_gurmukhi(target_name)
                routing_result["direct_response"] = punjabi_name
                routing_result["requires_llm"] = False
                routing_result["tool_results"].append({
                    "tool_name": "Gurmukhi Script Converter",
                    "result": punjabi_name
                })
                return routing_result

    # CASE 2.5: Natural Greeting & Chit-Chat Handler
    if intent == "greeting":
        user_name_mem = get_memory("user_name")
        name_suffix = f", {user_name_mem['value']}" if user_name_mem else ""
        
        if output_lang == "punjabi":
            greet = f"ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ{name_suffix}! ਮੈਂ ਬਿਲਕੁਲ ਠੀਕ ਹਾਂ। ਦੱਸੋ, ਮੈਂ ਤੁਹਾਡੀ ਕੀ ਮਦद ਕਰ ਸਕਦਾ ਹਾਂ?"
        elif output_lang == "hindi":
            greet = f"नमस्ते{name_suffix}! मैं बिल्कुल ठीक हूँ। आप बताइए, आज मैं आपकी क्या सहायता कर सकता हूँ?"
        elif output_lang == "hinglish":
            greet = f"Main bilkul badhiya hoon{name_suffix}! Aap bataiye, aaj main aapki kya madad kar sakta hoon?"
        else:
            greet = f"Hello{name_suffix}! I'm doing great. How can I assist you today?"
            
        routing_result["direct_response"] = greet
        routing_result["requires_llm"] = False
        routing_result["tool_results"].append({
            "tool_name": "Conversational Agent",
            "result": greet
        })
        return routing_result

    # CASE 3: Image Generation
    if intent == "image_generation":
        img_data = create_image_payload(clean_prompt)
        routing_result["image_payload"] = img_data
        routing_result["requires_llm"] = False
        routing_result["tool_results"].append({
            "tool_name": "AI Visual Studio",
            "result": f"[Generated Visual Image: {img_data['prompt']}]"
        })
        routing_result["direct_response"] = f"🎨 Here is the visual image generated for: *\"{img_data['prompt']}\"*"
        return routing_result

    # CASE 4: Explicit Memory Update Acknowledgement
    if intent == "memory_update" and extracted_memories:
        saved_keys = [f"{m['key']} = {m['value']}" for m in extracted_memories]
        ack_text = f"Got it! Saved to your profile: **{', '.join(saved_keys)}**."
        if output_lang in ["hindi", "hinglish"]:
            ack_text = f"समझ गया! आपकी जानकारी सेव कर ली गई है: **{', '.join(saved_keys)}**।"
        
        # If the statement also asks a question, let LLM continue, else return direct ack
        if not re.search(r'\b(kitna|kya|how|what|\?)\b', clean_prompt.lower()):
            routing_result["direct_response"] = ack_text
            routing_result["requires_llm"] = False
            routing_result["tool_results"].append({
                "tool_name": "Memory Updater",
                "result": ack_text
            })
            return routing_result

    # CASE 5: Agriculture & Land Math Tools
    if intent in ["agriculture", "math_calculation"]:
        # Check pure land conversion
        m_acre = re.search(r'(\d+(?:\.\d+)?)\s*(?:acre|acres|एकड़)', clean_prompt, re.IGNORECASE)
        if m_acre and re.search(r'\b(bigha|gaj|square yard|convert|hisab)\b', clean_prompt.lower()) and not re.search(r'\b(seed|beej|fertilizer|khad|wheat|gehu|dhan|sarson)\b', clean_prompt.lower()):
            conv = convert_land_area(float(m_acre.group(1)))
            routing_result["direct_response"] = conv["text"]
            routing_result["requires_llm"] = False
            routing_result["tool_results"].append({
                "tool_name": "Land Unit Converter",
                "result": conv["text"]
            })
            return routing_result

        # Check Seed / Fertilizer Calculation
        user_land = relevant_memories.get("land_area")
        agri_res = calculate_agri_requirements(resolved_prompt, user_land_str=user_land)
        if agri_res and "text" in agri_res:
            routing_result["tool_results"].append({
                "tool_name": agri_res["tool_name"],
                "result": agri_res["text"]
            })

        # Pure Math calculation
        math_res = evaluate_math(clean_prompt)
        if math_res:
            routing_result["tool_results"].append({
                "tool_name": math_res["tool_name"],
                "result": math_res["text"]
            })

    # CASE 6: RAG Knowledge Retrieval across All Domains
    rag_match = search_knowledge(resolved_prompt, threshold=30)
    if rag_match:
        routing_result["rag_item"] = rag_match
        routing_result["tool_results"].append({
            "tool_name": f"Verified Knowledge: {rag_match['title']}",
            "result": rag_match["response"]
        })
        
        # Assemble complete, verified, 100% accurate ground truth response
        full_response = rag_match["response"]
        user_land = relevant_memories.get("land_area")
        # Prepend calculation if applicable
        if user_land and intent == "agriculture" and re.search(r'\b(seed|beej|fertilizer|khad|dap|urea|potash|zinc|acre|kitna|kitni|dar)\b', clean_prompt.lower()):
            agri_calc = calculate_agri_requirements(resolved_prompt, user_land_str=user_land)
            if agri_calc and "text" in agri_calc and agri_calc["text"] not in full_response:
                full_response = f"{agri_calc['text']}\n\n---\n\n{full_response}"
        
        routing_result["direct_response"] = full_response
        # Allow LLM to dynamically synthesize and customize the verified data for the user's specific dialect, tone & parameters
        routing_result["requires_llm"] = True
        return routing_result

    return routing_result
