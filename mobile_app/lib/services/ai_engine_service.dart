import 'dart:convert';
import 'package:http/http.dart' as http;

class AIEngineService {
  // Configurable Server URL (Android Emulator: 10.0.2.2:8000, Wi-Fi LAN: 192.168.1.59:8000, Localhost: 127.0.0.1:8000)
  static String serverBaseUrl = 'http://192.168.1.59:8000';
  static String emulatorBaseUrl = 'http://10.0.2.2:8000';
  static String localhostUrl = 'http://127.0.0.1:8000';

  String activeServerUrl = serverBaseUrl;
  bool isServerOnline = false;

  // Embedded 100% Offline RAG Knowledge Base (Native Dart Engine)
  static final List<Map<String, dynamic>> offlineKnowledge = [
    {
      "id": "agri_wheat_yellow_rust",
      "keywords": ["peela ratua", "yellow rust", "gehu", "wheat", "propiconazole", "पीला रतुआ", "गेहूं"],
      "title": "गेहूं में पीला रतुआ रोकथाम",
      "response": "🌾 **गेहूं में पीला रतुआ (Yellow Rust) रोकथाम:**\n• **दवा:** **Propiconazole 25% EC (Tilt)** @ 200ml को 200 लीटर पानी में मिलाकर प्रति एकड़ तुरंत स्प्रे करें।\n• **सावधानी:** नाइट्रोजन (यूरिया) का अतिरिक्त छिड़काव न करें।"
    },
    {
      "id": "agri_mustard_cultivation",
      "keywords": ["sarson", "mustard", "chepa", "mahu", "सरसों", "माहू", "सल्फर"],
      "title": "सरसों की खेती व माहू कीट नियंत्रण",
      "response": "🌱 **सरसों की खेती व माहू नियंत्रण:**\n• **माहू (चेपा) स्प्रे:** Dimethoate 30% EC @ 300ml प्रति एकड़।\n• **खाद:** 1 बैग SSP (50kg) + 25kg DAP + 10kg बेंटोनाइट सल्फर प्रति एकड़।"
    },
    {
      "id": "agri_sweet_corn_harvester",
      "keywords": ["sweet corn", "corn", "tractor", "makka", "cutter", "harvester", "कटाई"],
      "title": "स्वीट कॉर्न / मक्का कटाई हेतु ट्रैक्टर यंत्र",
      "response": "🚜 **स्वीट कॉर्न व मक्का कटाई के प्रमुख ट्रैक्टर यंत्र:**\n• **सिंगल / डबल रो फॉरेज हार्वेस्टर (Corn Forage Harvester):** मक्के के पूरे पौधे को काटकर साइलेज बनाने के लिए (45+ HP ट्रैक्टर PTO संचालित)।\n• **रोटरी कटर / सिकल बार मोवर (Mower):** जमीन से 2-3 इंच ऊपर से भुट्टे समेत डंठल काटने हेतु।"
    },
    {
      "id": "medical_snake_bite",
      "keywords": ["saanp", "snake", "snake bite", "सांप", "काटना", "anti snake venom", "asv"],
      "title": "सांप काटने पर आपातकालीन प्राथमिक उपचार",
      "response": "🚨 **सांप काटने पर जीवन रक्षक प्राथमिक उपचार:**\n1. पीड़ित को शांत रखें और काटे गए अंग को बिना हिलाए दिल के स्तर से नीचे रखें।\n2. **Anti-Snake Venom (ASV)** हेतु तुरंत नजदीकी सरकारी अस्पताल ले जाएं।\n3. ❌ चीरा न लगाएं, रस्सी न बांधें और झाड़-फूंक में समय बर्बाद न करें।"
    },
    {
      "id": "medical_fever",
      "keywords": ["bukhar", "fever", "paracetamol", "बुखार", "पैरासिटामोल"],
      "title": "तेज बुखार प्राथमिक उपचार",
      "response": "🌡️ **बुखार प्राथमिक उपचार:**\n• **दवा (वयस्क):** Paracetamol 500mg या 650mg आवश्यकतानुसार 6-8 घंटे में 1 गोली।\n• **देखभाल:** माथे और गर्दन पर सामान्य नल के पानी की पट्टी रखें (बर्फ न लगाएं)। ORS और पानी खूब पिलाएं।"
    },
    {
      "id": "iot_arduino_dht22",
      "keywords": ["arduino", "dht22", "dht11", "sensor", "oled", "आर्डुइनो"],
      "title": "Arduino DHT22 Sensor Wiring",
      "response": "⚙️ **Arduino Uno + DHT22 Connection:**\n• VCC -> 5V, GND -> GND, Data -> Pin D2 (with 10k pull-up resistor to 5V).\n• OLED Display: VCC -> 5V, GND -> GND, SCL -> A5, SDA -> A4."
    },
    {
      "id": "scheme_pm_kisan",
      "keywords": ["pm kisan", "samman nidhi", "6000", "पीएम किसान", "योजना"],
      "title": "PM-Kisan सम्मान निधि योजना",
      "response": "🏛️ **PM-Kisan सम्मान निधि (₹6,000 प्रति वर्ष):**\n• **लाभ:** ₹2,000 की 3 समान किस्तों में सीधे बैंक खाते (DBT) में।\n• **आवश्यक:** e-KYC पूरा होना, आधार बैंक लिंक, और भूलेख (खतौनी) सत्यापन।\n• **पोर्टल:** pmkisan.gov.in"
    }
  ];

  // Check which server URL is reachable
  Future<String?> checkServerConnectivity() async {
    final candidateUrls = [serverBaseUrl, emulatorBaseUrl, localhostUrl];
    for (final url in candidateUrls) {
      try {
        final resp = await http.get(Uri.parse('$url/api/tags')).timeout(const Duration(seconds: 1));
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

  // Offline Search Matching
  Map<String, dynamic>? searchOfflineKnowledge(String query) {
    final clean = query.toLowerCase().trim();
    final words = clean.split(RegExp(r'\s+')).where((w) => w.length > 2).toList();
    if (words.isEmpty) return null;

    Map<String, dynamic>? bestMatch;
    int bestScore = 0;

    for (final item in offlineKnowledge) {
      int score = 0;
      final title = (item['title'] as String).toLowerCase();
      if (title.contains(clean)) score += 80;

      final kws = item['keywords'] as List;
      for (final kw in kws) {
        final kwStr = kw.toString().toLowerCase();
        if (clean.contains(kwStr)) score += 50;
      }

      if (score > bestScore) {
        bestScore = score;
        bestMatch = item;
      }
    }

    if (bestScore >= 30) return bestMatch;
    return null;
  }

  // Stream Chat Response (combines live streaming from server with offline RAG fallback)
  Stream<String> generateStreamingChat(String prompt, {List<Map<String, String>> history = const []}) async* {
    await checkServerConnectivity();

    if (isServerOnline) {
      try {
        final request = http.Request('POST', Uri.parse('$activeServerUrl/api/chat'));
        request.headers['Content-Type'] = 'application/json';
        request.body = jsonEncode({
          'prompt': prompt,
          'session_id': 'mobile_session',
          'history': history
        });

        final streamedResponse = await request.send();
        await for (final chunk in streamedResponse.stream.transform(utf8.decoder)) {
          final lines = chunk.split('\n').where((l) => l.trim().isNotEmpty);
          for (final line in lines) {
            try {
              final packet = jsonDecode(line);
              if (packet['type'] == 'token' && packet['token'] != null) {
                yield packet['token'] as String;
              } else if (packet['type'] == 'done' && packet['final'] != null) {
                // Done
              }
            } catch (_) {
              yield line;
            }
          }
        }
        return;
      } catch (err) {
        // Fallback to offline on error
      }
    }

    // 100% Offline Local RAG Fallback
    final localMatch = searchOfflineKnowledge(prompt);
    if (localMatch != null) {
      yield localMatch['response'] as String;
    } else {
      yield '🌱 **ग्रामसेतु AI ऑफलाइन उत्तर:**\n\n'
          'आपके प्रश्न: "$prompt"\n'
          '• आवश्यक बीज दर, खाद की मात्रा या रोग नियंत्रण के लिए सटीक आंकड़े दर्ज करें।\n'
          '• इंटरनेट उपलब्ध होने पर यह पूर्ण Qwen 2.5 डीप रीजनिंग मॉडल से कनेक्ट हो जाता है।';
    }
  }
}
