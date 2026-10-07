"""
GramSetu AI - Full Live Automated Agent Interaction Tester
Simulates real interactive user conversations turn-by-turn against the running server.
"""

import urllib.request
import json
import time

SERVER_URL = "http://localhost:8000/api/chat"

def chat_turn(prompt, session_id="live_user_session"):
    print(f"\n💬 USER: \"{prompt}\"")
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
                
    response_text = final_text if final_text else "".join(tokens)
    
    print(f"🧠 [Metadata] Intent: {metadata.get('intent')} | Tone: {metadata.get('tone')} | Lang: {metadata.get('input_language')} -> {metadata.get('output_language')}")
    if metadata.get('memories_used'):
        print(f"💾 [Memories Used]: {metadata.get('memories_used')}")
    if metadata.get('tools_executed'):
        print(f"🛠️ [Tools Executed]: {metadata.get('tools_executed')}")
    print(f"🤖 GRAMSETU AI:\n{response_text}")
    print("-" * 60)
    return metadata, response_text

def run_live_testing():
    print("=" * 60)
    print("🌾 STARTING LIVE MULTI-TURN INTERACTIVE SYSTEM TESTING")
    print("=" * 60)
    
    sess = f"session_{int(time.time())}"
    
    # Turn 1: Casual Greeting
    chat_turn("kya hal h", session_id=sess)
    time.sleep(1)

    # Turn 2: User Identification & Farm Setup
    chat_turn("yash name h mera aur mere paas 5 acre zameen hai", session_id=sess)
    time.sleep(1)

    # Turn 3: Memory Verification
    chat_turn("mera naam kya h aur meri zameen kitni hai?", session_id=sess)
    time.sleep(1)

    # Turn 4: Transliteration
    chat_turn("punjabi m mera name likh", session_id=sess)
    time.sleep(1)

    # Turn 5: Agricultural Math Calculation with Land Memory
    chat_turn("5 acre me gehu ugana hai, kitna seed aur khad lagega?", session_id=sess)
    time.sleep(1)

    # Turn 6: Multi-Turn Technical Project Binding
    chat_turn("My project is GenIDE", session_id=sess)
    time.sleep(1)
    chat_turn("isme local AI add karna hai step by step batao", session_id=sess)
    time.sleep(1)

    # Turn 7: Hardware & IoT Circuit
    chat_turn("arduino se flame sensor aur relay kaise connect kare code k sath", session_id=sess)
    time.sleep(1)

    # Turn 8: First-Aid Emergency
    chat_turn("emergency: kisi ko saanp ne kaat liya hai turant kya kare", session_id=sess)
    time.sleep(1)

    print("\n" + "=" * 60)
    print("🎉 LIVE INTERACTIVE TESTING COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_live_testing()
