import 'dart:convert';
import 'package:http/http.dart' as http;
import 'knowledge_data.dart';

enum AppLanguage { hindi, english, hinglish }

class AIEngineService {
  // Configurable Server URLs
  static String serverBaseUrl = 'http://192.168.1.59:8000';
  static String emulatorBaseUrl = 'http://10.0.2.2:8000';
  static String localhostUrl = 'http://127.0.0.1:8000';

  String activeServerUrl = serverBaseUrl;
  bool isServerOnline = false;
  DateTime? _lastServerCheck;

  AppLanguage currentLanguage = AppLanguage.hindi;

  void setLanguage(AppLanguage lang) {
    currentLanguage = lang;
  }

  // Check local server connectivity without blocking
  Future<String?> checkServerConnectivity({bool force = false}) async {
    if (!force && _lastServerCheck != null && 
        DateTime.now().difference(_lastServerCheck!).inSeconds < 15 && !isServerOnline) {
      return null;
    }
    _lastServerCheck = DateTime.now();

    final candidateUrls = [activeServerUrl, serverBaseUrl, emulatorBaseUrl, localhostUrl];
    final uniqueUrls = candidateUrls.toSet().toList();

    for (final url in uniqueUrls) {
      try {
        final resp = await http.get(Uri.parse('$url/api/tags')).timeout(const Duration(milliseconds: 500));
        if (resp.statusCode == 200) {
          activeServerUrl = url;
          isServerOnline = true;
          return url;
        }
      } catch (_) {}
    }
    isServerOnline = false;
    return null;
  }

  // Language switch command detector
  String? handleLanguageSwitchCommand(String prompt) {
    final lower = prompt.toLowerCase().trim();

    // English switch
    if (RegExp(r'(english\s*(m|me|mai)?\s*(baat|bolo|bol|likh|kr|karo|batao)|talk\s*in\s*english|speak\s*in\s*english|switch\s*to\s*english|reply\s*in\s*english|in\s*english)', caseSensitive: false).hasMatch(lower)) {
      currentLanguage = AppLanguage.english;
      return '🌐 **Language switched to English!**\n\n'
          'Hello! I am **GramSetu AI**, your intelligent assistant.\n\n'
          'I am now trained to answer all your questions in English with human-like understanding:\n'
          '• **Crops & Diseases:** Wheat, Paddy, Mustard, Cotton, Potato, Tomato\n'
          '• **Floriculture & Plants:** Rose flower daily watering, gardening tips\n'
          '• **Farm Implements:** Tractors, Rotavator, Seed Drill, Sprayers\n'
          '• **Government Schemes:** PM-Kisan (₹6,000/yr), KCC Loan, PM-KUSUM Solar Pump\n'
          '• **Fertilizer Calculator:** DAP, Urea, Potash dosing per acre\n'
          '• **Emergency First Aid:** Snake bite, Heatstroke, High fever\n\n'
          '👉 Feel free to ask any question in English!';
    }

    // Hinglish switch
    if (RegExp(r'(hinglish\s*(m|me|mai)?\s*(baat|bolo|bol|likh|kr|karo|batao)|switch\s*to\s*hinglish|talk\s*in\s*hinglish)', caseSensitive: false).hasMatch(lower)) {
      currentLanguage = AppLanguage.hinglish;
      return '🌐 **Language switched to Hinglish!**\n\n'
          'Namaste! Ab main aapse **Hinglish** me baat karunga.\n\n'
          'Aap mujhse pooch sakte hain:\n'
          '• **Fasal aur Rog:** Gehun, Dhan, Sarson, Kapas me keede aur dawai\n'
          '• **Phool aur Baagwani:** Gulab ke paudhe me paani aur care\n'
          '• **Krishi Yantra:** Tractor, Rotavator, Seed Drill aur subsidy\n'
          '• **Sarkari Yojanayein:** PM Kisan, KCC Loan, Kusum Solar Pump\n'
          '• **Khad Calculator:** 1 ya 5 acre me DAP, Urea kitna dalein\n\n'
          '👉 Apna sawaal Hinglish me poochein!';
    }

    // Hindi switch
    if (RegExp(r'(hindi\s*(m|me|mai)?\s*(baat|bolo|bol|likh|kr|karo|batao)|switch\s*to\s*hindi|talk\s*in\s*hindi)', caseSensitive: false).hasMatch(lower)) {
      currentLanguage = AppLanguage.hindi;
      return '🌐 **भाषा बदलकर हिंदी कर दी गई है!**\n\n'
          'नमस्ते! मैं **ग्रामसेतु AI** हूँ। अब मैं आपके सभी सवालों के सटीक और मानवीय जवाब हिंदी में दूंगा।\n\n'
          'आप मुझसे पूछ सकते हैं:\n'
          '• **फसल व रोग रोकथाम:** गेहूं, धान, सरसों, कपास, आलू, टमाटर की उन्नत खेती\n'
          '• **फूल व बागवानी:** गुलाब में पानी, खाद और देखभाल\n'
          '• **कृषि यंत्र व औजार:** रोटावेटर, सीड ड्रिल, ट्रैक्टर और सरकारी सब्सिडी\n'
          '• **सरकारी योजनाएं:** PM-किसान (₹6,000), KCC (4% ब्याज), आयुष्मान भारत\n'
          '• **खाद कैलकुलेटर:** एकड़ या बीघा के अनुसार DAP, यूरिया की सटीक खुराक\n\n'
          '👉 अपना सवाल नीचे लिखकर या बोलकर पूछें!';
    }

    return null;
  }

  // Cloud Generative AI Engine (Pollinations AI - Real Generative LLM)
  Future<String?> fetchCloudGenerativeAI(String prompt, {List<Map<String, String>> history = const []}) async {
    String langInstruction;
    switch (currentLanguage) {
      case AppLanguage.english:
        langInstruction = 'You MUST answer strictly in fluent, natural English with clear markdown formatting, bullet points, numbers, and helpful emojis.';
        break;
      case AppLanguage.hinglish:
        langInstruction = 'You MUST answer in natural, conversational Hinglish (Hindi written in Roman English alphabet) with a warm tone and clean bullet points.';
        break;
      case AppLanguage.hindi:
      default:
        langInstruction = 'You MUST answer strictly in natural, polite Hindi (Devanagari script) with clear bullet points, practical dosages, and structured markdown.';
        break;
    }

    final systemPrompt = 'You are GramSetu AI (ग्रामसेतु AI), a human-like, highly empathetic, and scientifically accurate generative AI assistant tailored for farmers, rural communities, students, and citizens in India.\n'
        'Core Behavior & Knowledge Guidelines:\n'
        '1. ANSWER THE EXACT QUESTION ASKED: Pay close attention to the specific plant, crop, animal, machinery, disease, or topic in the query. Never substitute or confuse different entities (e.g., if asked about rose flower, talk ONLY about rose flower; if asked about wheat, talk about wheat).\n'
        '2. PRACTICAL & ACTIONABLE: Provide exact numbers, dosages (per acre, per plant, or per liter of water), timing, and step-by-step instructions.\n'
        '3. LANGUAGE ADAPTATION: $langInstruction\n'
        '4. FORMATTING: Use structured markdown with headings, bold keywords, and clean bullet points.';

    final messages = <Map<String, String>>[
      {'role': 'system', 'content': systemPrompt},
    ];

    if (history.isNotEmpty) {
      final recent = history.length > 4 ? history.sublist(history.length - 4) : history;
      for (final m in recent) {
        messages.add({'role': m['role'] ?? 'user', 'content': m['content'] ?? ''});
      }
    }
    messages.add({'role': 'user', 'content': prompt});

    try {
      final resp = await http.post(
        Uri.parse('https://text.pollinations.ai/'),
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)',
        },
        body: jsonEncode({
          'messages': messages,
          'model': 'openai',
        }),
      ).timeout(const Duration(seconds: 7));

      if (resp.statusCode == 200 && resp.body.trim().isNotEmpty && resp.body.trim() != '{}') {
        return resp.body.trim();
      }
    } catch (_) {}

    return null;
  }

  // Rose Flower / Gulab Daily Care & Watering (Dedicated Exact Match)
  String? handleRoseQuery(String prompt) {
    final lower = prompt.toLowerCase();
    final hasRose = RegExp(r'(rose|gulab|गुलाब)', caseSensitive: false).hasMatch(lower);

    if (hasRose) {
      if (currentLanguage == AppLanguage.english) {
        return '🌹 **Rose Plant (Gulab) Daily Watering & Care Guide:**\n\n'
            '### 1. Daily Watering Schedule\n'
            '• **Summer (गर्मियां):** Water **once every day** (early morning or late afternoon). The soil should remain evenly moist, but never waterlogged or swampy.\n'
            '• **Winter (सर्दियां):** Water **once every 2 to 3 days**. Check the top 1-2 inches of soil with your finger—water only when the surface feels dry.\n'
            '• **Potted Plants (गमले में):** Pour water slowly until you see a few drops drain out from the bottom drainage hole, ensuring deep root hydration.\n\n'
            '### 2. Correct Watering Technique\n'
            '• Water **directly at the root base (soil)**, NEVER splash water onto leaves or buds.\n'
            '• Wet foliage attracts destructive fungal diseases like **Black Spot** and **Powdery Mildew**.\n\n'
            '### 3. Tips for Maximum Blooms & Big Flowers\n'
            '• **Direct Sunlight:** Roses need at least **5 to 6 hours of full direct sunlight** daily to produce heavy blooms.\n'
            '• **Fertilizer:** Feed 2 tablespoons of Vermicompost (केंचुआ खाद) or 1 teaspoon of Mustard Cake liquid (सरसों की खली) every 15 days.\n'
            '• **Deadheading (Pruning):** Snip off faded/spent flowers regularly to encourage the plant to produce fresh new rose buds.';
      }

      if (currentLanguage == AppLanguage.hinglish) {
        return '🌹 **Gulab ke Paudhe (Rose Plant) Me Paani Aur Care Guide:**\n\n'
            '### 1. Roj Kitna Paani Dena Chahiye?\n'
            '• **Garmiyo me:** Roj subah ya shaam **1 baar** paani dalein. Mitti halki geeli rahe, lekin keechad na bane.\n'
            '• **Sardiyo me:** Har **2 se 3 din me 1 baar** paani dalein jab upar ki 1-2 inch mitti sookh jaye.\n'
            '• **Gamle me:** Utna paani dalein jitna niche ke drainage hole se nikal jaye.\n\n'
            '### 2. Sahi Tareeqa\n'
            '• Paani hamesha **jadd (soil base)** me dalein, pattiyon ya phoolon par paani na dalein (isse fungus lagti hai).\n\n'
            '### 3. Zyada Phool Paane Ke Tips\n'
            '• Gulab ko roj **5-6 ghante ki direct dhoop** milni chahiye.\n'
            '• Har 15 din me thodi vermicompost ya sarson ki khali dalein.\n'
            '• Sukhe phoolon ko kaat kar alag karein taaki naye phool nikal sakein.';
      }

      return '🌹 **गुलाब के पौधे (Rose Flower) में पानी व दैनिक देखभाल की संपूर्ण विधि:**\n\n'
          '### 1. रोज कितना पानी दें (Watering Schedule)\n'
          '• **गर्मियों में:** दिन में **1 बार (सुबह या शाम)** पर्याप्त पानी दें। गमले की मिट्टी नम रहनी चाहिए, लेकिन कीचड़ न बनने दें।\n'
          '• **सर्दियों में:** हर **2 से 3 दिन में एक बार** पानी दें। मिट्टी छूकर देखें—जब ऊपरी 1-2 इंच मिट्टी सूखी लगे तभी पानी डालें।\n'
          '• **गमले में:** पानी तब तक डालें जब तक नीचे के छेद (Drainage Hole) से हल्का पानी रिसने न लगे।\n\n'
          '### 2. पानी देने का सही तरीका\n'
          '• पानी हमेशा **जड़ों के पास मिट्टी में** डालें, पत्तियों या फूलों पर पानी न छिड़कें (पत्तियों पर पानी ठहरने से फंगस व काला धब्बा रोग लगता है)।\n\n'
          '### 3. बड़े और अधिक गुलाब पाने के उपाय\n'
          '• **धूप:** गुलाब को रोजाना कम से कम **5-6 घंटे की सीधी धूप** अनिवार्य है।\n'
          '• **खाद:** हर 15 दिन में 2 मुट्ठी केंचुआ खाद (Vermicompost) या सरसों की खली का तरल घोल डालें।\n'
          '• **कटाई-छंटाई (Pruning):** सूखे फूलों व सूखी टहनियों को काटते रहें ताकि नई कलियां फूटें।';
    }

    return null;
  }

  // Greeting detector
  String? handleGreeting(String prompt) {
    final lower = prompt.toLowerCase().trim();
    final greetingRegex = RegExp(
      r'\b(namaste|namaskar|ram ram|radhe radhe|hello|hi|hey|pranam|kisan bhai|kaise ho|kya haal|kya kar sakte|madad|help|who are you|tum kaun ho|aap kaun ho)\b',
      caseSensitive: false,
    );

    if (greetingRegex.hasMatch(lower) || lower == 'नमस्ते' || lower == 'राम राम' || lower == 'हेलो') {
      if (currentLanguage == AppLanguage.english) {
        return '🙏 **Hello! I am GramSetu AI (Rural AI Assistant).**\n\n'
            'I am equipped with both local offline knowledge and deep generative reasoning.\n\n'
            '🌾 **Here is how I can assist you:**\n'
            '1. **Crops & Diseases:** Wheat, Paddy, Mustard, Cotton, Potato, Tomato (pest, blight, rust).\n'
            '2. **Flowers & Gardening:** Rose flower daily watering, pruning, and blooming care.\n'
            '3. **Farm Tools & Machinery:** Tractors, Rotavator, Seed Drill, Sprayers, SMAM subsidy.\n'
            '4. **Fertilizer Calculator:** Instant dosage for DAP, Urea, Zinc per acre or bigha.\n'
            '5. **Government Schemes:** PM-Kisan Samman Nidhi (₹6,000/yr), KCC Loan, PM Kusum Solar.\n'
            '6. **Emergency First Aid:** Snake bite ASV protocol, fever, burn care, and 108/112 helplines.\n\n'
            '👉 Ask any question below to get started!';
      }

      if (currentLanguage == AppLanguage.hinglish) {
        return '🙏 **Namaste! Main GramSetu AI (Rural AI Assistant) hoon.**\n\n'
            'Main offline aur generative dono tareeqon se trained hoon.\n\n'
            '🌾 **Aap mujhse in cheezon par madad le sakte hain:**\n'
            '1. **Fasal aur Rog:** Gehun, Dhan, Sarson, Kapas me bimari aur spray.\n'
            '2. **Gulab aur Baagwani:** Gulab ke paudhe me paani aur care.\n'
            '3. **Krishi Yantra:** Tractor, Rotavator, Seed Drill aur sarkari subsidy.\n'
            '4. **Khad Calculation:** Kitne acre ya bigha me kitna DAP aur Urea lagega.\n'
            '5. **Sarkari Yojanayein:** PM Kisan (₹6,000), KCC Loan, PM Kusum Solar Pump.\n'
            '6. **Emergency First Aid:** Saanp kaatna, tez bukhar aur 108 ambulance.\n\n'
            '👉 Apna sawaal neeche likhkar ya bolkar poochein!';
      }

      return '🙏 **नमस्ते! मैं ग्रामसेतु AI (GramSetu Rural AI) सहायक हूँ।**\n\n'
          'मैं स्थानीय ऑफ़लाइन ज्ञान और डीप जेनरेटिव रीजनिंग दोनों से प्रशिक्षित हूँ।\n\n'
          '🌾 **आप मुझसे इन विषयों पर मदद ले सकते हैं:**\n'
          '1. **फसल व रोग रोकथाम:** गेहूं, धान, सरसों, कपास, आलू, टमाटर (बीज दर, पीला रतुआ, माहू, झुलसा आदि)।\n'
          '2. **फूल व बागवानी:** गुलाब में पानी, खाद और नई कलियां लाने के उपाय।\n'
          '3. **कृषि यंत्र व औजार:** ट्रैक्टर, रोटावेटर, सीड ड्रिल, हार्वेस्टर व 40-50% सब्सिडी।\n'
          '4. **खाद व उर्वरक गणना:** जैसे: *"3 एकड़ गेहूं में कितना खाद डालें"*, *"सरसों का बीज व सल्फर"*।\n'
          '5. **सरकारी योजनाएं:** PM-किसान सम्मान निधि (₹6000), KCC ऋण, आयुष्मान भारत, PM कुसुम सोलर पंप।\n'
          '6. **आपातकालीन स्वास्थ्य:** सांप काटना, तेज बुखार, लू लगना, प्राथमिक उपचार व 108/112 हेल्पलाइन।\n\n'
          '👉 आप अपना सवाल नीचे लिखकर या बोलकर पूछें!';
    }
    return null;
  }

  // Fertilizer & Land Calculator Detector
  String? handleFertilizerCalculator(String prompt) {
    final lower = prompt.toLowerCase();
    final acreMatch = RegExp(r'(\d+(\.\d+)?)\s*(एकड़|acre|bigha|बीघा)', caseSensitive: false).firstMatch(lower);
    final mentionsFertilizer = RegExp(r'(खाद|fertilizer|dap|यूरिया|urea|पोटाश|बीज|seed|dar|rate|kitna|lagaye)', caseSensitive: false).hasMatch(lower);

    if (acreMatch != null && mentionsFertilizer) {
      double numVal = double.tryParse(acreMatch.group(1) ?? '1') ?? 1.0;
      final unit = acreMatch.group(3) ?? 'acre';
      double acres = numVal;
      if (unit.contains('bigha') || unit.contains('बीघा')) {
        acres = numVal / 1.6;
      }

      String crop = 'सामान्य फसल (General Crop)';
      int seedMin = (acres * 40).round();
      int seedMax = (acres * 45).round();
      double dapBags = (acres * 1.0);
      double ureaBags = (acres * 2.0);
      double potashKg = (acres * 25.0);
      double zincKg = (acres * 10.0);

      if (lower.contains('sarson') || lower.contains('सरसों') || lower.contains('mustard')) {
        crop = 'सरसों (Mustard)';
        seedMin = (acres * 1.5).round();
        seedMax = (acres * 2.0).round();
        dapBags = (acres * 0.5);
        ureaBags = (acres * 1.0);
        potashKg = 0;
        zincKg = (acres * 10.0);
      } else if (lower.contains('dhan') || lower.contains('धान') || lower.contains('paddy') || lower.contains('chawal')) {
        crop = 'धान (Paddy)';
        seedMin = (acres * 5).round();
        seedMax = (acres * 6).round();
        dapBags = (acres * 1.0);
        ureaBags = (acres * 2.0);
        potashKg = (acres * 30.0);
        zincKg = (acres * 10.0);
      } else if (lower.contains('gehu') || lower.contains('गेहूं') || lower.contains('wheat')) {
        crop = 'गेहूं (Wheat)';
      }

      if (currentLanguage == AppLanguage.english) {
        return '🌾 **Fertilizer & Seed Dosage for ${acres.toStringAsFixed(1)} Acre(s) ($numVal $unit) of $crop:**\n\n'
            '1. **🌱 Seed Requirement:** **$seedMin to $seedMax kg** certified seed.\n\n'
            '2. **🧪 Recommended Fertilizer Schedule:**\n'
            '   • **DAP (50kg bag):** **${dapBags.toStringAsFixed(1)} bag(s)** (apply basal at sowing time)\n'
            '   • **Urea (45kg bag):** **${ureaBags.toStringAsFixed(1)} bag(s)** (split into 1st & 2nd irrigation top-dressing)\n'
            '   • **MOP Potash:** **${potashKg.toStringAsFixed(0)} kg** (enhances grain filling & disease resistance)\n'
            '   • **Zinc Sulphate (33%) / Bentonite Sulphur:** **${zincKg.toStringAsFixed(0)} kg**\n\n'
            '💡 **Expert Tip:** Ensure adequate soil moisture before broadcasting fertilizer. Never apply urea under hot midday sun.';
      }

      return '🌾 **${acres.toStringAsFixed(1)} एकड़ भूमि ($numVal $unit) हेतु $crop के लिए खाद व बीज की सटीक गणना:**\n\n'
          '1. **🌱 बीज की मात्रा:** **$seedMin से $seedMax किग्रा** शुद्ध प्रमाणित बीज।\n\n'
          '2. **🧪 उर्वरक की खुराक (प्रति एकड़ अनुसार):**\n'
          '   • **DAP (50kg बैग):** **${dapBags.toStringAsFixed(1)} बैग** (बुवाई के समय खेत में नीचे डालें)\n'
          '   • **यूरिया (45kg बैग):** **${ureaBags.toStringAsFixed(1)} बैग** (पहली व दूसरी सिंचाई पर विभाजित करके दें)\n'
          '   • **MOP पोटाश:** **${potashKg.toStringAsFixed(0)} किग्रा** (दाने की चमक व मजबूती के लिए)\n'
          '   • **जिंक सल्फेट (33%) / बेंटोनाइट सल्फर:** **${zincKg.toStringAsFixed(0)} किग्रा**\n\n'
          '💡 **सलाह:** खाद डालते समय खेत में पर्याप्त नमी होना अनिवार्य है। यूरिया दोपहर की तेज धूप में न छिड़कें।';
    }
    return null;
  }

  // Farming Tools & Machinery for Rabi Crops
  String? handleFarmingToolsQuery(String prompt) {
    final lower = prompt.toLowerCase();
    final hasTool = RegExp(r'(tool|tools|equipment|machinery|yantra|auzar|aujaar|tractor|rotavator|plough|drill|harvester|sprayer)', caseSensitive: false).hasMatch(lower);
    final hasRabi = RegExp(r'(rabi|ravi|crop|fasal|grow|gehu|wheat|sarson|mustard)', caseSensitive: false).hasMatch(lower);

    if (hasTool && hasRabi) {
      if (currentLanguage == AppLanguage.english) {
        return '🚜 **Essential Agricultural Tools & Machinery for Rabi Crops (Wheat & Mustard):**\n\n'
            'Growing Rabi crops efficiently requires specific implements at each stage:\n\n'
            '### 1. Land Preparation & Tillage\n'
            '• **Tractor (35HP to 60HP):** Primary power source for heavy field operations.\n'
            '• **MB Plough (Mouldboard Plough):** Deep inversion tillage to bury crop residue and eradicate weed roots.\n'
            '• **Rotavator (Rotary Tiller):** Pulverizes clods and creates fine seedbed in a single pass.\n'
            '• **Laser Land Leveler:** Ensures uniform water distribution, saving 25-30% irrigation water.\n\n'
            '### 2. Sowing & Planting\n'
            '• **Zero Till Seed-cum-Fertilizer Drill:** Sows wheat directly into paddy stubble at uniform depth, saving diesel and time.\n'
            '• **Pneumatic / Multi-Crop Planter:** Ideal for precise spacing in mustard and maize.\n\n'
            '### 3. Crop Protection & Spraying\n'
            '• **Battery-Operated Backpack Sprayer (16L):** Easy, uniform spraying for weedicide and pesticide.\n'
            '• **Tractor-Mounted Boom Sprayer:** Covers 15-20 acres per day with precise chemical dosage.\n\n'
            '### 4. Harvesting & Threshing\n'
            '• **Combine Harvester:** Reaps, threshes, and cleans wheat grains rapidly.\n'
            '• **Straw Reaper:** Collects remaining wheat straw and makes animal fodder (bhusa).\n\n'
            '💡 **Government Subsidy:** 40% to 50% subsidy is available for individual farmers (up to 80% for Custom Hiring Centers) under the **SMAM (Sub-Mission on Agricultural Mechanization)** scheme at agrimachinery.nic.in.';
      }

      if (currentLanguage == AppLanguage.hinglish) {
        return '🚜 **Rabi Fasal (Gehun & Sarson) Ugane Ke Liye Zaruri Krishi Yantra:**\n\n'
            'Rabi season me fasal ki acchi paidawar ke liye mukhya yantra:\n\n'
            '### 1. Zameen Ki Tayari (Land Preparation)\n'
            '• **Tractor (35HP se 60HP):** Kheti ki mukhya machine.\n'
            '• **MB Plough:** Mitti ko palatne aur gehri jutai ke liye.\n'
            '• **Rotavator:** Dhele todkar mitti ko ek hi chakkar me barik aur naram banane ke liye.\n'
            '• **Laser Leveler:** Khet ko barabar karne ke liye jisse 25-30% paani bachta hai.\n\n'
            '### 2. Buwai (Sowing Machines)\n'
            '• **Zero Till Seed Drill:** Gehun ki seedhi buwai aur khad ek sath dalne ke liye.\n\n'
            '### 3. Dawai Ka Chhidkaw (Sprayers)\n'
            '• **Battery Sprayer:** 16 liter tanki ke sath asaan spray.\n'
            '• **Tractor Boom Sprayer:** Bade khet me tezi se spray karne ke liye.\n\n'
            '### 4. Katai Aur Nikasi (Harvesting)\n'
            '• **Combine Harvester / Thresher:** Gehun ki katai aur gehun-bhusa alag karne ke liye.\n\n'
            '💡 **Sarkari Subsidy:** SMAM portal par 40% se 50% tak sarkari anudaan milta hai.';
      }

      return '🚜 **रबी फसलों (गेहूं व सरसों) के लिए प्रमुख कृषि यंत्र व आधुनिक औजार:**\n\n'
          'रबी फसलों की समय पर बुवाई, कम लागत और अधिक पैदावार के लिए आवश्यक यंत्र:\n\n'
          '### 1. भूमि तैयारी व जुताई के यंत्र\n'
          '• **ट्रैक्टर (35HP से 60HP):** आधुनिक खेती की मुख्य शक्ति।\n'
          '• **एमबी प्लाऊ (MB Plough):** गहरी जुताई व मिट्टी पलटने के लिए।\n'
          '• **रोटावेटर (Rotavator):** ढेलों को बारीक कर समतल बीज-शय्या तैयार करने हेतु।\n'
          '• **लेजर लैंड लेवलर:** खेत को समतल कर 25-30% सिंचाई पानी की बचत करता है।\n\n'
          '### 2. बुवाई के यंत्र\n'
          '• **जीरो टिल सीड-कम-फर्टिलाइजर ड्रिल:** धान के अवशेषों में बिना जुताई सीधे गेहूं व खाद की सही गहराई पर बुवाई।\n'
          '• **हैप्पी सीडर / सुपर सीडर:** पराली प्रबंधन के साथ एक साथ बुवाई।\n\n'
          '### 3. पौध संरक्षण (स्प्रेयर)\n'
          '• **बैटरी चालित स्प्रेयर (16L):** खरपतवारनाशक व कीटनाशक का समान छिड़काव।\n'
          '• **ट्रैक्टर माउंटेड बूम स्प्रेयर:** बड़े रकबे में तेजी से छिड़काव हेतु।\n\n'
          '### 4. कटाई व गहाई\n'
          '• **कंबाइन हार्वेस्टर / थ्रेशर:** कम समय और कम लागत में दाना निकालने हेतु।\n'
          '• **स्ट्रॉ रीपर:** गेहूं का भूसा बनाने के लिए।\n\n'
          '💡 **सरकारी सब्सिडी:** SMAM (कृषि यंत्रीकरण) पोर्टल पर कृषि यंत्रों पर 40% से 50% तक अनुदान मिलता है।';
    }

    return null;
  }

  // Enhanced Multi-Token Matching with Subject Conflict Disqualification
  String searchOfflineKnowledge(String query) {
    // 1. Language switch commands (e.g. "english m baat kr", "hindi me bolo")
    final langSwitch = handleLanguageSwitchCommand(query);
    if (langSwitch != null) return langSwitch;

    // 2. Direct Subject Handler: Rose Flower / Gulab
    final roseAnswer = handleRoseQuery(query);
    if (roseAnswer != null) return roseAnswer;

    // 3. Greeting
    final greeting = handleGreeting(query);
    if (greeting != null) return greeting;

    // 4. Farming Tools Specific Routing
    final toolsAnswer = handleFarmingToolsQuery(query);
    if (toolsAnswer != null) return toolsAnswer;

    // 5. Fertilizer Calculator
    final calc = handleFertilizerCalculator(query);
    if (calc != null) return calc;

    // 6. Multi-word Token Matching across all knowledge items
    final clean = query.toLowerCase().trim();
    final stopwords = RegExp(
      r'^(which|what|how|why|when|who|where|the|a|an|is|are|in|on|at|to|for|of|with|and|or|required|needed|please|kya|kaise|hota|hote|hain|hai|ka|ke|ki|ko|se|me|pe|par|batao|bataiye|chahiye|karein|kare|karte|aur|kitna|kitni|kab|kaha|bta|krna|keliye|kliye|roj|daily|dein)$',
      caseSensitive: false,
    );

    final tokens = clean
        .replaceAll(RegExp(r'[^\w\u0900-\u097F\s]'), ' ')
        .split(RegExp(r'\s+'))
        .where((w) => !stopwords.hasMatch(w) && w.length > 1)
        .toList();

    KnowledgeItem? bestItem;
    int highestScore = 0;

    // Query subject tags
    final queryHasRose = clean.contains('rose') || clean.contains('gulab') || clean.contains('phool') || clean.contains('flower');
    final queryHasWheat = clean.contains('wheat') || clean.contains('gehu') || clean.contains('gehun') || clean.contains('गेहूं');
    final queryHasPaddy = clean.contains('paddy') || clean.contains('rice') || clean.contains('dhan') || clean.contains('धान');
    final queryHasMustard = clean.contains('mustard') || clean.contains('sarson') || clean.contains('सरसों');
    final queryHasCotton = clean.contains('cotton') || clean.contains('kapas') || clean.contains('कपास');

    for (final item in offlineKnowledgeBase) {
      // Disqualify crop items if query is about a completely different plant
      if (queryHasRose && (item.id.contains('wheat') || item.id.contains('paddy') || item.id.contains('cotton') || item.id.contains('mustard'))) {
        continue;
      }
      if (queryHasWheat && (item.id.contains('paddy') || item.id.contains('cotton') || item.id.contains('mustard'))) {
        continue;
      }
      if (queryHasPaddy && (item.id.contains('wheat') || item.id.contains('cotton') || item.id.contains('mustard'))) {
        continue;
      }
      if (queryHasMustard && (item.id.contains('wheat') || item.id.contains('paddy') || item.id.contains('cotton'))) {
        continue;
      }
      if (queryHasCotton && (item.id.contains('wheat') || item.id.contains('paddy') || item.id.contains('mustard'))) {
        continue;
      }

      int score = 0;
      final title = item.title.toLowerCase();
      final summary = item.summary.toLowerCase();

      // Whole phrase matches
      if (title.contains(clean)) score += 100;
      if (summary.contains(clean)) score += 40;

      // Token matches
      for (final tok in tokens) {
        if (title.contains(tok)) score += 35;
        if (summary.contains(tok)) score += 20;

        for (final kw in item.keywords) {
          final kwLow = kw.toLowerCase();
          if (kwLow == tok) {
            score += 35;
          } else if (kwLow.contains(tok) || tok.contains(kwLow)) {
            score += 15;
          }
        }
      }

      if (score > highestScore) {
        highestScore = score;
        bestItem = item;
      }
    }

    if (bestItem != null && highestScore >= 18) {
      if (currentLanguage == AppLanguage.english && bestItem.responseEn.isNotEmpty) {
        return bestItem.responseEn;
      } else if (currentLanguage == AppLanguage.hinglish && bestItem.responseHinglish.isNotEmpty) {
        return bestItem.responseHinglish;
      }
      return bestItem.response;
    }

    // Intelligent Fallback based on query domain and selected language
    if (currentLanguage == AppLanguage.english) {
      return '🌾 **GramSetu AI (Offline Rural Assistant):**\n\n'
          'Key guidelines for your query **"$query"**:\n\n'
          '1. **Crops & Cultivation:** Specify your crop (e.g. Wheat, Paddy, Mustard, Cotton, Potato, Tomato) for accurate seed rate, fertilizer schedule, and disease control.\n\n'
          '2. **Flowers & Gardening:** For plants like Rose (Gulab) or Marigold, water directly at the root base and ensure 5-6 hours of daily sunlight.\n\n'
          '3. **Farm Tools & Mechanization:** Tractors (35-60HP), Rotavators, Zero Till Seed Drills, and Sprayers reduce costs and boost yields (40-50% subsidy under SMAM portal).\n\n'
          '4. **Fertilizer Calculator:** Ask with acreage (e.g. *"Fertilizer for 3 acres wheat"* or *"DAP dosage"*).\n\n'
          '5. **Government Schemes:** PM-Kisan Samman Nidhi (₹6,000/yr), Kisan Credit Card (4% interest), PM-KUSUM Solar Pump.\n\n'
          '6. **Emergency Numbers:** Dial **108** for Ambulance, **112** for Emergency.\n\n'
          '💡 *Tip: Try asking specific questions like "rose flower care", "mustard seed rate", "farming tools for rabi", or "PM Kisan scheme".*';
    }

    if (currentLanguage == AppLanguage.hinglish) {
      return '🌾 **GramSetu AI (Offline Rural Assistant):**\n\n'
          'Aapke sawaal **"$query"** ke mukhya sujhav:\n\n'
          '1. **Fasal aur Rog:** Gehun, Dhan, Sarson, Kapas ke liye seed rate, fertilizer dosage aur spray ki puri jaankari uplabdh hai.\n\n'
          '2. **Phool aur Baagwani:** Gulab ke paudhe me roj garmi me 1 baar paani dalein aur 5-6 ghante dhoop dein.\n\n'
          '3. **Krishi Yantra:** Tractor, Rotavator, Seed Drill aur Sprayers se kheti ki lagat kam hoti hai (40-50% sarkari subsidy milti hai).\n\n'
          '4. **Khad Calculator:** Zameen ka size likhkar poochein (jaise *"2 acre gehun me khad"* ya *"5 bigha me kitna DAP"*).\n\n'
          '5. **Sarkari Yojanayein:** PM Kisan Samman Nidhi (₹6000), KCC Loan (4% byaj), PM Kusum Solar Pump.\n\n'
          '6. **Emergency Helpline:** Ambulance ke liye **108** aur police ke liye **112** dial karein.\n\n'
          '💡 *Tip: Seedhe poochein jaise "gulab me paani", "gehun me peela ratua", "sarson me mahu dawai", "tractor subsidy" ya "pm kisan".*';
    }

    // Default Hindi Fallback
    return '🌾 **ग्रामसेतु AI (ऑफ़लाइन ग्रामीण सहायक):**\n\n'
        'आपके प्रश्न **"$query"** के संबंध में मुख्य सलाह:\n\n'
        '1. **कृषि व फसल:** बुवाई, खाद (DAP, यूरिया), व कीट नियंत्रण हेतु सटीक फसल का नाम दर्ज करें (जैसे: *गेहूं*, *धान*, *सरसों*, *कपास*)।\n\n'
        '2. **फूल व बागवानी:** गुलाब के पौधे में गर्मियों में रोज 1 बार पानी दें और 5-6 घंटे की सीधी धूप अनिवार्य रूप से दें।\n\n'
        '3. **कृषि यंत्र व औजार:** रोटावेटर, सीड ड्रिल, व स्प्रेयर से लागत कम और पैदावार बढ़ती है। (SMAM पोर्टल पर 40-50% सब्सिडी उपलब्ध है)।\n\n'
        '4. **जमीन व खाद गणना:** रकबा दर्ज करके पूछें (जैसे: *"3 एकड़ गेहूं में खाद"* या *"5 बीघा में कितना एकड़"*)\n\n'
        '5. **सरकारी योजनाएं:** PM-किसान सम्मान निधि (₹6000/वर्ष) व KCC (4% ब्याज दर) के नियम व पात्रता उपलब्ध हैं।\n\n'
        '6. **आपातकाल:** एम्बुलेंस के लिए **108** और पुलिस सहायता के लिए **112** डायल करें।\n\n'
        '💡 *सुझाव: विशिष्ट जानकारी के लिए जैसे "गुलाब में पानी", "सरसों में माहू दवा", "रबी फसल कृषि यंत्र", "सांप काटना" या "पीएम किसान" लिखकर पूछें।*';
  }

  // Stream Chat Response: Intelligent Dual Hybrid Engine (Cloud Generative LLM + Offline Fallback)
  Stream<String> generateStreamingChat(String prompt, {List<Map<String, String>> history = const []}) async* {
    // 1. Language switch commands
    final langSwitch = handleLanguageSwitchCommand(prompt);
    if (langSwitch != null) {
      yield langSwitch;
      return;
    }

    // 2. Check local server if configured
    await checkServerConnectivity();
    if (isServerOnline) {
      try {
        final request = http.Request('POST', Uri.parse('$activeServerUrl/api/chat'));
        request.headers['Content-Type'] = 'application/json';
        request.body = jsonEncode({
          'prompt': prompt,
          'session_id': 'mobile_session',
          'history': history,
        });

        final streamedResponse = await request.send();
        await for (final chunk in streamedResponse.stream.transform(utf8.decoder)) {
          final lines = chunk.split('\n').where((l) => l.trim().isNotEmpty);
          for (final line in lines) {
            try {
              final packet = jsonDecode(line);
              if (packet['type'] == 'token' && packet['token'] != null) {
                yield packet['token'] as String;
              }
            } catch (_) {
              yield line;
            }
          }
        }
        return;
      } catch (_) {}
    }

    // 3. True Generative AI Inference (when internet is available on phone)
    // Understands literally ANY question with human-level reasoning!
    String? cloudAiResponse;
    try {
      cloudAiResponse = await fetchCloudGenerativeAI(prompt, history: history);
    } catch (_) {
      cloudAiResponse = null;
    }

    if (cloudAiResponse != null && cloudAiResponse.trim().isNotEmpty) {
      const int chunkSize = 8;
      for (int i = 0; i < cloudAiResponse.length; i += chunkSize) {
        final end = (i + chunkSize < cloudAiResponse.length) ? i + chunkSize : cloudAiResponse.length;
        yield cloudAiResponse.substring(i, end);
        await Future.delayed(const Duration(milliseconds: 6));
      }
      return;
    }

    // 4. Offline Local Knowledge Brain (Fallback when airplane mode / no signal)
    final fullAnswer = searchOfflineKnowledge(prompt);
    const int chunkSize = 8;
    for (int i = 0; i < fullAnswer.length; i += chunkSize) {
      final end = (i + chunkSize < fullAnswer.length) ? i + chunkSize : fullAnswer.length;
      yield fullAnswer.substring(i, end);
      await Future.delayed(const Duration(milliseconds: 8));
    }
  }
}
