"""
GramSetu AI - Context Resolution Engine
Resolves multi-turn references, pronouns (isme, isko, ye, woh, this, that),
and builds structured, compact context windows for inference.
"""
import re
from core.database import get_recent_messages, get_memory

PRONOUN_PATTERNS = [
    r'\bisme\b', r'\bisko\b', r'\busme\b', r'\busko\b', r'\biska\b', r'\biski\b',
    r'\byeh\b', r'\bye\b', r'\bwoh\b', r'\bwo\b', r'\bthis\b', r'\bthat\b',
    r'\bprevious\s+one\b', r'\bsame\s+wala\b', r'\bispar\b', r'\bispe\b'
]

def resolve_context_references(current_prompt: str, session_id: str = "default") -> str:
    """
    Inspects recent conversation to resolve pronoun references.
    Returns augmented prompt or context annotation.
    """
    clean = current_prompt.strip()
    lower = clean.lower()

    # Check if prompt contains anaphoric pronouns
    has_pronoun = any(re.search(pat, lower) for pat in PRONOUN_PATTERNS)
    if not has_pronoun:
        return clean

    recent = get_recent_messages(session_id, limit=4)
    if not recent:
        # Fallback to persistent memory if available
        curr_proj = get_memory("current_project")
        if curr_proj and ("project" in lower or "isme" in lower or "isko" in lower or "ai" in lower):
            return f"{clean} (Context: In the user's project '{curr_proj['value']}')"
        return clean

    # Find the most recent explicit subject mentioned
    resolved_subject = None
    for msg in reversed(recent):
        text = msg.get("content", "")
        
        # Check for project mention
        m_proj = re.search(r'\b(?:project\s+(?:is|name\s+is|hai)?\s*([A-Za-z0-9_\-]+))\b', text, re.IGNORECASE)
        if m_proj:
            resolved_subject = f"Project: {m_proj.group(1)}"
            break

        # Check for crop mention
        m_crop = re.search(r'\b(wheat|gehu|dhan|rice|sarson|mustard|cotton|potato|aalu)\b', text, re.IGNORECASE)
        if m_crop:
            resolved_subject = f"Crop: {m_crop.group(1)}"
            break

        # Check for scheme mention
        m_scheme = re.search(r'\b(pm kisan|ayushman|kcc|samman nidhi)\b', text, re.IGNORECASE)
        if m_scheme:
            resolved_subject = f"Scheme: {m_scheme.group(1)}"
            break

    # If no subject from recent history, check persistent memory
    if not resolved_subject:
        curr_proj = get_memory("current_project")
        if curr_proj and ("ai" in lower or "code" in lower or "isme" in lower or "feature" in lower):
            resolved_subject = f"Project: {curr_proj['value']}"
        else:
            curr_crop = get_memory("primary_crop")
            if curr_crop and ("khad" in lower or "fertilizer" in lower or "seed" in lower or "spray" in lower):
                resolved_subject = f"Crop: {curr_crop['value']}"

    if resolved_subject:
        return f"{clean} [Resolved Context Reference -> {resolved_subject}]"

    return clean
