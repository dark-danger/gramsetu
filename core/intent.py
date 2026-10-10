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
    if re.search(r'(?:^|[^\w\u0900-\u097F\u0A00-\u0A7F])(wheat|gehu|gehun|गेहूं|गेहू|कनक|dhan|rice|paddy|धान|चावल|झोना|sarson|mustard|सरसों|सरसो|cotton|kapas|कपास|नरमा|ganna|sugarcane|गन्ना|kheti|खेती|खेति|fasal|फसल|फ़सल|crop|keeda|कीड़ा|कीट|sundi|सूंडी|fungus|फंगस|rust|रतुआ|रोली|rot|spray|छिड़काव|स्प्रे|seed rate|beej|बीज|बियां|buwai|बुवाई|बोनी|dap|डीएप|यूरिया|urea|potash|पोटाश|zinc|जिंक|khad|खाद|fertilizer|उर्वरक|irrigation|sinchai|सिंचाई|सिचाई|पानी|pani|paani|soil|mitti|मिट्टी|माटी|npk|ph|gypsum|जिप्सम|chuna|चूना|pashu|पशु|गाय|gay|भैंस|bhains|cow|buffalo|doodh|दूध|milk|thanela|थनैला|mastitis|khurpaka|खुरपका|muhpaka|मुंहपका|fmd)(?:$|[^\w\u0900-\u097F\u0A00-\u0A7F])', lower):
        return "agriculture"

    # 8. Government Schemes (KCC, PM Kisan, Ayushman, Fasal Bima, Kusum, Soil Card)
    if re.search(r'(?:^|[^\w\u0900-\u097F\u0A00-\u0A7F])(pm kisan|pmkisan|ayushman|yojana|yojna|योजना|samman nidhi|सम्मान निधि|kcc|kisan credit card|क्रेडिट कार्ड|credit card|kisan card|subsidy|सब्सिडी|अनुदान|fasal bima|फसल बीमा|crop insurance|ration card|राशन कार्ड|e-kyc|ekyc|kusum|कुसुम|solar pump|सोलर पंप|soil health|मृदा स्वास्थ्य|mitti card|pension|पेंशन|shramik|श्रमिक)(?:$|[^\w\u0900-\u097F\u0A00-\u0A7F])', lower):
        return "government_scheme"

    # 9. Emergency First Aid & Clinical Medical (Vitals, Bites, Fever, Pain, Wounds)
    if re.search(r'(?:^|[^\w\u0900-\u097F\u0A00-\u0A7F])(cpr|cardiac arrest|heart attack|snake|saanp|सांप|साँप|bite|काटना|katna|डसना|current|electric shock|करंट|burn|जलना|jalna|bleeding|खून|khoon|poison|zehar|ज़हर|choking|fracture|हड्डी|blood pressure|bp|pulse rate|heart rate|spo2|vital signs|fever|bukhar|बुखार|तावत|temperature|tapman|तापमान|sugar level|dast|दस्त|loose motion|diarrhea|vomiting|ulti|उल्टी|pet dard|पेट दर्द|stomach pain|headache|sardard|सिरदर्द|chot|चोट|injury|wound|ghav|घाव|first aid|प्राथमिक उपचार)(?:$|[^\w\u0900-\u097F\u0A00-\u0A7F])', lower):
        return "medical"

    # 10. Pharmaceutical & Pharmacology
    if re.search(r'(?:^|[^\w\u0900-\u097F\u0A00-\u0A7F])(paracetamol|पैरासिटामोल|amoxicillin|antibiotic|antibiotics|एंटीबायोटिक|nsaid|nsaids|antipyretic|antihistamine|ppi|omeprazole|pantoprazole|azithromycin|ibuprofen|drug|medicine|dosage|खुराक|adme|pharmacokinetics|cold chain|vaccine|टीका|dawa|दवा|दवाई|dawai|tablet|goli|गोली)(?:$|[^\w\u0900-\u097F\u0A00-\u0A7F])', lower):
        return "pharmaceutical"

    # 11. Biology & Life Sciences
    if re.search(r'(?:^|[^\w\u0900-\u097F\u0A00-\u0A7F])(photosynthesis|प्रकाश संश्लेषण|calvin cycle|c3|c4|cam|chlorophyll|क्लोरोफिल|rubisco|nitrogen cycle|नाइट्रोजन चक्र|rhizobium|राइजोबियम|azotobacter|trichoderma|ट्राइकोडर्मा|dna|rna|genetics|आनुवंशिकी|transcription|translation|central dogma|mitochondria|biology|बायोलॉजी|जीव विज्ञान)(?:$|[^\w\u0900-\u097F\u0A00-\u0A7F])', lower):
        return "biology"

    # 12. Tech & Hardware / IoT / Embedded
    if re.search(r'(?:^|[^\w\u0900-\u097F\u0A00-\u0A7F])(arduino|आर्डुइनो|esp32|ईएसपी32|flame sensor|relay|रिले|soil moisture|ultrasonic|raspberry pi|iot|आईओटी|microcontroller|gpio|sensor|सेंसर|motor driver|l298n|dht11|dht22|oled|oled display)(?:$|[^\w\u0900-\u097F\u0A00-\u0A7F])', lower):
        return "tech_hardware"

    # 13. Programming & Software
    if re.search(r'(?:^|[^\w\u0900-\u097F\u0A00-\u0A7F])(python|पायथन|fastapi|javascript|जावास्क्रिप्ट|sql|c\+\+|coding|कोडिंग|function|class|algorithm|code|compile|bug|script|api|database|डेटाबेस|git|async|fetch|readablestream)(?:$|[^\w\u0900-\u097F\u0A00-\u0A7F])', lower):
        return "coding_technical"

    # 14. Greeting & Casual Chit-Chat
    if re.search(r'(?:^|[^\w\u0900-\u097F\u0A00-\u0A7F])(hi|hello|hey|namaste|नमस्ते|pranam|प्रणाम|kya\s+h[a]*l|kaise\s+ho|कैसे\s+हो|kese\s+ho|kiddan|ਕਿੱਦਾਂ|who\s+are\s+you|bhai|भाई|भैया|yaar|ताऊ|काका|ram\s+ram|राम\s+राम|sat\s+sri\s+akal|ਸਤਿ\s+ਸ਼੍ਰੀ\s+ਅਕਾਲ|good\s+morning|good\s+evening|kya\s+chal\s+raha|sab\s+badhiya|kem\s+cho|kasa\s+kay|kaisa\s+hai)(?:$|[^\w\u0900-\u097F\u0A00-\u0A7F])', lower):
        return "greeting"

    return "general_discussion"
