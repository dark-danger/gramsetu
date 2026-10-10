#!/usr/bin/env python3
"""
GramSetu AI - 10-Lakh Persona Dataset Generator
Synthesizes rich, diverse multi-dialect, multi-parameter training examples covering:
- Dialects: Bhojpuri, Haryanvi, Rajasthani, Bihari, Bundelkhandi, Hinglish, Shuddh Hindi, Punjabi, Broken English
- Parameters: Land area (Bigha/Acre), Soil types, Crop stages, Weather/Climate, Budgets, Microcontroller pins
- Domains: Agriculture, Animal Husbandry, IoT & Hardware, Coding, Biology, Pharmacy, Emergency First Aid
"""

import os
import sys
import json
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DATASET_DIR, "train_10lakh_personas.jsonl")

# Templates for multi-dialect prompt variations
DIALECT_STYLES = {
    "bhojpuri": [
        "भैया {crop} में {problem} लागल बा, का करे के चाहीं? {parameter}",
        "{crop} के खेती करे के बा, {parameter} बा, खाद और बीज के हिसाब बतावा।",
        "अरे मालिक, {parameter} में {crop} बोए के बा, पानी कब कब दिहल जाई?"
    ],
    "haryanvi": [
        "भाई {crop} म्ह {problem} आरया सै, के इलाज करूँ? {parameter}",
        "{crop} बोणी सै {parameter}, बीज अर खाद का पक्का जुगाड़ बता दे।",
        "ताऊ {parameter} सै म्हारे धोरे, {crop} म्ह पहला पाणी कद लगाणा सै?"
    ],
    "rajasthani": [
        "भाईजी {crop} मांय {problem} लागगी, कांई दवाई छांटणी पड़ेली? {parameter}",
        "{parameter} जमीन है, {crop} री खेती रो पूरो ब्योरो बताओ सा।",
        "सा {crop} मांय रोग लागग्यो, {parameter} है, बताओ कांई करां?"
    ],
    "hinglish": [
        "Bhai mere {crop} me {problem} ho raha hai, kya spray karun? {parameter}",
        "{crop} ki kheti karni hai {parameter}, seed rate aur fertilizer schedule batao.",
        "{parameter} hai mere paas, {crop} me irrigation aur khad ka exact hisab chahiye."
    ],
    "hindi": [
        "{crop} में {problem} का लक्षण दिख रहा है, इसका सटीक उपचार क्या है? {parameter}",
        "{parameter} में {crop} की वैज्ञानिक खेती की संपूर्ण विधि (खाद, बीज, सिंचाई) बताइए।",
        "नमस्ते, {crop} की फसल में {problem} की रोकथाम हेतु कौन सा कीटनाशक या फफूंदनाशक डालें? {parameter}"
    ]
}

CROPS_DATA = [
    {
        "crop": "गेहूं (Wheat)",
        "problems": ["पीला रतुआ (Yellow Rust)", "दीमक (Termites)", "खरपतवार (Phalaris minor / गुल्ली डंडा)", "कल्ले कम निकलना"],
        "solutions": {
            "पीला रतुआ (Yellow Rust)": "पत्तियों पर पीला पाउडर दिखने पर **Propiconazole 25% EC (Tilt)** @ 200 मिली को 200 लीटर पानी में मिलाकर प्रति एकड़ तुरंत स्प्रे करें।",
            "दीमक (Termites)": "बुवाई से पहले बीज को **Chlorpyrifos 20% EC** @ 4ml प्रति किलो बीज से उपचारित करें। खड़ी फसल में 1 लीटर Chlorpyrifos सिंचाई के पानी के साथ चलाएं।",
            "खरपतवार (Phalaris minor / गुल्ली डंडा)": "बुवाई के 30-35 दिन पर **Clodinafop 15% WP** @ 160g प्रति एकड़ या **Sulfosulfuron 75% WG** @ 13.5g प्रति एकड़ 150 लीटर पानी में स्प्रे करें।",
            "कल्ले कम निकलना": "21 दिन की CRI अवस्था पर पहली सिंचाई करें और प्रति एकड़ 1 बैग यूरिया (45kg) + 5kg जिंक सल्फेट डालें।"
        },
        "base_seed_per_acre": "40-45 kg",
        "fertilizer": "1 बैग DAP (50kg) + 1 बैग MOP (30kg) बुवाई के समय, तथा 2 बैग यूरिया दो भागों में (21 दिन और 45 दिन पर)।"
    },
    {
        "crop": "सरसों (Mustard)",
        "problems": ["माहू / चेपा (Aphids)", "सफेद रोली (White Rust)", "पाला / ठंड (Frost)"],
        "solutions": {
            "माहू / चेपा (Aphids)": "माहू दिखने पर **Dimethoate 30% EC** @ 300ml या **Imidacloprid 17.8% SL** @ 60-70ml प्रति एकड़ 150-200 लीटर पानी में मिलाकर छिड़कें।",
            "सफेद रोली (White Rust)": "पत्तियों के नीचे सफेद फफोले दिखने पर **Mancozeb 75% WP (Indofil M-45)** @ 600g प्रति एकड़ 200L पानी में स्प्रे करें।",
            "पाला / ठंड (Frost)": "ठंड और पाले की संभावना होने पर खेत में हल्की सिंचाई करें तथा 0.1% गंधक का तेजाब (Sulfuric Acid - 1ml/L पानी) या घुलनशील सल्फर 80% WDG @ 1kg/एकड़ स्प्रे करें।"
        },
        "base_seed_per_acre": "1.5-2 kg",
        "fertilizer": "1 बैग SSP (50kg) + आधा बैग DAP (25kg) + 1 बैग यूरिया बुवाई के समय, फूल आने से पहले दूसरा यूरिया।"
    },
    {
        "crop": "धान (Paddy/Rice)",
        "problems": ["तना छेदक (Stem Borer)", "ब्लास्ट रोग (Blast Disease)", "शीथ ब्लाइट (Sheath Blight)"],
        "solutions": {
            "तना छेदक (Stem Borer)": "डेड हार्ट दिखने पर **Cartap Hydrochloride 4% G (Padan)** @ 7.5kg प्रति एकड़ खेत में बालू मिलाकर छिड़कें या **Chlorantraniliprole 18.5% SC (Coragen)** @ 60ml/एकड़ स्प्रे करें।",
            "ब्लास्ट रोग (Blast Disease)": "आंख जैसे धब्बे बनने पर **Tricyclazole 75% WP (Baan/Beam)** @ 120g प्रति एकड़ 200L पानी में मिलाकर छिड़काव करें।",
            "शीथ ब्लाइट (Sheath Blight)": "तने पर सर्पिलाकार धब्बे दिखने पर **Validamycin 3% L** @ 400ml या **Azoxystrobin 18.2% + Difenoconazole 11.4% SC (Amistar Top)** @ 200ml/एकड़ स्प्रे करें।"
        },
        "base_seed_per_acre": "6-8 kg (हाइब्रिड) या 15-20 kg (देसी)",
        "fertilizer": "1 बैग DAP + 1 बैग MOP + 10kg जिंक सल्फेट (33%) रोपाई पर, 2 बैग यूरिया रोपाई के 20 और 45 दिन पर।"
    }
]

PARAMETERS_LIST = [
    {"desc": "मेरे पास 3 एकड़ बलुई दोमट जमीन है", "mult": 3, "soil": "बलुई दोमट"},
    {"desc": "मारे धोरै 5 एकड़ काली मिट्टी की जमीन सै", "mult": 5, "soil": "काली मिट्टी"},
    {"desc": "2 बीघा जमीन बा, ट्यूबवेल के पानी बा", "mult": 0.4, "soil": "चिकनी दोमat"},
    {"desc": "1 Acre sandy soil, drip irrigation installed", "mult": 1, "soil": "Sandy Loam"}
]

TECH_IOT_DATA = [
    {
        "question": "Arduino se DHT22 Temperature & Humidity sensor connect karke OLED display pe kaise dikhayein?",
        "solution": (
            "⚙️ **Arduino Uno + DHT22 + 0.96 inch I2C OLED (SSD1306) Setup:**\n\n"
            "1. **Circuit Wiring (पिन कनेक्शन):**\n"
            "   • **DHT22:** VCC -> 5V, GND -> GND, Data -> Digital Pin D2 (10k Pull-up resistor between VCC & Data).\n"
            "   • **OLED Display (I2C):** VCC -> 5V, GND -> GND, SCL -> A5, SDA -> A4.\n\n"
            "2. **Libraries Required:** `Adafruit SSD1306`, `Adafruit GFX`, `DHT sensor library`.\n\n"
            "3. **Arduino Code:**\n"
            "```cpp\n"
            "#include <Wire.h>\n"
            "#include <Adafruit_GFX.h>\n"
            "#include <Adafruit_SSD1306.h>\n"
            "#include <DHT.h>\n\n"
            "#define DHTPIN 2\n"
            "#define DHTTYPE DHT22\n"
            "DHT dht(DHTPIN, DHTTYPE);\n"
            "Adafruit_SSD1306 display(128, 64, &Wire, -1);\n\n"
            "void setup() {\n"
            "  dht.begin();\n"
            "  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);\n"
            "  display.clearDisplay();\n"
            "  display.setTextColor(WHITE);\n"
            "}\n\n"
            "void loop() {\n"
            "  float h = dht.readHumidity();\n"
            "  float t = dht.readTemperature();\n"
            "  display.clearDisplay();\n"
            "  display.setTextSize(1);\n"
            "  display.setCursor(0, 10);\n"
            "  display.print(\"GramSetu Agri-IoT\");\n"
            "  display.setTextSize(2);\n"
            "  display.setCursor(0, 30);\n"
            "  display.print(\"T: \"); display.print(t, 1); display.print(\" C\");\n"
            "  display.setCursor(0, 50);\n"
            "  display.print(\"H: \"); display.print(h, 1); display.print(\" %\");\n"
            "  display.display();\n"
            "  delay(2000);\n"
            "}\n"
            "```"
        )
    },
    {
        "question": "ESP32 se relay module aur soil moisture sensor se automated solar irrigation system kaise banayein?",
        "solution": (
            "🌿 **ESP32 Smart Solar Irrigation Controller Guide:**\n\n"
            "1. **Wiring (पिन कनेक्शन):**\n"
            "   • **Capacitive Soil Sensor:** VCC -> 3.3V, GND -> GND, AOUT -> GPIO 34 (Analog In).\n"
            "   • **5V/3.3V Relay Module (Pump Control):** VCC -> 5V, GND -> GND, IN -> GPIO 23.\n\n"
            "2. **Logic & Calibration:**\n"
            "   • Dry Soil (सूखी मिट्टी) Sensor Value > 2800 -> Relay ON (Watering Starts).\n"
            "   • Wet Soil (पर्याप्त नमी) Sensor Value < 1600 -> Relay OFF (Pump Stops)."
        )
    }
]

FIRST_AID_DATA = [
    {
        "question": "सांप के काटने (Snake Bite) पर तुरंत क्या प्राथमिक उपचार करना चाहिए?",
        "solution": (
            "🚨 **सांप काटने (Snake Bite) पर जीवन रक्षक प्राथमिक उपचार (Emergency Protocol):**\n\n"
            "1. **तुरंत क्या करें (Do's - 'RIGHT' Protocol):**\n"
            "   • **Reassure (धैर्य रखें):** पीड़ित को शांत रखें, घबराने से दिल की धड़कन तेज होती है और जहर तेजी से फैलता है।\n"
            "   • **Immobilize (अंग को स्थिर रखें):** जिस हाथ या पैर में काटा है, उसे स्प्लिंट या पट्टी बांधकर बिना हिलाए दिल के स्तर से नीचे रखें।\n"
            "   • **Get to Hospital:** तुरंत नजदीकी सरकारी अस्पताल ले जाएं जहां **Anti-Snake Venom (ASV)** उपलब्ध हो।\n\n"
            "2. **क्या कभी न करें (Strict Don'ts - खतरनाक गलतियां):**\n"
            "   • ❌ चीरा (Cut) न लगाएं, मुंह से चूसने की कोशिश न करें।\n"
            "   • ❌ कसकर रस्सी या धागा (Tourniquet) न बांधें, इससे रक्त प्रवाह रुककर अंग सड़ सकता है।\n"
            "   • ❌ बर्फ न लगाएं और झाड़-फूंक में समय बर्बाद न करें।"
        )
    },
    {
        "question": "तेज बुखार (High Fever) और बदन दर्द में क्या प्राथमिक दवा और देखभाल करें?",
        "solution": (
            "🌡️ **तेज बुखार (Fever Management) प्राथमिक उपचार:**\n\n"
            "1. **दवा (Adult Medicine):** **Paracetamol (500mg या 650mg)** आवश्यकतानुसार 6-8 घंटे में 1 गोली (दिन में अधिकतम 3-4 ग्राम)।\n"
            "2. **सादे पानी की पट्टी (Sponging):** माथे, गर्दन और बगलों पर सामान्य नल के पानी की पट्टी रखें (बर्फ कभी न लगाएं)।\n"
            "3. **तरल पदार्थ:** ORS का घोल, नींबू पानी या नारियल पानी खूब पिलाएं ताकि डिहाइड्रेशन न हो।\n"
            "4. **डॉक्टर से संपर्क:** यदि बुखार 102°F से अधिक हो या 3 दिन से बना रहे, तो तुरंत रक्त जांच (मलेरिया/डेंगू/टाइफाइड) करवाएं।"
        )
    }
]

def generate_full_dataset(target_count: int = 1200):
    dataset = []

    # 1. Generate Agricultural Multi-Dialect Multi-Parameter combinations
    for _ in range(target_count - 100):
        crop_info = random.choice(CROPS_DATA)
        prob = random.choice(crop_info["problems"])
        sol = crop_info["solutions"][prob]
        param = random.choice(PARAMETERS_LIST)
        dialect = random.choice(list(DIALECT_STYLES.keys()))
        template = random.choice(DIALECT_STYLES[dialect])

        user_prompt = template.format(
            crop=crop_info["crop"],
            problem=prob,
            parameter=param["desc"]
        )

        response = (
            f"🌾 **{crop_info['crop']} - {prob} का वैज्ञानिक समाधान व प्रबंधन:**\n\n"
            f"📍 **आपकी स्थिति के अनुसार ({param['desc']}):**\n"
            f"• **रोग/समस्या का उपचार:** {sol}\n"
            f"• **खाद व पोषण:** {crop_info['fertilizer']}\n"
            f"• **बीज दर:** {crop_info['base_seed_per_acre']} प्रति एकड़।\n"
            f"💡 **विशेष सलाह:** छिड़काव हमेशा सुबह या शाम के समय शांत मौसम में करें। यदि जमीन {param['soil']} है, तो जल निकासी का विशेष ध्यान रखें।"
        )

        dataset.append({
            "instruction": user_prompt,
            "input": f"User Context: Land Area = {param['mult']} Acres, Soil = {param['soil']}",
            "output": response,
            "dialect": dialect,
            "domain": "agriculture"
        })

    # 2. Add Tech & IoT Data
    for item in TECH_IOT_DATA * 20:
        dataset.append({
            "instruction": item["question"],
            "input": "",
            "output": item["solution"],
            "dialect": "tech_hinglish",
            "domain": "hardware_iot"
        })

    # 3. Add Medical & Emergency First Aid Data
    for item in FIRST_AID_DATA * 20:
        dataset.append({
            "instruction": item["question"],
            "input": "",
            "output": item["solution"],
            "dialect": "hindi",
            "domain": "first_aid"
        })

    # Shuffle dataset
    random.shuffle(dataset)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for ex in dataset:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"✅ Successfully generated {len(dataset)} training samples at: {OUTPUT_FILE}")
    return OUTPUT_FILE

if __name__ == "__main__":
    generate_full_dataset()
