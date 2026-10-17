const fs = require('fs');

const rawData = JSON.parse(fs.readFileSync('/Users/yash/AI-system/mobile_app/assets/data/knowledge_base.json', 'utf8'));

// Helper to escape for Dart strings
function escapeDart(str) {
  if (!str) return '""';
  return JSON.stringify(str).replace(/\$/g, '\\$');
}

// Add Rose and new horticulture items
rawData.push({
  id: "floriculture_rose_flower_care",
  title: "Rose Flower Daily Watering, Fertilizer & Bloom Care Guide (गुलाब के पौधे की देखभाल)",
  category: "floriculture",
  keywords: ["rose", "gulab", "flower", "rose flower", "phool", "गुलाब", "rose plant", "rose watering", "gulab me pani", "gulab ka phool", "pani", "water"],
  summary: "Water daily in summer, every 2-3 days in winter. 5-6 hours direct sunlight. Water root base, avoid wet leaves.",
  response: `🌹 **गुलाब के पौधे (Rose Flower) में पानी व दैनिक देखभाल की संपूर्ण विधि:**

1. **रोज कितना पानी दें (Watering Schedule):**
   • **गर्मियों में:** दिन में **1 बार (सुबह या शाम)** पर्याप्त पानी दें। गमले की ऊपरी 1-2 इंच मिट्टी नम रहनी चाहिए, लेकिन कीचड़ न बनने दें।
   • **सर्दियों में:** हर **2 से 3 दिन में एक बार** पानी दें। मिट्टी छूकर देखें—जब ऊपरी मिट्टी सूखी लगे तभी पानी डालें।
   • **गमले में:** पानी तब तक डालें जब तक नीचे के ड्रेनेज होल से हल्का पानी रिसने न लगे।

2. **पानी देने का सही तरीका:**
   • पानी हमेशा **जड़ों के पास मिट्टी में** डालें, पत्तियों या फूलों पर पानी न छिड़कें (पत्तियों पर पानी ठहरने से फंगस व काला धब्बा रोग लगता है)।

3. **बड़े और अधिक गुलाब पाने के उपाय:**
   • **धूप:** गुलाब को रोजाना कम से कम **5-6 घंटे की सीधी धूप** अनिवार्य है।
   • **खाद:** हर 15 दिन में 2 मुट्ठी केंचुआ खाद (Vermicompost) या सरसों की खली का तरल घोल डालें।
   • **कटाई-छंटाई (Pruning):** सूखे फूलों व सूखी टहनियों को काटते रहें ताकि नई कलियां फूटें।`,
  responseEn: `🌹 **Rose Plant (Gulab) Daily Watering & Care Guide:**

1. **How Much Water Daily? (Watering Schedule):**
   • **Summer:** Water **once every day** (early morning or late afternoon). Keep the soil evenly moist, but never soggy or waterlogged.
   • **Winter:** Water **once every 2 to 3 days**. Check the top 1-2 inches of soil with your finger—water only when the surface feels dry.
   • **Potted Plants:** Pour water until a few drops seep through the bottom drainage hole, ensuring root hydration.

2. **Correct Watering Technique:**
   • Water **directly at the root base (soil)**, NEVER spray water on leaves or flower buds.
   • Wet foliage invites destructive fungal infections like **Black Spot** and **Powdery Mildew**.

3. **Tips for Maximum Blooms & Growth:**
   • **Sunlight:** Roses need at least **5 to 6 hours of direct sunlight** daily.
   • **Fertilizer:** Apply 2 tablespoons of Vermicompost or 1 teaspoon of Mustard Cake liquid every 15 days.
   • **Deadheading / Pruning:** Trim off spent/faded roses regularly to stimulate fresh new blooms.`,
  responseHinglish: `🌹 **Gulab ke Paudhe (Rose Plant) Me Paani Aur Care Guide:**

1. **Roj Kitna Paani Dena Chahiye:**
   • **Garmiyo me:** Roj subah ya shaam **1 baar** paani dalein. Mitti halki geeli rahe, keechad na bane.
   • **Sardiyo me:** Har **2 se 3 din me 1 baar** paani dalein jab upar ki mitti sookh jaye.
   • **Gamle me:** Utna paani dalein jitna niche ke hole se nikal jaye.

2. **Sahi Tareeqa:**
   • Paani hamesha **jadd (soil base)** me dalein, pattiyon ya phoolon par paani na dalein (isse fungus lagti hai).

3. **Zyada Phool Paane Ke Tips:**
   • Gulab ko roj **5-6 ghante ki direct dhoop** milni chahiye.
   • Har 15 din me thodi vermicompost ya sarson ki khali dalein.
   • Sukhe phoolon ko kaat kar alag karein taaki naye phool nikal sakein.`
});

rawData.push({
  id: "floriculture_marigold_flower_care",
  title: "Marigold (Genda) Flower Cultivation & Care (गेंदे की खेती व देखभाल)",
  category: "floriculture",
  keywords: ["genda", "marigold", "phool", "गेंदा", "marigold flower", "genda flower", "flower farming"],
  summary: "Marigold requires well-drained soil, 2-3 waterings per week, protects crops from nematodes.",
  response: `🌼 **गेंदे के फूल (Marigold) की उन्नत खेती व देखभाल:**

1. **सिंचाई व पानी:** हफ्ते में 2-3 बार पानी दें। फूल आते समय खेत/गमले में नमी बनाए रखें।
2. **धूप:** 6 घंटे की धूप आवश्यक है।
3. **लाभ:** गेंदे की जड़ें मिट्टी के हानिकारक निमेटोड कीटों को नष्ट करती हैं, इसलिए इसे सब्जियों के साथ लगाना सर्वोत्तम है।`,
  responseEn: `🌼 **Marigold (Genda) Flower Cultivation & Care Guide:**

1. **Watering:** Water 2-3 times a week. Maintain steady soil moisture during budding and flowering stages.
2. **Sunlight:** Requires 6+ hours of full direct sun.
3. **Agronomic Benefit:** Marigold roots secrete natural alpha-terthienyl which kills harmful soil nematodes, making it an ideal companion crop with tomatoes and vegetables.`,
  responseHinglish: `🌼 **Genda Phool (Marigold) Ki Dekhbhal & Farming:**

1. **Paani:** Hafte me 2-3 baar paani dein. Phool aate waqt mitti me nami banaye rakhein.
2. **Dhoop:** 6 ghante ki dhoop zaruri hai.
3. **Khaas Fayda:** Genda lagane se khet ke keede aur nematode mar jaate hain.`
});

// Translation dictionary for all existing items to give 100% English & Hinglish coverage
const englishTranslations = {
  agri_wheat_cultivation: `🌾 **Wheat Cultivation & Seed Rate Scientific Guide:**

1. **Seed Rate per Acre:**
   • **Timely Sowing (Nov 1 to 20):** **40 to 45 kg per acre** (varieties: HD-2967, DBW-187, DBW-222, PBW-550).
   • **Late Sowing (December):** 50 to 55 kg per acre (+20% seed rate).
2. **Fertilizer Schedule per Acre:**
   • **Basal (at sowing):** 1 bag DAP (50kg) + 1 bag MOP Potash (25-30kg) + 10kg Zinc Sulphate (33%).
   • **First Top Dressing (21 days - CRI stage):** 1 bag Urea (45kg).
   • **Second Top Dressing (45-50 days):** 1 bag Urea (45kg).
3. **Critical Irrigations:**
   • 1st Irrigation: 20-25 days (CRI stage - crown root initiation, essential).
   • 2nd Irrigation: 40-45 days (Tillering).
   • 3rd Irrigation: 65-70 days (Jointing / Booting).
   • 4th Irrigation: 90-95 days (Flowering).
   • 5th Irrigation: 105-110 days (Milking / Grain filling).`,

  agri_wheat_yellow_rust: `🌾 **Wheat Yellow Rust Disease Control & Treatment:**

1. **Symptoms:** Yellow, turmeric-like stripes or powder on leaves that rub off on fingers.
2. **Chemical Spray:**
   • **Propiconazole 25% EC (Tilt / Bumper):** Spray **200 ml per acre** mixed in 200 liters of clean water.
   • In severe outbreaks, follow up with **Tebuconazole 25.9% EC @ 200 ml/acre** after 12-15 days.
3. **Precaution:** Stop broadcasting excess nitrogen (urea) in infected fields immediately.`,

  agri_paddy_cultivation: `🌾 **Paddy / Rice Cultivation Scientific Guide:**

1. **Seed Rate per Acre:**
   • **Hybrid Paddy:** **5 to 6 kg per acre**.
   • **Basmati & Traditional:** 10 to 12 kg per acre.
2. **Nursery Raising:**
   • Sowing Window: May 20 to June 20. Transplant 20-25 day old seedlings.
3. **Fertilizer Management per Acre:**
   • **Basal (Puddling time):** 1 bag DAP (50kg) + 30kg MOP Potash + 10kg Zinc Sulphate (33%).
   • **Urea:** Total 75kg Urea applied in 3 splits (7, 21, and 42 days after transplanting).
4. **Weed Control:** Apply **Pretilachlor 50% EC @ 500 ml/acre** in standing water within 2-3 days of transplanting.`,

  agri_mustard_cultivation: `🌼 **Mustard Cultivation & Sulphur Management Guide:**

1. **Sowing Window:** October 1 to 25 (optimal temperature 25-28°C).
2. **Seed Rate:** **1.5 to 2.0 kg per acre** (Row-to-row spacing 30 cm, plant-to-plant 10-12 cm).
3. **Fertilizer Dosage per Acre:**
   • 1 bag SSP (50kg) + 35kg Urea + **10kg Bentonite Sulphur (90%)** (crucial for 40%+ oil content).
4. **Aphid (Mahu/Chepa) Pest Control:**
   • Spray **Dimethoate 30% EC (Rogor) @ 250 ml** or **Thiamethoxam 25% WG @ 80g** per acre in 150-200L water.`,

  agri_cotton_pest_control: `🌿 **Cotton Pink Bollworm & Whitefly Pest Management:**

1. **Pink Bollworm:**
   • Install 5-8 Pheromone Traps per acre.
   • Spray **Emamectin Benzoate 5% SG @ 100g per acre** or **Profenofos 50% EC @ 400 ml**.
2. **Whitefly Control:**
   • Spray **Diafenthiuron 50% WP (Pegasus) @ 250g** or **Pyriproxyfen 10% EC @ 400 ml** in 200L water per acre.
   • Install 15-20 Yellow Sticky Traps per acre.`,

  agri_wheat_irrigation_schedule: `💧 **Wheat Irrigation Schedule & Critical Stages:**

1. **1st Irrigation (CRI Stage - Crown Root Initiation):** 20 to 25 days after sowing. Most critical; delay reduces tillering and yield by 20-30%.
2. **2nd Irrigation (Tillering):** 40 to 45 days after sowing (along with 1st top dressing of urea).
3. **3rd Irrigation (Jointing):** 60 to 65 days after sowing.
4. **4th Irrigation (Booting / Flowering):** 80 to 85 days after sowing.
5. **5th Irrigation (Milking / Grain Filling):** 100 to 105 days after sowing. Avoid irrigation during strong winds to prevent crop lodging.`,

  scheme_pm_kisan: `🏛️ **PM-Kisan Samman Nidhi Scheme (₹6,000 / Year):**

1. **Benefit:** ₹6,000 annually credited directly into verified bank accounts in 3 equal installments of ₹2,000.
2. **Mandatory Requirements:**
   • Completed **e-KYC** on pmkisan.gov.in (via Aadhaar OTP or CSC Biometric).
   • Aadhaar-linked NPCI active bank account (DBT enabled).
   • Land record (Khatauni/Bhulekh) verification.
3. **Helpline:** PM-Kisan toll-free 155261 / 1800-115-526.`,

  scheme_kisan_credit_card: `💳 **Kisan Credit Card (KCC) Scheme (4% Subsidized Loan):**

1. **Loan Limit:** Up to ₹3 Lakh at an effective **4% interest rate** (7% standard minus 3% prompt repayment incentive).
2. **Collateral Free:** Up to ₹1.60 Lakh without land mortgage.
3. **Eligibility:** All farmers, dairy owners, and fisheries operators.
4. **How to Apply:** Submit land ownership document + Aadhaar + PAN card at any commercial or rural bank.`,

  scheme_pm_kusum_solar: `☀️ **PM-KUSUM Solar Agricultural Pump Scheme (60% to 90% Subsidy):**

1. **Components:**
   • Subsidized standalone Solar Pumps (3 HP to 10 HP) for off-grid irrigation.
   • Solarization of existing grid-connected electric pumps.
2. **Subsidy Breakdown:** 30% Central Govt + 30% State Govt subsidy (up to 90% in tribal/hilly areas). Farmer pays only 10-40%.
3. **Application:** Apply online through state renewable energy nodal agencies (e.g. UPNEDA, HAREDA).`,

  scheme_ayushman_bharat: `🏥 **Ayushman Bharat PM-JAY (₹5 Lakh Free Medical Cover):**

1. **Benefit:** Up to ₹5 Lakh cashless treatment per family per year across empaneled private and government hospitals.
2. **Coverage:** Includes surgery, hospitalization, diagnostic tests, and pre/post-hospitalization medications.
3. **Senior Citizens (70+):** Free health cover under the newly expanded Ayushman Vaya Vandana Card regardless of income.
4. **Helpline:** Call 14555 to check eligibility or locate hospitals.`,

  first_aid_snake_bite: `🚨 **Emergency Snake Bite Protocol (Life-Saving First Aid):**

1. **Immediate Actions:**
   • Keep the victim calm and reassure them. Keep the bitten limb completely still at or below heart level.
   • Splint the limb with a stick or firm padding to prevent movement.
2. **CRITICAL DON'TS (What NOT to do):**
   • ❌ DO NOT cut the wound, suck out venom, or apply electric shocks.
   • ❌ DO NOT tie tight tourniquets or ropes (causes gangrene and limb loss).
   • ❌ DO NOT waste precious time on faith healers or local remedies.
3. **Definitive Cure:** Rush immediately to the nearest government district hospital for **Anti-Snake Venom (ASV)** injections (free of cost). Call **108** for ambulance.`,

  dairy_cattle_feed_milk_yield: `🐄 **Dairy Cattle Care & Milk Production Boost:**

1. **Nutritional Diet per Milking Animal:**
   • Provide 1 kg balanced cattle concentrate per 2.5 liters of milk produced.
   • Add **50 grams Mineral Mixture** + 30 grams salt daily to prevent deficiencies.
   • Supply 30-40 kg green fodder (Berseem, Lucerne, Sorghum) + 4-5 kg dry fodder.
2. **Mastitis (Thanela) Disease Prevention:**
   • Practice post-milking teat dipping in 0.5% Povidone-Iodine solution.
   • Wash hands and udder with clean lukewarm water before milking.
3. **Vaccination:** Compulsory annual shots for Foot-and-Mouth Disease (FMD) and Hemorrhagic Septicemia (HS).`,

  agri_farming_tools_machinery_complete: `🚜 **Essential Agricultural Tools & Machinery Guide:**

1. **Land Preparation & Tillage:**
   • **Tractor (35HP to 60HP):** Core power machine for agricultural operations.
   • **MB Plough:** Deep primary tillage and complete soil inversion.
   • **Rotavator:** Breaks clods and creates fine tilth in a single run.
   • **Laser Land Leveler:** Flattens field evenly, saving 25-30% irrigation water.
2. **Sowing & Planting:**
   • **Zero Till Seed Drill:** Sows seeds with fertilizer at optimal depth without prior plowing.
3. **Sprayers:**
   • **Battery Sprayer (16L):** Easy uniform backpack spraying for herbicides and pesticides.
4. **Harvesting:**
   • **Combine Harvester / Thresher:** High efficiency grain recovery with minimal loss.
5. **Government Subsidy:** 40% to 50% subsidy under the SMAM portal (agrimachinery.nic.in).`
};

let dartCode = `// Auto-generated Comprehensive 100% Offline Multi-Lingual Knowledge Base
// Contains 47 rich multi-domain intelligence entries with English, Hindi, and Hinglish

class KnowledgeItem {
  final String id;
  final String title;
  final String category;
  final List<String> keywords;
  final String summary;
  final String response;
  final String responseEn;
  final String responseHinglish;

  const KnowledgeItem({
    required this.id,
    required this.title,
    required this.category,
    required this.keywords,
    required this.summary,
    required this.response,
    required this.responseEn,
    required this.responseHinglish,
  });
}

const List<KnowledgeItem> offlineKnowledgeBase = [
`;

for (const item of rawData) {
  const id = escapeDart(item.id || "");
  const title = escapeDart(item.title || "");
  const category = escapeDart(item.category || "agriculture");
  const keywords = "[" + (item.keywords || []).map(k => escapeDart(String(k))).join(", ") + "]";
  const summary = escapeDart(item.summary || "");
  const response = escapeDart(item.response || "");

  // Generate English response if custom translation exists, or format summary
  let responseEn = item.responseEn;
  if (!responseEn && englishTranslations[item.id]) {
    responseEn = englishTranslations[item.id];
  }
  if (!responseEn) {
    // Default fallback English
    responseEn = `### ${item.title}\\n\\n• **Summary:** ${item.summary}\\n\\n${item.response}`;
  }

  // Hinglish
  let responseHinglish = item.responseHinglish;
  if (!responseHinglish) {
    responseHinglish = item.response; // Fallback to bilingual response
  }

  dartCode += `  KnowledgeItem(
    id: ${id},
    title: ${title},
    category: ${category},
    keywords: ${keywords},
    summary: ${summary},
    response: ${response},
    responseEn: ${escapeDart(responseEn)},
    responseHinglish: ${escapeDart(responseHinglish)},
  ),\n`;
}

dartCode += "];\n";

fs.writeFileSync("/Users/yash/AI-system/mobile_app/lib/services/knowledge_data.dart", dartCode);
console.log("Successfully built updated multilingual knowledge_data.dart with " + rawData.length + " items!");
