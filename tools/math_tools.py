"""
GramSetu AI - High-Precision Arithmetic & Math Tools
"""
import re

def evaluate_math(prompt: str) -> dict:
    clean = prompt.strip()
    m = re.search(r'([0-9\.\s\+\-\*\/\(\)]{3,}[0-9])', clean)
    if m:
        expr = m.group(1).strip()
        # Safe expression check
        if re.match(r'^[0-9\.\s\+\-\*\/\(\)]+$', expr) and any(op in expr for op in ['+', '-', '*', '/']):
            try:
                val = eval(expr, {"__builtins__": None}, {})
                if isinstance(val, (int, float)):
                    return {
                        "tool_name": "Math Calculator",
                        "expression": expr,
                        "result": val,
                        "text": f"🔢 **Calculation:** `{expr}` = **{val}**"
                    }
            except Exception:
                pass
    return None
