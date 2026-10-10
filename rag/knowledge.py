"""
GramSetu AI - Comprehensive Multidisciplinary Knowledge & Offline RAG Engine
Auto-trained & synced via rag/train_ingest.py
"""

import re

KNOWLEDGE_BASE = [
    {
        "id": "agri_wheat_cultivation",
        "category": "agriculture",
        "title": "Complete Step-by-Step Wheat Cultivation Guide (\u0917\u0947\u0939\u0942\u0902 \u0915\u0940 \u0916\u0947\u0924\u0940)",
        "keywords": ["wheat", "gehu", "gehun", "cultivation", "farming", "sowing", "kheti", "bona", "seed rate", "beej", "गेहूं की खेती", "बीज दर", "खाद", "सिंचाई", "wheat cultivation"],
        "summary": "Wheat sowing Nov 1-20, seed rate 40-45 kg/acre, 1 bag DAP + 2 bags Urea/acre, 6 critical irrigations.",
        "response": "🌾 **Wheat Cultivation & Seed Rate Scientific Guide (गेहूं की खेती):**\n\n1. **Seed Rate (प्रति एकड़ बीज दर):**\n   • **Timely Sowing (समय पर बुवाई - 1 से 20 नवंबर):** **40 से 45 किलोग्राम प्रति एकड़** (HD-2967, DBW-187, DBW-222, PBW-550)।\n   • **Late Sowing (पछेती बुवाई - दिसंबर):** 50 से 55 किलोग्राम प्रति एकड़ (20% अधिक बीज)।\n2. **Fertilizer Schedule (प्रति एकड़ खाद):**\n   • **Basal (बुवाई के समय):** 1 बैग DAP (50kg) + 1 बैग MOP पोटाश (25-30kg) + 10kg जिंक सल्फेट (33%)।\n   • **First Top Dressing (21 दिन - CRI स्टेज):** 1 बैग यूरिया (45kg)।\n   • **Second Top Dressing (45-50 दिन):** 1 बैग यूरिया (45kg)।\n3. **Critical Irrigations (सिंचाई के मुख्य चरण):**\n   • पहली सिंचाई: 20-25 दिन पर (CRI स्टेज - मुकुट जड़ अवस्था, अत्यंत महत्वपूर्ण)।\n   • दूसरी सिंचाई: 40-45 दिन (कल्ले फूटते समय)।\n   • तीसरी सिंचाई: 65-70 दिन (गाभा अवस्था / बूटिंग)।\n   • चौथी सिंचाई: 90-95 दिन (फूल आने पर)।\n   • पांचवीं सिंचाई: 105-110 दिन (दूधिया अवस्था / दाना भराव)।"
    },
    {
        "id": "agri_wheat_yellow_rust",
        "category": "agriculture",
        "title": "Wheat Yellow Rust Disease Control (\u0917\u0947\u0939\u0942\u0902 \u092e\u0947\u0902 \u092a\u0940\u0932\u093e \u0930\u0924\u0941\u0906 \u0930\u094b\u0915\u0925\u093e\u092e)",
        "keywords": ["yellow rust", "peela ratua", "rust", "fungus", "haldi rog", "wheat disease", "propiconazole", "tilt", "पीला रतुआ", "गेहूं", "हल्दी रोग"],
        "summary": "Yellow powder on leaves. Spray Propiconazole 25% EC (Tilt) @ 200ml in 200L water per acre.",
        "response": "🌾 **Wheat Yellow Rust / Peela Ratua Cure (पीला रतुआ रोकथाम):**\n\n1. **लक्षण:** पत्तियों पर पीले रंग की हल्दी जैसी धारियां या पाउडर दिखाई देना जो छूने पर उंगलियों पर लग जाता है।\n2. **रासायनिक उपचार (Chemical Spray):**\n   • **प्रोपिकोनाज़ोल 25% EC (Propiconazole - Tilt / Bumper):** **200 मिली प्रति एकड़** को 200 लीटर पानी में मिलाकर साफ मौसम में स्प्रे करें।\n   • यदि प्रकोप अधिक हो तो 12-15 दिन बाद दूसरा छिड़काव करें (**Tebuconazole 25.9% EC @ 200ml/acre**)।\n3. **सावधानी:** रोगग्रस्त खेत में नाइट्रोजन (यूरिया) का अतिरिक्त छिड़काव न करें, इससे फंगस तेजी से फैलती है।"
    },
    {
        "id": "agri_paddy_cultivation",
        "category": "agriculture",
        "title": "Paddy/Rice Cultivation & Transplanting Guide (\u0927\u093e\u0928 \u0915\u0940 \u0916\u0947\u0924\u0940)",
        "keywords": ["paddy", "rice", "dhan", "chawal", "transplanting", "nursery", "dhan ki kheti", "धान", "चावल", "रोपाई"],
        "summary": "Nursery May 20-June 20, seed rate 5-6 kg/acre hybrid, 1 bag DAP + 1 bag Potash + 2 bags Urea.",
        "response": "🌾 **Paddy/Rice Cultivation Guide (धान की वैज्ञानिक खेती):**\n\n1. **Seed Rate (बीज दर प्रति एकड़):**\n   • **Hybrid धान:** **5 से 6 किलोग्राम** प्रति एकड़।\n   • **बासमती व देसी किस्में:** 10 से 12 किलोग्राम प्रति एकड़।\n2. **पौध तैयार करना (Nursery):**\n   • बुवाई समय: 20 मई से 20 जून। 20-25 दिन पुरानी पौध ही रोपाई हेतु सर्वोत्तम होती है।\n3. **उर्वरक प्रबंधन (Fertilizers per Acre):**\n   • **रोपाई पूर्व (लेव लगाते समय):** 1 बैग DAP (50kg) + 30kg MOP पोटाश + 10kg जिंक सल्फेट (33%)।\n   • **यूरिया:** कुल 70-80kg यूरिया को 3 भागों में दें (रोपाई के 7 दिन, 21 दिन और 42 दिन पर)।\n4. **खरपतवार नियंत्रण:** रोपाई के 2-3 दिन के अंदर **Pretilachlor 50% EC @ 500ml प्रति एकड़** खड़े पानी में छिड़कें।"
    },
    {
        "id": "agri_mustard_cultivation",
        "category": "agriculture",
        "title": "Mustard Cultivation & Sulphur Dosage Guide (\u0938\u0930\u0938\u094b\u0902 \u0915\u0940 \u0916\u0947\u0924\u0940)",
        "keywords": ["mustard", "sarson", "oilseed", "sarson seed rate", "beej", "sulphur", "सरसों", "सरसो", "माहू", "चेपा"],
        "summary": "Sowing Oct 1-25, seed rate 1.5-2 kg/acre, 10kg Sulphur mandatory for oil content.",
        "response": "🌼 **Mustard Cultivation Guide (सरसों की उन्नत खेती):**\n\n1. **बुवाई समय:** 1 से 25 अक्टूबर (सर्वोत्तम तापमान 25-28°C)।\n2. **Seed Rate (बीज दर):** **1.5 से 2.0 किलोग्राम प्रति एकड़** (कतार से कतार दूरी 30 सेमी, पौधे से पौधा 10-12 सेमी)।\n3. **उर्वरक प्रबंधन (प्रति एकड़):**\n   • 1 बैग SSP (सिंगल सुपर फॉस्फेट 50kg) + 35kg यूरिया + **10kg बेंटोनाइट सल्फर 90%** (तेल की मात्रा 40%+ करने हेतु अनिवार्य)।\n4. **माहू / एफिड (Aphid/Chepa) कीट रोकथाम:**\n   • फूल आने के बाद माहू दिखने पर **Dimethoate 30% EC (Rogor) @ 250ml** या **Thiamethoxam 25% WG @ 80g** प्रति एकड़ स्प्रे करें।"
    },
    {
        "id": "agri_cotton_pest_control",
        "category": "agriculture",
        "title": "Cotton Pink Bollworm & Whitefly Management (\u0915\u092a\u093e\u0938 \u092e\u0947\u0902 \u0917\u0941\u0932\u093e\u092c\u0940 \u0938\u0941\u0902\u0921\u0940 \u0935 \u0938\u092b\u0947\u0926 \u092e\u0915\u094d\u0916\u0940)",
        "keywords": ["cotton", "kapas", "pink bollworm", "gulabi sundi", "whitefly", "safed makkhi"],
        "summary": "Pheromone traps for pink bollworm. Spray Emamectin Benzoate 5% SG @ 100g/acre for bollworm, Diafenthiuron 50% WP for whitefly.",
        "response": "🌿 **Cotton Pest & Disease Management (कपास कीट नियंत्रण):**\n\n1. **गुलाबी सुंडी (Pink Bollworm):**\n   • प्रति एकड़ 5-8 फेरोमोन ट्रैप (Pheromone Traps) लगाएं।\n   • प्रकोप होने पर **Emamectin Benzoate 5% SG @ 100 ग्राम प्रति एकड़** या **Profenofos 50% EC @ 400 मिली** स्प्रे करें।\n2. **सफेद मक्खी (Whitefly):**\n   • **Diafenthiuron 50% WP (Pegasus) @ 250 ग्राम** या **Pyriproxyfen 10% EC @ 400 मिली** प्रति 200 लीटर पानी में छिड़कें।\n3. **सावधानी:** एक ही कीटनाशक का बार-बार छिड़काव न करें, दवाएं बदल-बदल कर स्प्रे करें।"
    },
    {
        "id": "agri_soil_npk_ph",
        "category": "agriculture",
        "title": "Soil Health, pH Testing & NPK Management (\u092e\u093f\u091f\u094d\u091f\u0940 \u091c\u093e\u0902\u091a \u0935 NPK \u092a\u094d\u0930\u092c\u0902\u0927\u0928)",
        "keywords": ["soil", "mitti", "npk", "ph", "soil testing", "acidic soil", "alkaline soil", "gypsum", "chuna"],
        "summary": "Ideal soil pH is 6.5-7.5. Use Gypsum for alkaline soil (pH > 8.5) and Agricultural Lime for acidic soil (pH < 6.0).",
        "response": "🌱 **Soil Health & pH Management Guide (मिट्टी सुधार व NPK संतुलन):**\n\n1. **आदर्श मिट्टी pH मान:** **6.5 से 7.5** (पौधों द्वारा पोषक तत्व अवशोषण के लिए सर्वोत्तम)।\n2. **pH सुधार के उपाय:**\n   • **क्षारीय / कल्लर मिट्टी (Alkaline pH > 8.5):** **जिप्सम (Gypsum)** 2-3 क्विंटल प्रति एकड़ खेत में मिलाकर गहरी जुताई करें।\n   • **अम्लीय मिट्टी (Acidic pH < 6.0):** **कृषि चूना (Agricultural Lime)** 1-2 क्विंटल प्रति एकड़ डालें।\n3. **NPK आदर्श अनुपात:**\n   • अनाज वाली फसलें (गेहूं/धान): **4:2:1** (नाइट्रोजन : फॉस्फोरस : पोटाश)।\n   • दलहनी फसलें (चना/मूंग): **1:2:1** (दलहन में नाइट्रोजन कम और फॉस्फोरस अधिक चाहिए)।"
    },
    {
        "id": "tech_arduino_flame_relay",
        "category": "tech_hardware",
        "title": "Arduino Flame Sensor & Relay Control Module Interfacing",
        "keywords": ["arduino", "flame sensor", "relay", "fire alarm", "relay module", "fire detection", "arduino code"],
        "summary": "Flame sensor digital out connected to Pin 2, Relay input to Pin 8. Active LOW relay activates on fire detection.",
        "response": "⚡ **Arduino Flame Sensor with Relay Interfacing Guide:**\n\n1. **Circuit Connections (पिन कनेक्शन):**\n   • **Flame Sensor:** VCC ➔ 5V, GND ➔ GND, D0 (Digital Out) ➔ Arduino Pin 2.\n   • **Relay Module:** VCC ➔ 5V, GND ➔ GND, IN1 ➔ Arduino Pin 8.\n2. **Production Arduino C++ Code:**\n```cpp\nconst int flamePin = 2;\nconst int relayPin = 8;\n\nvoid setup() {\n  pinMode(flamePin, INPUT);\n  pinMode(relayPin, OUTPUT);\n  digitalWrite(relayPin, HIGH); // Relay OFF (Active LOW)\n  Serial.begin(9600);\n}\n\nvoid loop() {\n  int fireDetected = digitalRead(flamePin);\n  if (fireDetected == LOW) { // Flame sensor outputs LOW on fire\n    digitalWrite(relayPin, LOW); // Turn Relay ON (Buzzer/Pump)\n    Serial.println(\"🚨 WARNING: Fire Detected!\");\n  } else {\n    digitalWrite(relayPin, HIGH); // Turn Relay OFF\n  }\n  delay(100);\n}\n```\n3. **Hardware Note:** Active-LOW Relays turn ON when pin is driven `LOW`."
    },
    {
        "id": "tech_esp32_iot_wifi",
        "category": "tech_hardware",
        "title": "ESP32 Wi-Fi Station & Web Server / MQTT Gateway Setup",
        "keywords": ["esp32", "wifi", "iot", "nodemcu", "mqtt", "web server", "esp32 code"],
        "summary": "ESP32 dual-core 240MHz microcontroller with built-in 2.4GHz Wi-Fi and BLE 4.2. Connect via WiFi.h.",
        "response": "📡 **ESP32 Wi-Fi & IoT Gateway Setup Guide:**\n\n1. **Specifications:** Dual-core Xtensa 32-bit LX6 @ 240 MHz, 520 KB SRAM, built-in 802.11 b/g/n Wi-Fi & Bluetooth 4.2 BR/EDR/BLE.\n2. **Wi-Fi Station Connection Code (Arduino IDE):**\n```cpp\n#include <WiFi.h>\n\nconst char* ssid = \"Your_SSID\";\nconst char* password = \"Your_PASSWORD\";\n\nvoid setup() {\n  Serial.begin(115200);\n  WiFi.mode(WIFI_STA);\n  WiFi.begin(ssid, password);\n  Serial.print(\"Connecting to WiFi\");\n  while (WiFi.status() != WL_CONNECTED) {\n    delay(500);\n    Serial.print(\".\");\n  }\n  Serial.println(\"\\nConnected!\");\n  Serial.print(\"ESP32 IP Address: \");\n  Serial.println(WiFi.localIP());\n}\n\nvoid loop() {}\n```\n3. **Operating Voltage:** 3.3V logic level (DO NOT feed 5V into GPIO pins directly)."
    },
    {
        "id": "tech_soil_moisture_sensor",
        "category": "tech_hardware",
        "title": "Capacitive vs Resistive Soil Moisture Sensor Interfacing",
        "keywords": ["soil moisture sensor", "capacitive", "resistive", "drip automation", "irrigation sensor"],
        "summary": "Capacitive v1.2 is corrosion-free. Reads analog voltage (3.3V-5V) inversely proportional to moisture.",
        "response": "🌾 **Soil Moisture Sensor Interfacing & Auto-Irrigation:**\n\n1. **Sensor Types:**\n   • **Capacitive Moisture Sensor (v1.2 - Recommended):** No exposed metal traces; zero corrosion from electrolysis; long lifespan.\n   • **Resistive Moisture Sensor:** Corrodes rapidly in wet soil within weeks due to DC current.\n2. **Calibration Values (10-bit ADC 0-1023):**\n   • Dry Air (0% Moisture): ~520 - 580 Analog Value.\n   • Wet Saturated Soil (100% Moisture): ~260 - 300 Analog Value.\n3. **Auto-Irrigation Logic:** When ADC > 450 (Dry), trigger relay for solenoid valve/water pump."
    },
    {
        "id": "prog_python_fastapi_sqlite",
        "category": "coding_technical",
        "title": "Python REST API Development with FastAPI & SQLite",
        "keywords": ["python", "fastapi", "sqlite", "rest api", "backend", "endpoint", "pydantic"],
        "summary": "Asynchronous high-performance REST APIs with automatic OpenAPI/Swagger docs using FastAPI and SQLite.",
        "response": "🐍 **Python FastAPI & SQLite Production Template:**\n\n```python\nfrom fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\nimport sqlite3\n\napp = FastAPI(title=\"GramSetu API\")\n\nclass Item(BaseModel):\n    name: str\n    quantity: float\n\ndef get_db():\n    conn = sqlite3.connect(\"app.db\")\n    conn.row_factory = sqlite3.Row\n    return conn\n\n@app.post(\"/items\")\ndef create_item(item: Item):\n    conn = get_db()\n    cursor = conn.cursor()\n    cursor.execute(\"INSERT INTO items (name, qty) VALUES (?, ?)\", (item.name, item.quantity))\n    conn.commit()\n    item_id = cursor.lastrowid\n    conn.close()\n    return {\"id\": item_id, \"status\": \"created\"}\n```\n• **Run Server:** `uvicorn main:app --reload --port 8000`"
    },
    {
        "id": "prog_javascript_fetch_streaming",
        "category": "coding_technical",
        "title": "JavaScript Async/Await & ReadableStream Real-Time Streaming",
        "keywords": ["javascript", "fetch api", "readablestream", "ndjson", "streaming", "async await"],
        "summary": "Consuming NDJSON or token streams using fetch() and response.body.getReader() TextDecoder.",
        "response": "⚡ **JavaScript Real-Time Chunked Stream Consumer:**\n\n```javascript\nasync function streamAgentResponse(prompt) {\n  const response = await fetch('/api/chat', {\n    method: 'POST',\n    headers: { 'Content-Type': 'application/json' },\n    body: JSON.stringify({ prompt })\n  });\n\n  const reader = response.body.getReader();\n  const decoder = new TextDecoder('utf-8');\n  let buffer = '';\n\n  while (true) {\n    const { done, value } = await reader.read();\n    if (done) break;\n    buffer += decoder.decode(value, { stream: true });\n    const lines = buffer.split('\\n');\n    buffer = lines.pop(); // Retain incomplete chunk\n\n    for (const line of lines) {\n      if (!line.trim()) continue;\n      const packet = JSON.parse(line);\n      if (packet.type === 'token') {\n        document.getElementById('output').innerText += packet.token;\n      }\n    }\n  }\n}\n```"
    },
    {
        "id": "bio_photosynthesis_cycles",
        "category": "biology",
        "title": "Photosynthesis: Light Reaction, Calvin Cycle & C3/C4/CAM Pathways",
        "keywords": ["photosynthesis", "calvin cycle", "c3", "c4", "cam", "chlorophyll", "rubisco", "light reaction", "biology"],
        "summary": "6CO2 + 6H2O + Light -> C6H12O6 + 6O2. C3 (Wheat/Rice), C4 (Maize/Sugarcane via PEP Carboxylase), CAM (Cactus/Pineapple).",
        "response": "🔬 **Photosynthesis & Biochemical Carbon Fixation Pathways:**\n\n1. **Master Chemical Equation:**\n   $$6CO_2 + 6H_2O + \\text{Photons} \\xrightarrow{\\text{Chlorophyll}} C_6H_{12}O_6 + 6O_2$$\n\n2. **Light-Dependent Reactions (Thylakoid Membrane):**\n   • Photolysis of water ($2H_2O \\to 4H^+ + 4e^- + O_2$).\n   • Generates chemical energy: **ATP** and **NADPH**.\n\n3. **Dark Reaction / Calvin Cycle (Stroma):**\n   • **Enzyme:** **RuBisCO** (Ribulose-1,5-bisphosphate carboxylase-oxygenase).\n   • Converts $CO_2$ into 3-PGA, then reduces to G3P sugars.\n\n4. **Comparative Pathways:**\n   • **C3 Plants (Wheat, Rice, Soybean):** First product is 3-PGA (3 Carbon). Subject to photorespiration under high heat.\n   • **C4 Plants (Maize, Sugarcane):** Krantz anatomy; fixes $CO_2$ via **PEP Carboxylase** into Oxaloacetate (4 Carbon); high water/temp efficiency.\n   • **CAM Plants (Pineapple, Agave):** Stomata open only at night to conserve water in arid zones."
    },
    {
        "id": "bio_nitrogen_cycle_microbes",
        "category": "biology",
        "title": "Biological Nitrogen Cycle & Bio-fertilizer Microorganisms",
        "keywords": ["nitrogen cycle", "rhizobium", "azotobacter", "trichoderma", "biofertilizer", "nitrification", "denitrification"],
        "summary": "Biological nitrogen fixation via Rhizobium (symbiotic) and Azotobacter (free-living). Nitrosomonas -> Nitrobacter.",
        "response": "🌱 **Biological Nitrogen Cycle & Beneficial Microorganisms:**\n\n1. **Nitrogen Fixation Process:**\n   • **Symbiotic Fixation:** **Rhizobium** bacteria form root nodules in leguminous crops (Gram, Moong, Pea) fixing 50-100 kg N/ha.\n   • **Free-Living Fixation:** **Azotobacter** (in non-legumes like Wheat/Maize) and **Azospirillum** (in Grasses/Paddy).\n2. **Nitrification Stages:**\n   • **Step 1:** Ammonia ($NH_3$) $\\to$ Nitrite ($NO_2^-$) via *Nitrosomonas* bacteria.\n   • **Step 2:** Nitrite ($NO_2^-$) $\\to$ Nitrate ($NO_3^-$) via *Nitrobacter* bacteria (Plant usable form).\n3. **Bio-Control Agents:**\n   • **Trichoderma viride / harzianum:** Beneficial fungus protecting against root rot, wilts, and damping off."
    },
    {
        "id": "bio_dna_rna_genetics",
        "category": "biology",
        "title": "Molecular Genetics: DNA Structure, RNA & Central Dogma",
        "keywords": ["dna", "rna", "genetics", "transcription", "translation", "central dogma", "replication", "mutation"],
        "summary": "DNA double helix (Watson-Crick). Central Dogma: DNA -> (Transcription) -> mRNA -> (Translation) -> Protein.",
        "response": "🧬 **Molecular Biology & Genetics (The Central Dogma):**\n\n1. **DNA Structure (Deoxyribonucleic Acid):**\n   • Double helix with antiparallel sugar-phosphate backbone (5' to 3' and 3' to 5').\n   • **Base Pairing (Chargaff's Rules):** Adenine (A) = Thymine (T) [2 Hydrogen bonds]; Guanine (G) $\\equiv$ Cytosine (C) [3 Hydrogen bonds].\n2. **The Central Dogma of Molecular Biology:**\n   $$\\text{DNA} \\xrightarrow{\\text{Replication}} \\text{DNA} \\xrightarrow{\\text{Transcription (RNA Polymerase)}} \\text{mRNA} \\xrightarrow{\\text{Translation (Ribosomes)}} \\text{Functional Protein}$$\n3. **Key Differences (DNA vs RNA):**\n   • DNA contains Deoxyribose sugar + Thymine (T).\n   • RNA contains Ribose sugar + Uracil (U) in place of Thymine."
    },
    {
        "id": "pharma_drug_classifications",
        "category": "pharmaceutical",
        "title": "Major Pharmaceutical Drug Classes & Mechanisms of Action",
        "keywords": ["pharmaceutical", "drug class", "antibiotics", "nsaids", "antipyretic", "antihistamine", "ppi", "paracetamol", "amoxicillin"],
        "summary": "Core drug categories: Antibiotics (Amoxicillin), NSAIDs (Ibuprofen), Antipyretics (Paracetamol), PPIs (Omeprazole), Antihistamines (Cetirizine).",
        "response": "💊 **Essential Pharmaceutical Drug Classifications:**\n\n1. **Antipyretics & Analgesics (बुखार व दर्द निवारक):**\n   • **Paracetamol / Acetaminophen (500mg/650mg):** Inhibits central prostaglandin synthesis; antipyretic & mild analgesic. Safe in therapeutic doses (Max 4g/day for adults).\n2. **NSAIDs (Non-Steroidal Anti-Inflammatory Drugs):**\n   • **Ibuprofen, Diclofenac, Aceclofenac:** Inhibit COX-1 and COX-2 enzymes to reduce swelling & severe pain. *Caution: Avoid in active peptic ulcers or severe kidney disease.*\n3. **Antibiotics (जीवाणुरोधी):**\n   • **Beta-Lactams (Amoxicillin + Clavulanic Acid):** Inhibits bacterial cell wall synthesis.\n   • **Macrolides (Azithromycin):** Inhibits 50S ribosomal protein synthesis. *Take exact prescribed full course to prevent antimicrobial resistance (AMR).*\n4. **Proton Pump Inhibitors (PPIs - एसिडिटी/गैस):**\n   • **Omeprazole, Pantoprazole (40mg), Rabeprazole:** Irreversibly blocks the $H^+/K^+$ ATPase pump in gastric parietal cells. *Best taken 30-60 mins before morning breakfast.*"
    },
    {
        "id": "pharma_pharmacokinetics_adme",
        "category": "pharmaceutical",
        "title": "Pharmacokinetics (ADME) & Drug Half-Life Principles",
        "keywords": ["pharmacokinetics", "adme", "bioavailability", "half-life", "drug metabolism", "cytochrome p450", "renal clearance"],
        "summary": "ADME: Absorption (bioavailability), Distribution (plasma protein binding), Metabolism (Liver CYP450), Excretion (Kidneys).",
        "response": "🔬 **Pharmacokinetics Fundamentals (ADME Principles):**\n\n1. **Absorption (अवशोषण):**\n   • Movement of drug from site of administration into systemic circulation.\n   • **Bioavailability ($F$):** Fraction of unchanged drug reaching systemic circulation (IV = 100%, Oral = variable due to first-pass metabolism).\n2. **Distribution (वितरण):**\n   • Reversible transfer between blood and extravascular tissues. Governed by plasma protein (Albumin) binding and lipid solubility.\n3. **Metabolism / Biotransformation (मेटाबॉलिज्म):**\n   • Primary site: **Liver** via **Cytochrome P450 (CYP450)** enzyme family (Phase I: Oxidation/Reduction; Phase II: Conjugation).\n4. **Excretion / Elimination (उत्सर्जन):**\n   • Primary route: **Renal (Kidneys)** via glomerular filtration and active tubular secretion.\n   • **Half-life ($t_{1/2}$):** Time required for serum drug concentration to decrease by 50%."
    },
    {
        "id": "pharma_cold_chain_storage",
        "category": "pharmaceutical",
        "title": "Pharmaceutical Cold Chain & Medicine Storage Standards",
        "keywords": ["cold chain", "medicine storage", "vaccine storage", "temperature", "2-8 degree", "pharmacy standards"],
        "summary": "Vaccines & biologicals require 2°C to 8°C. Room temperature drugs 15°C to 25°C. Protect from direct sunlight and humidity.",
        "response": "❄️ **Pharmaceutical Storage & Cold Chain Management:**\n\n1. **Cold Storage (2°C to 8°C - Never Freeze):**\n   • Vaccines (TT, Rabies, Hepatitis, Polio, COVID-19).\n   • Insulin vials/pens, Monoclonal Antibodies, and Tetanus Toxoid.\n2. **Controlled Room Temperature (15°C to 25°C):**\n   • Tablets, capsules, dry syrups, and standard ointments.\n3. **Critical Pharmacy Directives:**\n   • Keep medicines away from direct sunlight, moisture, and high heat.\n   • Once reconstituted, oral antibiotic suspensions (e.g. Amoxicillin dry syrup) must be stored in refrigerator and discarded after 7 days."
    },
    {
        "id": "med_cpr_protocol",
        "category": "medical",
        "title": "Emergency CPR (Cardiopulmonary Resuscitation) Protocol (AHA Guidelines)",
        "keywords": ["cpr", "cardiac arrest", "heart attack", "cpr kaise de", "unconscious", "chest compression", "first aid"],
        "summary": "Check responsiveness, call 108, start high-quality chest compressions: 100-120 bpm, 2 inches deep, 30 compressions : 2 rescue breaths.",
        "response": "🚨 **Cardiopulmonary Resuscitation (CPR) Emergency Life-Saving Protocol:**\n\n1. **Immediate Assessment (C-A-B Steps):**\n   • **Step 1 - Check Safety & Response:** Tap shoulders firmly: *\"Are you okay?\"* Check carotid pulse & normal breathing (max 10 seconds).\n   • **Step 2 - Call Emergency:** Shout for help and dial **108 (Ambulance) / 112** immediately. Ask for an **AED (Defibrillator)**.\n2. **High-Quality Chest Compressions:**\n   • Place heel of one hand in the **center of chest** (lower half of sternum); interlock other hand on top.\n   • **Depth:** Press down **2 to 2.4 inches (5 to 6 cm)** deep.\n   • **Rate:** **100 to 120 compressions per minute** (to the beat of *\"Stayin' Alive\"*).\n   • Allow complete chest recoil between compressions; do not lean on chest.\n3. **Compression to Breath Ratio:**\n   • **30 Chest Compressions : 2 Rescue Breaths** (or continuous Hands-Only CPR if untrained).\n   • Continue without interruption until medical emergency team arrives or patient regains consciousness."
    },
    {
        "id": "med_bleeding_hemorrhage_control",
        "category": "medical",
        "title": "Severe Bleeding & Hemorrhage Control Protocol",
        "keywords": ["bleeding", "khoon", "hemorrhage", "cut", "wound", "direct pressure", "tourniquet"],
        "summary": "Apply firm direct pressure with clean gauze/cloth for 5-10 minutes without lifting. Elevate limb. Use tourniquet only for life-threatening arterial limb bleeding.",
        "response": "🩸 **Severe Bleeding Control & Wound First-Aid:**\n\n1. **Direct Pressure (प्राथमिक उपाय):**\n   • Place clean sterile gauze, cloth, or towel directly over the bleeding wound.\n   • Apply **firm, continuous direct pressure** with both hands for at least **5 to 10 minutes** without lifting to check.\n2. **Elevation:** Elevate the injured limb above heart level if no fracture is suspected.\n3. **Pressure Bandage:** Wrap elastic bandage firmly over dressing (ensure fingers/toes don't turn blue or cold).\n4. **Arterial Bleeding (Pumping Bright Red Blood):**\n   • If direct pressure fails on limbs, apply a commercial **Tourniquet** 2-3 inches above the wound (never over a joint). Note exact application time and rush to trauma center."
    },
    {
        "id": "med_burn_management",
        "category": "medical",
        "title": "Burn Injury Emergency Management & Treatment (\u091c\u0932\u0928\u0947 \u092a\u0930 \u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915 \u0909\u092a\u091a\u093e\u0930)",
        "keywords": ["burn", "jalna", "scald", "fire burn", "burn first aid", "blisters", "silver sulfadiazine"],
        "summary": "Cool with running tap water for 15-20 mins (NO ice, NO toothpaste). Cover with sterile non-stick dressing. Apply Silver Sulfadiazine cream.",
        "response": "🔥 **Emergency Burn Management Protocol (आग या गर्म तरल से जलने पर):**\n\n1. **तुरंत क्या करें (DOs):**\n   • **Cool Running Water:** जले हुए हिस्से पर तुरंत **15 से 20 मिनट तक सामान्य नल का बहता ठंडा पानी** डालें (दर्द और ऊतक क्षति तुरंत रुकती है)।\n   • अंगूठी, घड़ी, तंग कपड़े सूजन आने से पहले तुरंत उतार लें।\n   • **दवा:** **सिल्वर सल्फाडियाज़ीन (Silver Sulfadiazine 1% / Burnol)** क्रीम धीरे से लगाएं।\n   • साफ, सूखे, नॉन-स्टिक स्टेराइल कपड़े से ढंकें।\n2. **क्या बिल्कुल न करें (DON'Ts):**\n   • ❌ **बर्फ (Ice) कभी न लगाएं** (इससे फ्रॉस्टबाइट और ऊतक नष्ट होते हैं)।\n   • ❌ **टूथपेस्ट, हल्दी, तेल, या गोबर कभी न लगाएं** (गंभीर सेप्सिस/इन्फेक्शन का खतरा)।\n   • ❌ फफोले (Blisters) को कभी न फोड़ें।\n3. **अस्पताल कब ले जाएं:** यदि चेहरा, हाथ, जननांग जले हों या जलने का क्षेत्रफल हथेली से बड़ा हो तो तुरंत डॉक्टर के पास जाएं।"
    },
    {
        "id": "med_clinical_vital_signs",
        "category": "medical",
        "title": "Standard Clinical Vital Signs & Normal Diagnostic Ranges",
        "keywords": ["vital signs", "blood pressure", "bp", "pulse rate", "heart rate", "spo2", "temperature", "normal sugar"],
        "summary": "Normal Vitals: BP 120/80 mmHg, Pulse 60-100 bpm, SpO2 95-100%, Temp 98.6°F (37°C), Fasting Sugar 70-100 mg/dL.",
        "response": "🩺 **Standard Clinical Vital Signs & Normal Adult Diagnostic Ranges:**\n\n1. **Blood Pressure (रक्तचाप):**\n   • **Normal (सामान्य):** **120/80 mmHg** (Systolic < 120 and Diastolic < 80).\n   • **Hypertension Stage 1 (उच्च रक्तचाप):** 130-139 / 80-89 mmHg.\n   • **Hypertensive Crisis (आपातकाल):** > 180 / > 120 mmHg (Seek immediate medical care).\n2. **Heart Rate / Pulse (हृदय गति):** **60 से 100 धड़कन प्रति मिनट (bpm)** (Resting state).\n3. **Oxygen Saturation ($SpO_2$):** **95% से 100%** (यदि < 92% हो तो मेडिकल ऑक्सीजन सपोर्ट की आवश्यकता होती है)।\n4. **Body Temperature (शरीर का तापमान):** **97.8°F से 99.0°F (36.5°C से 37.2°C)**. बुखार $\\ge$ 100.4°F (38.0°C).\n5. **Blood Glucose (रक्त शर्करा):**\n   • **Fasting (खाली पेट):** **70 से 99 mg/dL**.\n   • **Post-Prandial (खाना खाने के 2 घंटे बाद):** **< 140 mg/dL**."
    },
    {
        "id": "scheme_pm_kisan",
        "category": "government_scheme",
        "title": "PM-Kisan Samman Nidhi Yojana (\u092a\u0940\u090f\u092e \u0915\u093f\u0938\u093e\u0928 \u092f\u094b\u091c\u0928\u093e \u20b96000)",
        "keywords": ["pm kisan", "pmkisan", "samman nidhi", "6000", "installment", "kist", "e-kyc", "ekyc"],
        "summary": "₹6,000 yearly in 3 installments of ₹2,000 directly to farmer bank accounts via DBT. e-KYC and land seeding mandatory.",
        "response": "🏛️ **PM-Kisan Samman Nidhi Scheme (पीएम-किसान सम्मान निधि):**\n\n1. **लाभ (Benefits):** ₹6,000 प्रति वर्ष (₹2,000 की 3 समान किस्तों में हर 4 महीने पर DBT द्वारा बैंक खाते में)।\n2. **अनिवार्य शर्तें (Checklist):**\n   • **Aadhaar e-KYC:** OTP या बायोमेट्रिक द्वारा पूर्ण होना आवश्यक।\n   • **Land Seeding (भूलेख अंकन):** जमीन की खतौनी पोर्टल पर सत्यापित हो।\n   • **Aadhaar-Bank Linkage:** बैंक खाते में NPCI DBT सक्रिय हो।\n3. **आधिकारिक पोर्टल व हेल्पलाइन:** `pmkisan.gov.in` | टोल फ्री: **155261 / 1800-115-526**"
    },
    {
        "id": "scheme_ayushman_bharat",
        "category": "government_scheme",
        "title": "Ayushman Bharat PM-JAY Health Card (\u0906\u092f\u0941\u0937\u094d\u092e\u093e\u0928 \u092d\u093e\u0930\u0924 \u20b95 \u0932\u093e\u0916 \u0915\u093e\u0930\u094d\u0921)",
        "keywords": ["ayushman", "pmjay", "health card", "5 lakh", "hospital", "card kaise banaye"],
        "summary": "₹5 Lakh annual free cashless health coverage per family for secondary & tertiary hospital care.",
        "response": "🩺 **Ayushman Bharat PM-JAY (आयुष्मान गोल्डन कार्ड):**\n\n1. **लाभ:** प्रति परिवार प्रति वर्ष **₹5 लाख तक का निःशुल्क कैशलेस इलाज**।\n2. **पात्रता दस्तावेज:** राशन कार्ड (SECC सूची), आधार कार्ड, और आधार से जुड़ा मोबाइल नंबर।\n3. **कार्ड कैसे बनाएं:** `beneficiary.nha.gov.in` पोर्टल या नजदीकी CSC / सरकारी अस्पताल में जाकर बनवाएं।\n4. **हेल्पलाइन:** **14555**"
    },
    {
        "id": "first_aid_snake_bite",
        "category": "first_aid",
        "title": "Emergency First Aid for Snake Bite (\u0938\u093e\u0902\u092a \u0915\u093e\u091f\u0928\u0947 \u092a\u0930 \u0906\u092a\u093e\u0924\u0915\u093e\u0932\u0940\u0928 \u0909\u092a\u091a\u093e\u0930)",
        "keywords": ["snake bite", "snake", "saanp", "katna", "poison", "anti snake venom", "asv", "सांप", "साँप", "काटना", "डसना", "जहर"],
        "summary": "Immediate immobilization, do NOT tie tourniquet or cut wound, rush to nearest civil hospital for Anti-Snake Venom (ASV).",
        "response": "🚨 **Snake Bite Emergency First-Aid Protocol (सांप काटने पर तुरंत क्या करें):**\n\n1. **क्या करें (DOs):**\n   • पीड़ित को शांत रखें और स्थिर बैठाएं/सुलाएं (दौड़ने या चलने न दें)।\n   • काटे गए अंग को हृदय के स्तर से नीचे रखें और स्प्लिंट/पट्टी से स्थिर करें।\n   • अंगूठी, कड़े, जूते तुरंत उतार दें।\n   • **बिना 1 मिनट गंवाए सीधे निकटतम सरकारी/सिविल अस्पताल ले जाएं** जहां **Anti-Snake Venom (ASV)** उपलब्ध हो।\n2. **क्या बिल्कुल न करें (DON'Ts):**\n   • ❌ चीरा (cut) न लगाएं और मुंह से जहर चूसने की कोशिश न करें।\n   • ❌ कसकर टाइट रस्सी/टूर्निकेट न बांधें।\n   • ❌ झाड़-फूंक में समय बर्बाद न करें।\n3. **आपातकालीन नंबर:** **108 (एम्बुलेंस) | 112 (राष्ट्रीय आपातकाल)**"
    },
    {
        "id": "scheme_kisan_credit_card",
        "category": "government_scheme",
        "title": "Kisan Credit Card (KCC) Scheme & Low-Interest Loan (\u0915\u093f\u0938\u093e\u0928 \u0915\u094d\u0930\u0947\u0921\u093f\u091f \u0915\u093e\u0930\u094d\u0921)",
        "keywords": ["kisan credit card", "kcc", "credit card", "kisan card", "kcc loan", "byaj", "crop loan", "fasal loan", "kcc limit"],
        "summary": "KCC provides short term crop loans at effective 4% interest (7% with 3% prompt repayment subvention). Up to 1.6 lakh collateral free, up to 3 lakh total.",
        "response": "🏛️ **Kisan Credit Card (KCC) - किसान क्रेडिट कार्ड योजना:**\n\n1. **ब्याज दर व सब्सिडी (Interest Rate):**\n   • सामान्य ब्याज दर: **7% प्रति वर्ष**।\n   • **समय पर चुकाने पर (Prompt Repayment):** 3% अतिरिक्त छूट ➔ प्रभावी ब्याज दर **मात्र 4%**।\n2. **लोन लिमिट (Loan Limit):**\n   • बिना जमीन बंधक रखे (Collateral-Free): **₹1.60 लाख तक**।\n   • जमीन व फसल के आधार पर: **₹3 लाख तक**।\n3. **आवश्यक दस्तावेज:**\n   • जमीन की खतौनी (LPC/खसरा-खतौनी नकल), आधार कार्ड, पैन कार्ड, और पासपोर्ट फोटो।\n4. **आवेदन कहां करें:**\n   • अपनी नजदीकी बैंक शाखा (SBI, PNB, ग्रामीण बैंक) या CSC केंद्र पर जाकर फॉर्म भरें।"
    },
    {
        "id": "scheme_pm_fasal_bima",
        "category": "government_scheme",
        "title": "PM Fasal Bima Yojana (\u092a\u094d\u0930\u0927\u093e\u0928\u092e\u0902\u0924\u094d\u0930\u0940 \u092b\u0938\u0932 \u092c\u0940\u092e\u093e \u092f\u094b\u091c\u0928\u093e - PMFBY)",
        "keywords": ["fasal bima", "crop insurance", "pmfby", "fasal insurance", "bima yojana", "muavza", "claim", "damage", "fasal kharab"],
        "summary": "1.5% premium for Rabi crops, 2% for Kharif. 72 hours window to claim damages on portal or toll free 14447.",
        "response": "🏛️ **PM Fasal Bima Yojana (PMFBY - फसल बीमा व मुआवजा):**\n\n1. **प्रीमियम दर (किसान अंश):**\n   • **रबी फसल (गेहूं, सरसों):** मात्र **1.5%**।\n   • **खरीफ फसल (धान, कपास):** मात्र **2.0%**।\n   • बागवानी व वाणिज्यिक फसलें: **5.0%** (शेष प्रीमियम सरकार देती है)।\n2. **नुकसान कवरेज:**\n   • ओलावृष्टि, सूखा, बाढ़, बेमौसम बारिश और कटाई के 14 दिन बाद तक का नुकसान।\n3. **क्लेम रिपोर्टिंग (समय सीमा):**\n   • नुकसान होने के **72 घंटे के अंदर** शिकायत दर्ज कराना अनिवार्य है।\n4. **हेल्पलाइन व पोर्टल:**\n   • टोल-फ्री नंबर: **14447** | पोर्टल: `pmfby.gov.in` या 'Crop Insurance' मोबाइल ऐप।"
    },
    {
        "id": "scheme_pm_kusum_solar",
        "category": "government_scheme",
        "title": "PM-KUSUM Solar Agricultural Pump Scheme (\u092a\u0940\u090f\u092e-\u0915\u0941\u0938\u0941\u092e \u0938\u094b\u0932\u0930 \u092a\u0902\u092a \u092f\u094b\u091c\u0928\u093e)",
        "keywords": ["kusum", "solar pump", "solar", "pm kusum", "solar yojana", "tubewell solar", "sinchai solar", "solar subsidy"],
        "summary": "Up to 60% subsidy for solar water pumps (3HP, 5HP, 7.5HP) under PM-KUSUM. Farmers pay only 10%-40%.",
        "response": "☀️ **PM-KUSUM Solar Pump Scheme (सोलर कृषि पंप पर 60% तक सब्सिडी):**\n\n1. **सब्सिडी विवरण (Subsidy Details):**\n   • **60% सरकारी सब्सिडी** (30% केंद्र + 30% राज्य सरकार)।\n   • किसान को मात्र **10% से 40%** लागत देनी होती है (30% तक बैंक लोन उपलब्ध)।\n2. **उपलब्ध पंप क्षमता:**\n   • **3 HP, 5 HP, और 7.5 HP** के सोलर सबमर्सिबल / सरफेस पंप।\n3. **पात्रता व दस्तावेज:**\n   • जमीन की खतौनी, आधार कार्ड, बैंक पासबुक, और बोरवेल/सिंचाई जल स्रोत।\n4. **आवेदन पोर्टल:**\n   • राज्य ऊर्जा विकास एजेंसी (जैसे UPNEDA, HAREDA, RREC) या `pmkusum.mnre.gov.in`।"
    },
    {
        "id": "agri_wheat_irrigation_schedule",
        "category": "agriculture",
        "title": "Wheat Irrigation Schedule & Critical Stages (\u0917\u0947\u0939\u0942\u0902 \u092e\u0947\u0902 \u092a\u0939\u0932\u093e \u092a\u093e\u0928\u0940 \u0935 \u0938\u093f\u0902\u091a\u093e\u0908 \u0938\u092e\u092f)",
        "keywords": ["pehla pani", "wheat irrigation", "gehu me pani", "gehu sinchai", "irrigation schedule", "cri stage", "pani kab de", "sinchai kab kare"],
        "summary": "1st irrigation at 20-25 days (CRI stage), 2nd at 40-45 days (Tillering), 3rd at 65-70 days, 4th at 85-90 days, 5th at 105 days.",
        "response": "💧 **गेहूं में सिंचाई का सटीक वैज्ञानिक समय (Wheat Irrigation Schedule):**\n\n1. **पहली सिंचाई (CRI Stage - मुकुट जड़ / ताज अवस्था):**\n   • **बुवाई के 20 से 25 दिन बाद**। यह सबसे महत्वपूर्ण सिंचाई है; इसमें देरी करने पर कल्ले कम फूटते हैं और उपज 20-30% घट जाती है।\n2. **दूसरी सिंचाई (Tillering - कल्ले फूटने पर):**\n   • बुवाई के **40 से 45 दिन बाद** (साथ में 1 बैग यूरिया की टॉप ड्रेसिंग करें)।\n3. **तीसरी सिंचाई (Jointing - गांठ बनते समय):**\n   • बुवाई के **60 से 65 दिन बाद**।\n4. **चौथी सिंचाई (Booting / Flowering - फूल व बाली निकलते समय):**\n   • बुवाई के **80 से 85 दिन बाद**।\n5. **पांचवीं सिंचाई (Milking - दाना दूधिया अवस्था):**\n   • बुवाई के **100 से 105 दिन बाद**।\n   • *सावधानी: तेज हवा चलने पर पानी न लगाएं, अन्यथा फसल गिर (lodging) सकती है।*"
    },
    {
        "id": "agri_dairy_livestock_care",
        "category": "agriculture",
        "title": "Dairy Cattle Care & Milk Production Boost (\u092a\u0936\u0941\u092a\u093e\u0932\u0928 \u0935 \u0926\u0942\u0927 \u092c\u0922\u093c\u093e\u0928\u0947 \u0915\u0947 \u0935\u0948\u091c\u094d\u091e\u093e\u0928\u093f\u0915 \u0909\u092a\u093e\u092f)",
        "keywords": ["pashu", "gay", "bhains", "cow", "buffalo", "doodh", "milk", "doodh badhaye", "pashupalan", "dairy", "thanela", "mastitis", "khurpaka", "fmd"],
        "summary": "Balanced cattle feed 400g/L milk, mineral mixture 50g/day, teat dip post milking to prevent mastitis, routine deworming.",
        "response": "🐄 **दुधारू पशु प्रबंधन व दूध उत्पादन वृद्धि (Scientific Dairy Management):**\n\n1. **संतुलित आहार (Feed Management):**\n   • प्रति लीटर दूध उत्पादन पर **400 ग्राम संतुलित दाना/खली** अतिरिक्त दें।\n   • **मिनरल मिक्सचर (खनिज मिश्रण):** प्रतिदिन **50 ग्राम** चारे में अनिवार्य रूप से मिलाएं।\n   • हरा चारा (बरसीम, जई, नेपियर) + सूखा भूसा 3:1 के अनुपात में दें।\n2. **थनैला रोग (Mastitis) से बचाव:**\n   • दूध निकालने के बाद थनों को **Povidone Iodine (1%) Teat Dip** में डुबोएं।\n   • दूध निकालने के 30-45 मिनट तक पशु को बैठने न दें ताकि थन का छिद्र बंद हो सके।\n3. **कृमिनाशक (Deworming) व टीकाकरण:**\n   • हर 3-4 महीने में पेट के कीड़ों की दवा (Albendazole / Fenbendazole) दें।\n   • FMD (खुरपका-मुंहपका) व HS (गलघोंटू) का नियमित टीका लगवाएं।"
    },
    {
        "id": "medical_fever_first_aid",
        "category": "medical",
        "title": "Fever Emergency First Aid & Management (\u092c\u0941\u0916\u093e\u0930 \u0915\u093e \u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915 \u0909\u092a\u091a\u093e\u0930 \u0935 \u0926\u0947\u0916\u092d\u093e\u0932)",
        "keywords": ["bukhar", "fever", "tapman", "paracetamol", "bukhar ki dawa", "calpol", "crocin", "high fever", "sardard", "bukhar me kya kare", "बुखार", "तापमान", "पैरासिटामोल"],
        "summary": "Paracetamol 500/650mg every 6-8 hrs for adults, cold sponging on forehead with normal water, plenty of ORS/fluids. See doctor if >102°F or >3 days.",
        "response": "🌡️ **बुखार का त्वरित व सुरक्षित प्राथमिक उपचार (Fever Management):**\n\n1. **दवा (Medicine - वयस्क/Adult):**\n   • **Paracetamol (500mg या 650mg):** 6 से 8 घंटे के अंतराल पर (दिन में अधिकतम 3 से 4 ग्राम)।\n   • *सावधानी: बिना डॉक्टर के परामर्श के एस्पिरिन या अत्यधिक एंटीबायोटिक न लें।*\n2. **शारीरिक देखभाल (Physical Care):**\n   • **सामान्य पानी की पट्टी (Cold Sponging):** माथे, गर्दन और बगलों पर सादे पानी की भीगी पट्टी रखें (बर्फ का उपयोग कभी न करें)।\n   • शरीर को ढकने के लिए हल्के सूती कपड़े पहनाएं।\n3. **तरल पदार्थ (Hydration):**\n   • डिहाइड्रेशन से बचने के लिए ORS का घोल, गुनगुना पानी, दाल का पानी या नारियल पानी खूब पिलाएं।\n4. **डॉक्टर से तुरंत कब मिलें (Red Flags):**\n   • बुखार 102°F (38.9°C) से अधिक हो या 3 दिन से अधिक लगातार बना रहे।"
    },
    {
        "id": "test_organic_vermicompost",
        "category": "agriculture",
        "title": "Vermicompost (Kechua Khad) Preparation Guide",
        "keywords": ["vermicompost", "kechua khad", "kechuye", "organic fertilizer", "gobar khad"],
        "summary": "Step by step vermicompost preparation using Eisenia fetida earthworms in 45-60 days.",
        "response": "🌿 **वर्मीकम्पोस्ट (केंचुआ खाद) बनाने की वैज्ञानिक विधि:**\n1. **केंचुए की प्रजाति:** *Eisenia fetida* (लाल केंचुआ सबसे उपयुक्त)।\n2. **बेड का आकार:** 30 फीट लंबा x 3 फीट चौड़ा x 2 फीट ऊंचा।\n3. **कच्चा माल:** 70% सड़ा हुआ गोबर + 30% सूखी पत्तियां व बायोमास।\n4. **नमी व तापमान:** 30-40% नमी बनाए रखें और सीधी धूप से बचाएं।\n5. **तैयार होने का समय:** 45 से 60 दिन में चायपत्ती जैसी भुरभुरी खाद तैयार हो जाती है।"
    },
]

GENERIC_STOP_KEYWORDS = {"python", "javascript", "code", "function", "biology", "science", "medical", "drug", "medicine", "first aid", "soil", "crop", "farming"}

def search_knowledge(query: str, threshold: int = 30) -> dict:
    """
    Multidisciplinary keyword and phrase matching engine with specific term weighting.
    """
    if not query:
        return None

    clean = query.strip().lower()
    words = [w for w in re.findall(r'[a-zA-Z0-9\u0900-\u097F]+', clean) if len(w) > 2]
    if not words:
        return None

    best_item = None
    best_score = 0

    for item in KNOWLEDGE_BASE:
        score = 0
        title_lower = item.get("title", "").lower()

        # Direct phrase match in title
        if clean in title_lower:
            score += 80

        # Match keywords using exact word boundaries with full Unicode support
        for kw in item.get("keywords", []):
            kw_lower = kw.lower()
            is_generic = kw_lower in GENERIC_STOP_KEYWORDS
            
            # Full phrase match
            if len(kw_lower.split()) > 1:
                if kw_lower in clean:
                    score += 60
            else:
                # Standalone word boundary match with Unicode support
                pattern = r"(?:^|[^\w\u0900-\u097F\u0A00-\u0A7F])" + re.escape(kw_lower) + r"(?:$|[^\w\u0900-\u097F\u0A00-\u0A7F])"
                if re.search(pattern, clean) or (kw_lower in clean and len(kw_lower) >= 4):
                    score += 15 if is_generic else 45

        if score > best_score:
            best_score = score
            best_item = item

    if best_score >= threshold:
        return best_item
    return None
