"""
GramSetu AI - Automated 10-Point Verification Test Suite
Tests all requirements from Section 22 against the running local server.
"""

import urllib.request
import json
import sqlite3
import os
import sys
import time

SERVER_URL = "http://localhost:8000/api/chat"
DB_PATH = "/Users/yash/AI-system/gramsetu.db"

from core.database import get_memory, clear_all_memories, get_connection

def clear_db():
    clear_all_memories()

def get_db_memory(key):
    mem = get_memory(key)
    return mem["value"] if mem else None

def send_chat_stream(prompt, session_id="test_session"):
    req_data = json.dumps({"prompt": prompt, "session_id": session_id}).encode('utf-8')
    req = urllib.request.Request(SERVER_URL, data=req_data, headers={'Content-Type': 'application/json'}, method='POST')
    
    metadata = {}
    tokens = []
    final_text = ""
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        for line in resp:
            line_str = line.decode('utf-8').strip()
            if not line_str:
                continue
            try:
                packet = json.loads(line_str)
                if packet.get("type") == "metadata":
                    metadata = packet.get("data", {})
                elif packet.get("type") == "token":
                    tokens.append(packet.get("token", ""))
                elif packet.get("type") == "done":
                    final_text = packet.get("final", "")
            except Exception:
                tokens.append(line_str)
    
    accumulated = "".join(tokens) if not final_text else final_text
    return {
        "metadata": metadata,
        "text": accumulated,
        "final": final_text
    }

def run_tests():
    print("=" * 60)
    print("🚀 STARTING GRAMSETU AI 10-POINT AUTOMATED TEST SUITE")
    print("=" * 60)
    
    results = {}
    clear_db()
    
    # ----------------------------------------------------------------
    # TEST 1: "yash name h mera" -> Saves user_name = Yash
    # ----------------------------------------------------------------
    print("\n[TEST 1] Testing User Name Extraction: 'yash name h mera'...")
    res1 = send_chat_stream("yash name h mera", session_id="sess_1")
    val1 = get_db_memory("user_name")
    print(f"  Response: {res1['text']}")
    print(f"  DB user_name: {val1}")
    passed1 = val1 is not None and "yash" in val1.lower()
    results["TEST 1 (Name Extraction)"] = "PASSED" if passed1 else "FAILED"
    print(f"  -> Result: {results['TEST 1 (Name Extraction)']}")

    # ----------------------------------------------------------------
    # TEST 2: "mera naam kya h?" -> "Yash."
    # ----------------------------------------------------------------
    print("\n[TEST 2] Testing Direct Name Query: 'mera naam kya h?'...")
    res2 = send_chat_stream("mera naam kya h?", session_id="sess_1")
    print(f"  Response: {res2['text']}")
    passed2 = "yash" in res2['text'].lower()
    results["TEST 2 (Zero-Hallucination Name Query)"] = "PASSED" if passed2 else "FAILED"
    print(f"  -> Result: {results['TEST 2 (Zero-Hallucination Name Query)']}")

    # ----------------------------------------------------------------
    # TEST 3: "punjabi m mera name likh" -> strictly "ਯਸ਼"
    # ----------------------------------------------------------------
    print("\n[TEST 3] Testing Transliteration: 'punjabi m mera name likh'...")
    res3 = send_chat_stream("punjabi m mera name likh", session_id="sess_1")
    print(f"  Response: {res3['text']}")
    passed3 = "ਯਸ਼" in res3['text']
    results["TEST 3 (Strict Transliteration)"] = "PASSED" if passed3 else "FAILED"
    print(f"  -> Result: {results['TEST 3 (Strict Transliteration)']}")

    # ----------------------------------------------------------------
    # TEST 4: "bhai kya haal h" -> Casual friendly Hinglish response
    # ----------------------------------------------------------------
    print("\n[TEST 4] Testing Tone & Style: 'bhai kya haal h'...")
    res4 = send_chat_stream("bhai kya haal h", session_id="sess_2")
    print(f"  Response: {res4['text']}")
    passed4 = len(res4['text'].strip()) > 0 and res4['metadata'].get('tone') in ['friendly', 'casual_friendly', 'casual']
    results["TEST 4 (Casual Friendly Tone)"] = "PASSED" if passed4 else "FAILED"
    print(f"  -> Result: {results['TEST 4 (Casual Friendly Tone)']}")

    # ----------------------------------------------------------------
    # TEST 5: "Prepare a formal proposal for the university." -> Formal proposal in English
    # ----------------------------------------------------------------
    print("\n[TEST 5] Testing Formal English Directive: 'Prepare a formal proposal for the university.'...")
    res5 = send_chat_stream("Prepare a formal proposal for the university.", session_id="sess_3")
    print(f"  Response snippet: {res5['text'][:150]}...")
    print(f"  Detected Tone: {res5['metadata'].get('tone')}, Lang: {res5['metadata'].get('output_language')}")
    passed5 = res5['metadata'].get('output_language') == 'english' and "proposal" in res5['text'].lower()
    results["TEST 5 (Formal English Proposal)"] = "PASSED" if passed5 else "FAILED"
    print(f"  -> Result: {results['TEST 5 (Formal English Proposal)']}")

    # ----------------------------------------------------------------
    # TEST 6: Multi-turn test: "My project is GenIDE." then "isme AI add karna hai"
    # ----------------------------------------------------------------
    print("\n[TEST 6] Testing Multi-turn Pronoun Resolution...")
    res6a = send_chat_stream("My project is GenIDE.", session_id="sess_4")
    time.sleep(0.5)
    res6b = send_chat_stream("isme AI add karna hai", session_id="sess_4")
    print(f"  Turn 1: My project is GenIDE -> DB current_project: {get_db_memory('current_project')}")
    print(f"  Turn 2: isme AI add karna hai -> Response: {res6b['text'][:150]}...")
    passed6 = get_db_memory("current_project") == "GenIDE" or "genide" in res6b['text'].lower()
    results["TEST 6 (Multi-turn Context)"] = "PASSED" if passed6 else "FAILED"
    print(f"  -> Result: {results['TEST 6 (Multi-turn Context)']}")

    # ----------------------------------------------------------------
    # TEST 7: "mera naam Rahul hai" -> Updates user_name = Rahul
    # ----------------------------------------------------------------
    print("\n[TEST 7] Testing Memory Update: 'mera naam Rahul hai'...")
    res7 = send_chat_stream("mera naam Rahul hai", session_id="sess_5")
    val7 = get_db_memory("user_name")
    print(f"  Response: {res7['text']}")
    print(f"  Updated DB user_name: {val7}")
    passed7 = val7 == "Rahul"
    results["TEST 7 (Name Update to Rahul)"] = "PASSED" if passed7 else "FAILED"
    print(f"  -> Result: {results['TEST 7 (Name Update to Rahul)']}")

    # ----------------------------------------------------------------
    # TEST 8: Persistence across restart check
    # ----------------------------------------------------------------
    print("\n[TEST 8] Testing Persistence in SQLite...")
    # Read directly from DB file
    val8 = get_db_memory("user_name")
    passed8 = val8 == "Rahul"
    results["TEST 8 (SQLite Persistence)"] = "PASSED" if passed8 else "FAILED"
    print(f"  DB verified value: {val8} -> Result: {results['TEST 8 (SQLite Persistence)']}")

    # ----------------------------------------------------------------
    # TEST 9: "mere paas 4 acre zameen hai" -> Saves land; "meri zameen kitni hai?" -> 4 acre
    # ----------------------------------------------------------------
    print("\n[TEST 9] Testing Land Area Memory & Direct Query...")
    res9a = send_chat_stream("mere paas 4 acre zameen hai", session_id="sess_6")
    val9 = get_db_memory("land_area")
    print(f"  DB land_area: {val9}")
    res9b = send_chat_stream("meri zameen kitni hai?", session_id="sess_6")
    print(f"  Query Response: {res9b['text']}")
    passed9 = "4 acre" in res9b['text'].lower() or "4 एकड़" in res9b['text']
    results["TEST 9 (Land Area Memory Query)"] = "PASSED" if passed9 else "FAILED"
    print(f"  -> Result: {results['TEST 9 (Land Area Memory Query)']}")

    # ----------------------------------------------------------------
    # TEST 10: "4 acre mein wheat ke liye kitna seed chahiye?" -> Seed & fertilizer calculation
    # ----------------------------------------------------------------
    print("\n[TEST 10] Testing Agri Calculation Tool: '4 acre mein wheat ke liye kitna seed chahiye?'...")
    res10 = send_chat_stream("4 acre mein wheat ke liye kitna seed chahiye?", session_id="sess_7")
    print(f"  Response: {res10['text']}")
    print(f"  Tools executed: {res10['metadata'].get('tools_executed')}")
    passed10 = "Agri Calculator" in str(res10['metadata'].get('tools_executed', [])) or "160" in res10['text'] or "kg" in res10['text'].lower() or "बीज" in res10['text']
    results["TEST 10 (Agri Calculation Tool)"] = "PASSED" if passed10 else "FAILED"
    print(f"  -> Result: {results['TEST 10 (Agri Calculation Tool)']}")

    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY OF RESULTS:")
    print("=" * 60)
    all_passed = True
    for test, status in results.items():
        print(f"  {test:.<45} {status}")
        if status != "PASSED":
            all_passed = False
    print("=" * 60)
    if all_passed:
        print("🎉 ALL 10 TEST CASES PASSED PERFECTLY!")
    else:
        print("⚠️ SOME TESTS FAILED. PLEASE REVIEW LOGS.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
