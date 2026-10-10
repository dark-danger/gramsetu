"""
GramSetu AI - Intent Detection Engine
Classifies user requests into actionable operational intents.
"""
import re

def detect_intent(text: str) -> str:
    if not text:
        return "general_discussion"
    
    clean = text.strip()
    lower = clean.lower()

    # 1. Image Generation Intent
    if lower.startswith('/image') or re.search(r'\b(photo banao|image banao|generate image|picture banao|generate visual)\b', lower):
        return "image_generation"

    # 2. Simple Language Transformation / Translation Request (e.g. "punjabi m mera name likh")
    if re.search(r'\b(punjabi|hindi|english|urdu|bengali|marathi|gurmukhi)\b', lower) and \
       re.search(r'\b(likh|likho|write|translate|convert|transliterate|batao)\b', lower):
        return "simple_transformation"

    # 3. Direct Memory Query Intent ("mera naam kya hai?", "meri zameen kitni hai?")
    if ((re.search(r'\b(mera|meri|my|apna)\s+(?:naam|name|zameen|khet|project|fasal|crop)\b', lower) and
         re.search(r'\b(kya|kitni|kitna|what|how\s+much|batao|bataye|tell|who|\?)\b', lower)) or
        re.search(r'\bwhat(?:\'s|\s+is)\s+my\s+(?:name|land|project|crop)\b', lower) or
        re.search(r'\bhow\s+much\s+land\s+(?:do\s+i\s+have|i\s+own)\b', lower)):
        return "memory_query"

    # 4. Explicit Memory Update Statement ("yash name h mera", "mera naam rahul hai", "mere paas 4 acre zameen hai")
    if (re.search(r'\b([A-Za-z\u0900-\u097F]+)\s+(?:name|naam)\s+(?:h|hai)?\s*(?:mera)?\b', clean) or
        re.search(r'\b(?:mera|meri|my)\s+(?:naam|name|project)\s+(?:is|hai|h)?\s*[A-Za-z0-9_\-]+\b', clean) or
        re.search(r'\b(?:mere\s+paas|i\s+have)\s+\d+(?:\.\d+)?\s*(?:acre|bigha|hectare)\b', lower)):
        # Ensure it's not a question
        if not re.search(r'\b(kya|what|how|kitna|kitni|\?)\b', lower):
            return "memory_update"

    # 5. Language Switch Intent ("english m baat kr", "hindi me bolo")
    if re.search(r'\b(english|hindi|hinglish)\s*(?:m|me|mai|mein)?\s*(?:baat|bol|bolo|kr|karo|batao)\b', lower) or \
       re.search(r'\b(speak|talk|reply)\s*(?:in)?\s*(?:english|hindi|hinglish)\b', lower):
        return "language_switch"

    # 6. Math & Land Calculation
    if re.search(r'(\d+(?:\.\d+)?)\s*(?:acre|acres|bigha|hectare|gaj|square yard)', lower) and \
       re.search(r'\b(bigha|gaj|square yard|convert|hisab|calculate|kitna|seed|beej|fertilizer|khad)\b', lower):
        if re.search(r'\b(seed|beej|fertilizer|khad|dap|urea|wheat|gehu|dhan|sarson)\b', lower):
            return "agriculture"
        return "math_calculation"

    if re.search(r'(?:calculate|hisab|solve|kitna hoga|\bmath\b)?\s*[0-9\.\s\+\-\*\/\(\)]{3,}[0-9]', lower) and \
       re.search(r'[+\-*/]', lower):
        return "math_calculation"

    # 7. Agriculture Domain & Diagnostics (Crops, Soil, Fertilizer, Irrigation, Dairy/Livestock)
    if re.search(r'\b(wheat|gehu|gehun|dhan|rice|paddy|sarson|mustard|cotton|kapas|ganna|sugarcane|kheti|fasal|crop|keeda|sundi|fungus|rust|rot|spray|seed rate|beej|buwai|dap|urea|potash|zinc|khad|fertilizer|irrigation|sinchai|pani|paani|soil|mitti|npk|ph|gypsum|chuna|pashu|gay|bhains|cow|buffalo|doodh|milk|thanela|mastitis|khurpaka|muhpaka|fmd)\b', lower):
        return "agriculture"

    # 8. Government Schemes (KCC, PM Kisan, Ayushman, Fasal Bima, Kusum, Soil Card)
    if re.search(r'\b(pm kisan|pmkisan|ayushman|yojana|yojna|samman nidhi|kcc|kisan credit card|credit card|kisan card|subsidy|fasal bima|crop insurance|ration card|e-kyc|ekyc|kusum|solar pump|soil health|mitti card|pension|shramik)\b', lower):
        return "government_scheme"

    # 9. Emergency First Aid & Clinical Medical (Vitals, Bites, Fever, Pain, Wounds)
    if re.search(r'\b(cpr|cardiac arrest|heart attack|snake|saanp|bite|katna|current|electric shock|burn|jalna|bleeding|khoon|poison|zehar|choking|fracture|blood pressure|bp|pulse rate|heart rate|spo2|vital signs|fever|bukhar|temperature|tapman|sugar level|dast|loose motion|diarrhea|vomiting|ulti|pet dard|stomach pain|headache|sardard|chot|injury|wound|ghav|first aid)\b', lower):
        return "medical"

    # 10. Pharmaceutical & Pharmacology
    if re.search(r'\b(paracetamol|amoxicillin|antibiotic|antibiotics|nsaid|nsaids|antipyretic|antihistamine|ppi|omeprazole|pantoprazole|azithromycin|ibuprofen|drug|medicine|dosage|adme|pharmacokinetics|cold chain|vaccine|dawa|dawai|tablet|goli)\b', lower):
        return "pharmaceutical"

    # 11. Biology & Life Sciences
    if re.search(r'\b(photosynthesis|calvin cycle|c3|c4|cam|chlorophyll|rubisco|nitrogen cycle|rhizobium|azotobacter|trichoderma|dna|rna|genetics|transcription|translation|central dogma|mitochondria|biology)\b', lower):
        return "biology"

    # 12. Tech & Hardware / IoT / Embedded
    if re.search(r'\b(arduino|esp32|flame sensor|relay|soil moisture|ultrasonic|raspberry pi|iot|microcontroller|gpio|sensor|motor driver|l298n|dht11|dht22)\b', lower):
        return "tech_hardware"

    # 13. Programming & Software
    if re.search(r'\b(python|fastapi|javascript|sql|c\+\+|coding|function|class|algorithm|code|compile|bug|script|api|database|git|async|fetch|readablestream)\b', lower):
        return "coding_technical"

    # 14. Greeting & Casual Chit-Chat
    if re.search(r'\b(hi|hello|hey|namaste|pranam|kya\s+h[a]*l|kaise\s+ho|kese\s+ho|kiddan|who\s+are\s+you|bhai|yaar|ram\s+ram|sat\s+sri\s+akal|good\s+morning|good\s+evening|kya\s+chal\s+raha|sab\s+badhiya|kem\s+cho|kasa\s+kay|kaisa\s+hai)\b', lower):
        return "greeting"

    return "general_discussion"
