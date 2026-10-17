import 'package:flutter/material.dart';

class KisanScreen extends StatefulWidget {
  const KisanScreen({super.key});

  @override
  State<KisanScreen> createState() => _KisanScreenState();
}

class _KisanScreenState extends State<KisanScreen> {
  String _selectedCrop = 'गेहूं';
  String _selectedSymptom = 'पीला रतुआ (हल्दी रोग)';
  String? _diagnosisResult;

  final Map<String, List<String>> _cropSymptoms = {
    'गेहूं': [
      'पीला रतुआ (हल्दी रोग)',
      'माहू (चेपा कीट)',
      'दीमक रोकथाम',
      'करनाल बंट',
    ],
    'धान': [
      'झुलसा रोग (Blight)',
      'तना छेदक (Stem Borer)',
      'भूरा फुदका कीट',
      'खैरा रोग (जिंक कमी)',
    ],
    'सरसों': [
      'माहू कीट (चेपा/एफिड)',
      'सफेद रोली (White Rust)',
      'तना गलन रोग',
    ],
    'कपास': [
      'गुलाबी सुंडी (Pink Bollworm)',
      'सफेद मक्खी (Whitefly)',
      'पत्ता मरोड़ वायरस',
    ],
    'आलू': [
      'अगेती/पछेती झुलसा (Blight)',
      'पत्ता मरोड़ रोग',
      'कंद सड़न रोग',
    ],
    'टमाटर': [
      'पत्ता मरोड़ (Leaf Curl)',
      'फल छेदक इल्ली',
      'झुलसा रोग (Blight)',
    ],
    'मिर्च': [
      'पत्ता मरोड़ (चुरड़ा-मुरड़ा)',
      'उकठा रोग (Wilt)',
      'फल गलन / डाईबैक',
    ],
  };

  final Map<String, Map<String, String>> _cures = {
    'गेहूं': {
      'पीला रतुआ (हल्दी रोग)': '🌾 **गेहूं पीला रतुआ (Yellow Rust) समाधान:**\n\n'
          '• **रासायनिक दवा:** Propiconazole 25% EC (Tilt / Bumper) @ 200ml प्रति 200 लीटर पानी में मिलाकर प्रति एकड़ तुरंत स्प्रे करें।\n'
          '• **गंभीर प्रकोप:** 12 दिन बाद Tebuconazole 25.9% EC @ 200ml/एकड़ का दूसरा छिड़काव करें।\n'
          '• **जैविक उपचार:** 2 लीटर 10 दिन पुरानी खट्टी छाछ को 150 लीटर पानी में मिलाकर छिड़कें।\n'
          '• **सावधानी:** यूरिया (नाइट्रोजन) का अतिरिक्त छिड़काव तुरंत बंद करें।',
      'माहू (चेपा कीट)': '🌾 **गेहूं में माहू कीट नियंत्रण:**\n\n'
          '• **दवा:** Thiamethoxam 25% WG @ 80 ग्राम प्रति एकड़ 150 लीटर पानी में स्प्रे करें।\n'
          '• **वैकल्पिक:** Imidacloprid 17.8% SL @ 60ml प्रति एकड़।\n'
          '• **जैविक:** 5ml/लीटर नीम का तेल (1500 PPM)।',
      'दीमक रोकथाम': '🌾 **गेहूं में दीमक नियंत्रण:**\n\n'
          '• **उपचार:** Fipronil 0.3% GR @ 8-10 किग्रा प्रति एकड़ पहली सिंचाई के समय रेत में मिलाकर डालें या Chlorpyrifos 20% EC @ 1 लीटर सिंचाई के पानी के साथ बहाएं।',
      'करनाल बंट': '🌾 **गेहूं करनाल बंट रोग:**\n\n'
          '• **लक्षण:** दानों में काले रंग का दुर्गंधयुक्त चूर्ण भरना।\n'
          '• **रोकथाम:** बाली निकलने के समय Propiconazole 25% EC @ 200ml/एकड़ का छिड़काव करें।'
    },
    'धान': {
      'झुलसा रोग (Blight)': '🌾 **धान का झुलसा रोग (Bacterial Blight):**\n\n'
          '• **दवा:** Copper Oxychloride 50% WP @ 500 ग्राम + Streptocycline @ 15 ग्राम प्रति एकड़ 200 लीटर पानी में स्प्रे करें।\n'
          '• **जैविक:** स्यूडोमोनास फ्लोरेसेंस (Pseudomonas) @ 1 किग्रा प्रति एकड़।\n'
          '• **सावधानी:** खेत से पानी का निकास करें और यूरिया बंद रखें।',
      'तना छेदक (Stem Borer)': '🌾 **धान में तना छेदक नियंत्रण:**\n\n'
          '• **दवा:** Cartap Hydrochloride 4G @ 7.5-10 किग्रा प्रति एकड़ खड़े पानी में बुरकें, या Chlorantraniliprole 18.5% SC (Coragen) @ 60ml प्रति एकड़ स्प्रे करें।',
      'भूरा फुदका कीट': '🌾 **धान में भूरा फुदका (BPH):**\n\n'
          '• **दवा:** Pymetrozine 50% WG (Chess) @ 120 ग्राम प्रति एकड़ पौधों की जड़ के पास स्प्रे करें।',
      'खैरा रोग (जिंक कमी)': '🌾 **धान में खैरा रोग (जिंक की कमी):**\n\n'
          '• **दवा:** 5 किग्रा जिंक सल्फेट (21%) + 2.5 किग्रा बुझा हुआ चूना या 1 किग्रा यूरिया को 200 लीटर पानी में घोलकर प्रति एकड़ छिड़कें।'
    },
    'सरसों': {
      'माहू कीट (चेपा/एफिड)': '🌼 **सरसों में माहू (चेपा) नियंत्रण:**\n\n'
          '• **दवा:** Dimethoate 30% EC (Rogor) @ 250ml या Thiamethoxam 25% WG @ 80 ग्राम प्रति एकड़ 150-200 लीटर पानी में स्प्रे करें।\n'
          '• **जैविक:** 5% नीम गिरी अर्क (NSKE) या 5ml नीम का तेल प्रति लीटर पानी।\n'
          '• **समय:** छिड़काव हमेशा दोपहर बाद 3 बजे के बाद करें जब मधुमक्खियां कम हों।',
      'सफेद रोली (White Rust)': '🌼 **सरसों में सफेद रोली (White Rust):**\n\n'
          '• **दवा:** Mancozeb 75% WP @ 600 ग्राम या Metalaxyl 8% + Mancozeb 64% WP (Ridomil) @ 400 ग्राम प्रति एकड़ स्प्रे करें।',
      'तना गलन रोग': '🌼 **सरसों में तना गलन (Sclerotinia):**\n\n'
          '• **दवा:** Carbendazim 50% WP (Bavistin) @ 250 ग्राम प्रति एकड़ 200 लीटर पानी में छिड़कें।'
    },
    'कपास': {
      'गुलाबी सुंडी (Pink Bollworm)': '🌿 **कपास गुलाबी सुंडी नियंत्रण:**\n\n'
          '• **दवा:** Emamectin Benzoate 5% SG @ 100 ग्राम प्रति एकड़ या Profenofos 50% EC @ 400ml स्प्रे करें।\n'
          '• **ट्रैप:** खेत में 5-8 फेरोमोन ट्रैप (Pheromone Traps) प्रति एकड़ अनिवार्य रूप से लगाएं।',
      'सफेद मक्खी (Whitefly)': '🌿 **कपास सफेद मक्खी नियंत्रण:**\n\n'
          '• **दवा:** Diafenthiuron 50% WP (Pegasus) @ 250 ग्राम या Pyriproxyfen 10% EC @ 400ml प्रति एकड़ 200 लीटर पानी में स्प्रे करें।\n'
          '• **ट्रैप:** पीले चिपचिपे कार्ड (Yellow Sticky Traps) 15-20 प्रति एकड़ लगाएं।',
      'पत्ता मरोड़ वायरस': '🌿 **कपास पत्ता मरोड़ (CLCuV):**\n\n'
          '• सफेद मक्खी ही इस वायरस को फैलाती है। सफेद मक्खी का तुरंत नियंत्रण करें और रोगग्रस्त पौधों को उखाड़कर नष्ट करें।'
    },
    'आलू': {
      'अगेती/पछेती झुलसा (Blight)': '🥔 **आलू में झुलसा रोग (Late Blight):**\n\n'
          '• **दवा:** Cymoxanil 8% + Mancozeb 64% WP (Sectin) @ 600 ग्राम प्रति एकड़ या Metalaxyl + Mancozeb (Ridomil MZ) @ 500 ग्राम प्रति एकड़ स्प्रे करें।\n'
          '• **बचाव:** Mancozeb 75% WP @ 2.5 ग्राम/लीटर का 10 दिन के अंतराल पर छिड़काव जारी रखें।',
      'पत्ता मरोड़ रोग': '🥔 **आलू पत्ता मरोड़ वायरस:**\n\n'
          '• माहू/एफिड कीट नियंत्रण हेतु Imidacloprid 17.8% SL @ 60ml प्रति एकड़ छिड़कें।',
      'कंद सड़न रोग': '🥔 **आलू कंद सड़न (Soft Rot):**\n\n'
          '• बुवाई से पहले बीजों को Trichoderma viride @ 5 ग्राम/किग्रा या Carbendazim @ 2 ग्राम/किग्रा से उपचारित करें।'
    },
    'टमाटर': {
      'पत्ता मरोड़ (Leaf Curl)': '🍅 **टमाटर पत्ता मरोड़ (Leaf Curl Virus):**\n\n'
          '• **सफेद मक्खी नियंत्रण:** Acetamiprid 20% SP @ 80 ग्राम प्रति एकड़ या Imidacloprid 17.8% SL @ 60ml प्रति एकड़।\n'
          '• **जैविक:** नीम का तेल 5ml/लीटर + खट्टी छाछ का छिड़काव।',
      'फल छेदक इल्ली': '🍅 **टमाटर फल छेदक इल्ली:**\n\n'
          '• **दवा:** Spinosad 45% SC @ 75ml प्रति एकड़ या Chlorantraniliprole 18.5% SC @ 60ml प्रति एकड़।',
      'झुलसा रोग (Blight)': '🍅 **टमाटर झुलसा रोग:**\n\n'
          '• **दवा:** Mancozeb 75% WP @ 500 ग्राम या Copper Oxychloride @ 500 ग्राम प्रति एकड़ छिड़कें।'
    },
    'मिर्च': {
      'पत्ता मरोड़ (चुरड़ा-मुरड़ा)': '🌶️ **मिर्च का चुरड़ा-मुरड़ा (थ्रिप्स व माइट्स):**\n\n'
          '• **दवा:** Fipronil 5% SC @ 300ml प्रति एकड़ या Diafenthiuron 50% WP @ 250 ग्राम प्रति एकड़ 200 लीटर पानी में स्प्रे करें।\n'
          '• **माइट्स के लिए:** Spiromesifen 22.9% SC @ 150ml प्रति एकड़ छिड़कें।',
      'उकठा रोग (Wilt)': '🌶️ **मिर्च में उकठा रोग (Wilt):**\n\n'
          '• **जैविक उपचार:** Trichoderma viride @ 2 किग्रा को 50 किग्रा गोबर की खाद में मिलाकर जड़ों के पास डालें।\n'
          '• **ड्रेंचिंग:** Copper Oxychloride @ 3 ग्राम/लीटर पानी से पौधों की जड़ों की ड्रेंचिंग करें।',
      'फल गलन / डाईबैक': '🌶️ **मिर्च फल गलन (Anthracnose / Dieback):**\n\n'
          '• **दवा:** Azoxystrobin 23% SC @ 200ml या Difenoconazole 25% EC @ 150ml प्रति एकड़ स्प्रे करें।'
    },
  };

  void _onCropChanged(String crop) {
    setState(() {
      _selectedCrop = crop;
      final symptoms = _cropSymptoms[crop] ?? ['सामान्य लक्षण'];
      _selectedSymptom = symptoms.first;
      _diagnosisResult = null;
    });
  }

  void _diagnose() {
    final cureText = _cures[_selectedCrop]?[_selectedSymptom] ??
        '🌾 **$_selectedCrop - $_selectedSymptom:**\n• नीम का तेल (1500 PPM) 5ml प्रति लीटर पानी में मिलाकर स्प्रे करें।\n• संतुलित खाद व सिंचाई प्रबंधन रखें।';

    setState(() {
      _diagnosisResult = cureText;
    });
  }

  @override
  Widget build(BuildContext context) {
    final availableSymptoms = _cropSymptoms[_selectedCrop] ?? ['सामान्य लक्षण'];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        title: const Text('🌾 किसान मित्र (Crop Doctor)', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            color: const Color(0xFF1E293B),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('🩺 फसल रोग निदान (Symptom Doctor)', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 14),
                  DropdownButtonFormField<String>(
                    value: _selectedCrop,
                    dropdownColor: const Color(0xFF1E293B),
                    decoration: const InputDecoration(
                      labelText: 'फसल चुनें',
                      labelStyle: TextStyle(color: Color(0xFF94A3B8)),
                      border: OutlineInputBorder(),
                    ),
                    items: _cropSymptoms.keys.map((c) => DropdownMenuItem(value: c, child: Text(c, style: const TextStyle(color: Colors.white)))).toList(),
                    onChanged: (val) {
                      if (val != null) _onCropChanged(val);
                    },
                  ),
                  const SizedBox(height: 14),
                  DropdownButtonFormField<String>(
                    value: _selectedSymptom,
                    dropdownColor: const Color(0xFF1E293B),
                    decoration: const InputDecoration(
                      labelText: 'लक्षण व रोग चुनें',
                      labelStyle: TextStyle(color: Color(0xFF94A3B8)),
                      border: OutlineInputBorder(),
                    ),
                    items: availableSymptoms.map((s) => DropdownMenuItem(value: s, child: Text(s, style: const TextStyle(color: Colors.white)))).toList(),
                    onChanged: (val) => setState(() => _selectedSymptom = val!),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF15803D),
                      minimumSize: const Size.fromHeight(44),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                    onPressed: _diagnose,
                    child: const Text('🔍 तुरंत सटीक उपचार व दवा देखें', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  ),
                  if (_diagnosisResult != null) ...[
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: const Color(0xFF0F172A),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: const Color(0xFF22C55E), width: 1.2),
                      ),
                      child: Text(_diagnosisResult!, style: const TextStyle(color: Colors.white, height: 1.5, fontSize: 13.5)),
                    )
                  ]
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            color: const Color(0xFF1E293B),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            child: const Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('🌱 200L देसी जीवामृत बनाने की विधि', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFF4ADE80))),
                  SizedBox(height: 8),
                  Text('• 10 किग्रा देसी गाय का गोबर + 10 लीटर गोमूत्र + 2 किग्रा पुराना गुड़ + 2 किग्रा बेसन + 1 मुट्ठी खेत की सजीव मिट्टी को 180 लीटर पानी में घोलकर 48 घंटे छाया में रखें। सुबह-शाम डंडे से चलाएं।\n• 1 एकड़ में सिंचाई के पानी के साथ बहाएं। मिट्टी की उर्वरता और केंचुआ संख्या कई गुना बढ़ जाएगी।',
                      style: TextStyle(color: Color(0xFFCBD5E1), fontSize: 13, height: 1.5)),
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
