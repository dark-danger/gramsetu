"""
GramSetu AI - Response Validation & Hallucination Guard Engine
Validates LLM output against confirmed deterministic memory and requested constraints.
"""
import re

def validate_and_sanitize(response_text: str, routing_info: dict) -> str:
    if not response_text or not response_text.strip():
        if routing_info.get("output_language") in ["hindi", "hinglish"]:
            return "नमस्ते! मैं आपकी क्या सहायता कर सकता हूँ?"
        return "Hello! How can I assist you today?"

    out = response_text.strip()

    # 0. If direct deterministic response was generated, return it untouched
    if routing_info.get("direct_response"):
        return routing_info["direct_response"]

    # 1. Strip raw thinking tags if any leaked
    out = re.sub(r'<think>[\s\S]*?<\/think>', '', out).strip()
    out = re.sub(r'<\|im_start\|>[\s\S]*?<\|im_end\|>', '', out).strip()

    # 2. Check for Name Hallucination against confirmed memory
    confirmed_memories = routing_info.get("relevant_memories", {})
    actual_user_name = confirmed_memories.get("user_name")
    
    if actual_user_name:
        # If user asks for their name or translation, ensure no false names appear
        if routing_info.get("intent") in ["memory_query", "simple_transformation"]:
            if routing_info.get("output_language") == "punjabi":
                from core.router import transliterate_to_gurmukhi
                punjabi_name = transliterate_to_gurmukhi(actual_user_name)
                if punjabi_name not in out:
                    return punjabi_name
            else:
                if actual_user_name.lower() not in out.lower():
                    return f"{actual_user_name}."

    # 3. Truncate runaway pip install loops or long package repetitions
    def clean_pip_runs(match):
        pkgs = match.group(1).split()
        if len(pkgs) > 4:
            unique_pkgs = list(dict.fromkeys(pkgs))[:4]
            return f"pip install {' '.join(unique_pkgs)}"
        return match.group(0)

    out = re.sub(r'pip install ([a-zA-Z0-9_\-\s]{30,})', clean_pip_runs, out)

    # 4. Strip repetitive filler intros
    out = re.sub(r'^(?:Aap is tarah se solve kar sakte hain\.?|Iska main reason yeh hai:?)\s*', '', out, flags=re.IGNORECASE).strip()

    # 5. Deduplicate repetitive lines & terminate runaway loops
    lines = out.split("\n")
    cleaned_lines = []
    seen_normalized = set()
    prev_num = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            continue

        # Check for numbered list loop resets (e.g. 1..10 then 1 again)
        m_num = re.match(r'^(\d+)[\.\)\-]\s*(.*)$', stripped)
        if m_num:
            curr_num = int(m_num.group(1))
            line_body = m_num.group(2).strip()
            if prev_num is not None and curr_num <= prev_num and curr_num == 1:
                break
            prev_num = curr_num
            norm_key = re.sub(r'[^a-zA-Z0-9\u0900-\u097F]', '', line_body.lower())
        else:
            norm_key = re.sub(r'[^a-zA-Z0-9\u0900-\u097F]', '', stripped.lower())

        # Discard repeated bullet/content
        if len(norm_key) > 8:
            if norm_key in seen_normalized:
                continue
            seen_normalized.add(norm_key)

        cleaned_lines.append(stripped)

    # Limit maximum list length to keep answers crisp & to-the-point
    out = "\n".join(cleaned_lines).strip()

    return out
