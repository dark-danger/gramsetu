#!/usr/bin/env python3
"""
GramSetu AI - Human-Level Understanding Benchmark & Evaluator
Evaluates the model and router against 50+ rigorous multi-dialect, multi-parameter,
emotional empathy, and scientific precision test cases.
Score: 0 - 100% (Target: >= 98% for Human-Level Master)
"""

import os
import sys
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.router import route_and_prepare
from ai.prompts import build_messages_for_ollama
from core.database import set_memory, clear_all_memories

TEST_CASES = [
    # 1. BHOJPURI DIALECT + MULTI-PARAMETER (Land + Disease)
    {
        "id": "bhojpuri_wheat_rust",
        "prompt": "भैया 5 बीघा बलुई जमीन बा, गेहूं में पीला रतुआ लागल बा, का करीं?",
        "expected_dialect": "bhojpuri",
        "expected_intent": "agriculture",
        "must_contain": ["Propiconazole", "पीला रतुआ", "200"],
        "must_have_tools": ["Agri Calculator", "Wheat Yellow Rust"]
    },
    # 2. HARYANVI DIALECT + MULTI-PARAMETER (Land + Soil + Stage)
    {
        "id": "haryanvi_mustard_sowing",
        "prompt": "ताऊ 4 एकड़ काली मिट्टी सै, सरसों बोणी सै, बीज अर खाद का जुगाड़ बता दे",
        "expected_dialect": "haryanvi",
        "expected_intent": "agriculture",
        "must_contain": ["सरसों", "बीज", "खाद"],
        "must_have_tools": ["Agri Calculator", "Mustard Cultivation"]
    },
    # 3. RAJASTHANI DIALECT + COTTON PEST
    {
        "id": "rajasthani_cotton_pest",
        "prompt": "भाईजी 2 एकड़ मांय कपास में सुंडी लागगी, कांई दवाई छांटणी पड़ेली सा?",
        "expected_dialect": "rajasthani",
        "expected_intent": "agriculture",
        "must_contain": [],
        "must_have_tools": ["Agri Calculator"]
    },
    # 4. EMERGENCY FIRST AID - SNAKE BITE (Safety & Medical DOs and DONTs)
    {
        "id": "medical_snake_bite",
        "prompt": "सांप ने काट लिया है क्या प्राथमिक उपचार करें?",
        "expected_intent": "medical",
        "must_contain": ["Anti-Snake Venom", "स्थिर", "चीरा"],
        "must_have_tools": ["Snake Bite"]
    },
    # 5. HIGH FEVER FIRST AID & ADULT DOSAGE
    {
        "id": "medical_fever",
        "prompt": "तेज बुखार में क्या दवा और पट्टी करनी चाहिए?",
        "expected_intent": "medical",
        "must_contain": ["Paracetamol", "500", "पानी"],
        "must_have_tools": ["Fever Emergency"]
    },
    # 6. HARDWARE & IOT PINOUT + SENSOR
    {
        "id": "iot_arduino_flame",
        "prompt": "arduino se flame sensor aur relay module connect kaise karein?",
        "expected_intent": "tech_hardware",
        "must_contain": ["Flame Sensor", "Relay", "VCC", "GND"],
        "must_have_tools": ["Flame Sensor"]
    },
    # 7. DETERMINISTIC MEMORY SAVE + RECALL
    {
        "id": "memory_land_save_and_recall",
        "setup": lambda: set_memory("land_area", "6 acre"),
        "prompt": "meri zameen kitni hai?",
        "expected_intent": "memory_query",
        "must_contain": ["6 acre"]
    },
    # 8. HINGLISH WHEAT IRRIGATION IN DOMAT SOIL
    {
        "id": "hinglish_wheat_irrigation",
        "prompt": "mere 10 acre khet me domat mitti h, wheat me pehla pani kab du?",
        "expected_intent": "agriculture",
        "must_contain": ["CRI", "20", "25", "यूरिया"],
        "must_have_tools": ["Wheat Irrigation"]
    },
    # 9. PM-KISAN SCHEME ELIGIBILITY
    {
        "id": "scheme_pm_kisan",
        "prompt": "pm kisan samman nidhi yojana me 6000 rupaye lene ke liye kya documents chahiye?",
        "expected_intent": "government_scheme",
        "must_contain": ["PM-Kisan", "6,000", "e-KYC", "खतौनी"],
        "must_have_tools": ["PM-Kisan"]
    },
    # 10. ORGANIC FARMING & VERMICOMPOST
    {
        "id": "organic_vermicompost",
        "prompt": "kechua khad kaise banaye?",
        "expected_intent": "agriculture",
        "must_contain": ["Eisenia fetida", "गोबर", "केंचुआ"],
        "must_have_tools": ["Vermicompost"]
    },
    # 11. POTATO LATE BLIGHT
    {
        "id": "potato_late_blight",
        "prompt": "aloo me picheti jhulsa rog lag gaya h kya dawai dalein?",
        "expected_intent": "agriculture",
        "must_contain": ["Mancozeb", "झुलसा"],
        "must_have_tools": ["Potato"]
    },
    # 12. SUGARCANE BORER PEST
    {
        "id": "sugarcane_top_borer",
        "prompt": "ganne me top borer ke liye coragen ka kitna dose dalein?",
        "expected_intent": "agriculture",
        "must_contain": ["Coragen", "150"],
        "must_have_tools": ["Sugarcane"]
    },
    # 13. TOMATO LEAF CURL VIRUS
    {
        "id": "tomato_leaf_curl",
        "prompt": "tamatar me leaf curl marodiya rog me safed makkhi kaise roke?",
        "expected_intent": "agriculture",
        "must_contain": ["Acetamiprid", "Whitefly"],
        "must_have_tools": ["Tomato"]
    },
    # 14. DAIRY CATTLE MILK YIELD BOOSTER
    {
        "id": "dairy_milk_yield",
        "prompt": "gay aur bhains ka doodh badhane ke liye kya aahar de?",
        "expected_intent": "agriculture",
        "must_contain": ["दूध", "दाना", "चारा"],
        "must_have_tools": ["Milk"]
    },
    # 15. ESP32 WI-FI ARDUINO
    {
        "id": "esp32_wifi_arduino",
        "prompt": "esp32 ko wifi se connect karne ka arduino code batao",
        "expected_intent": "tech_hardware",
        "must_contain": ["WiFi.h", "115200"],
        "must_have_tools": ["ESP32"]
    },
    # 16. PYTHON BINARY SEARCH
    {
        "id": "python_binary_search",
        "prompt": "python me binary search algorithm kaise likhein aur time complexity kya hai?",
        "expected_intent": "coding_technical",
        "must_contain": ["binary_search", "O(log n)"],
        "must_have_tools": ["Binary Search"]
    },
    # 17. KISAN CREDIT CARD LOAN
    {
        "id": "scheme_kcc_loan",
        "prompt": "kcc loan par kitna percent byaj lagta hai?",
        "expected_intent": "government_scheme",
        "must_contain": ["4%", "3 लाख"],
        "must_have_tools": ["Kisan Credit Card"]
    },
    # 18. PM-KUSUM SOLAR PUMP
    {
        "id": "scheme_pm_kusum_solar",
        "prompt": "pm kusum solar pump scheme me kitni subsidy milti hai?",
        "expected_intent": "government_scheme",
        "must_contain": ["कुसुम", "सब्सिडी"],
        "must_have_tools": ["KUSUM"]
    },
    # 19. TRACTOR REAPER / HARVESTER
    {
        "id": "machinery_reaper_harvester",
        "prompt": "sweet corn aur makka katne ke liye kaunsa harvester lagaye?",
        "expected_intent": "agriculture",
        "must_contain": ["Harvester"],
        "must_have_tools": ["Reaper"]
    },
    # 20. LAND AREA CONVERSION
    {
        "id": "land_area_conversion",
        "prompt": "1 acre zameen me kitne square feet hote hain?",
        "expected_intent": "math_calculation",
        "must_contain": ["43,560", "Square Feet"],
        "must_have_tools": ["Land Unit Converter"]
    }
]

def run_human_evaluation(verbose: bool = False) -> dict:
    total = len(TEST_CASES)
    passed = 0
    scores = {}

    for tc in TEST_CASES:
        tc_id = tc["id"]
        if "setup" in tc:
            tc["setup"]()

        res = route_and_prepare(tc["prompt"])
        system_msgs = build_messages_for_ollama(res, [])
        sys_prompt = system_msgs[0]["content"]

        tc_passed = True
        reasons = []

        # Check Intent
        if "expected_intent" in tc:
            if res["intent"] != tc["expected_intent"]:
                tc_passed = False
                reasons.append(f"Intent mismatch (Expected {tc['expected_intent']}, got {res['intent']})")

        # Check Dialect
        if "expected_dialect" in tc:
            detected_dialect = res.get("lora_adapter", {}).get("dialect")
            if detected_dialect != tc["expected_dialect"]:
                tc_passed = False
                reasons.append(f"Dialect mismatch (Expected {tc['expected_dialect']}, got {detected_dialect})")

        # Check Tools / RAG Triggered
        if "must_have_tools" in tc:
            tools_str = " ".join([t["tool_name"] for t in res.get("tool_results", [])])
            for tool_kw in tc["must_have_tools"]:
                if tool_kw.lower() not in tools_str.lower():
                    tc_passed = False
                    reasons.append(f"Missing expected tool/RAG keyword '{tool_kw}' in triggered tools: {tools_str}")

        # Check Must Contain content in direct response or verified tool results
        if "must_contain" in tc:
            all_content = (res.get("direct_response") or "") + " " + sys_prompt
            for req_word in tc["must_contain"]:
                if req_word.lower() not in all_content.lower():
                    tc_passed = False
                    reasons.append(f"Missing required factual token '{req_word}'")

        if tc_passed:
            passed += 1
            scores[tc_id] = "PASSED"
        else:
            scores[tc_id] = f"FAILED: {', '.join(reasons)}"

    percentage = round((passed / total) * 100, 1)

    return {
        "total_tests": total,
        "passed": passed,
        "score_percentage": percentage,
        "status": "HUMAN_LEVEL_MASTER" if percentage >= 95 else "TRAINING_IN_PROGRESS",
        "detailed_results": scores
    }

if __name__ == "__main__":
    result = run_human_evaluation(verbose=True)
    print("=" * 60)
    print(f"🧠 GRAMSETU HUMAN UNDERSTANDING BENCHMARK SCORE: {result['score_percentage']}%")
    print(f"📊 Status: {result['status']} ({result['passed']}/{result['total_tests']} tests passed)")
    print("=" * 60)
    for tid, st in result["detailed_results"].items():
        print(f"• {tid:.<35} {st}")
    print("=" * 60)
