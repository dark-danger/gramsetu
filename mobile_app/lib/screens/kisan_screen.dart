import 'package:flutter/material.dart';

class KisanScreen extends StatefulWidget {
  const KisanScreen({super.key});

  @override
  State<KisanScreen> createState() => _KisanScreenState();
}

class _KisanScreenState extends State<KisanScreen> {
  String _selectedCrop = 'गेहूं';
  String _selectedSymptom = 'पीला रतुआ';
  String? _diagnosisResult;

  void _diagnose() {
    setState(() {
      _diagnosisResult = '🌾 **गेहूं पीला रतुआ समाधान:**\n1. प्रोपिकोनाजोल 25% EC (Tilt) 200ml / 200L पानी प्रति एकड़ स्प्रे करें।\n2. जैविक: 2L खट्टी छाछ + 150L पानी।\n3. अधिक यूरिया डालने से बचें।';
    });
  }

  @override
  Widget build(BuildContext context) {
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
                  const SizedBox(height: 12),
                  DropdownButtonFormField<String>(
                    value: _selectedCrop,
                    dropdownColor: const Color(0xFF1E293B),
                    decoration: const InputDecoration(labelText: 'फसल चुनें', border: OutlineInputBorder()),
                    items: ['गेहूं', 'धान', 'सरसों', 'कपास', 'आलू', 'टमाटर', 'मिर्च'].map((c) => DropdownMenuItem(value: c, child: Text(c))).toList(),
                    onChanged: (val) => setState(() => _selectedCrop = val!),
                  ),
                  const SizedBox(height: 12),
                  DropdownButtonFormField<String>(
                    value: _selectedSymptom,
                    dropdownColor: const Color(0xFF1E293B),
                    decoration: const InputDecoration(labelText: 'लक्षण चुनें', border: OutlineInputBorder()),
                    items: ['पीला रतुआ', 'माहू कीट', 'झुलसा रोग', 'पत्ता मरोड़'].map((s) => DropdownMenuItem(value: s, child: Text(s))).toList(),
                    onChanged: (val) => setState(() => _selectedSymptom = val!),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF15803D),
                      minimumSize: const Size.fromHeight(44),
                    ),
                    onPressed: _diagnose,
                    child: const Text('🔍 तुरंत उपचार देखें', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  ),
                  if (_diagnosisResult != null) ...[
                    const SizedBox(height: 14),
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: const Color(0xFF0F172A),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: const Color(0xFF22C55E)),
                      ),
                      child: Text(_diagnosisResult!, style: const TextStyle(color: Colors.white, height: 1.4)),
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
                  Text('• 10 किग्रा देसी गोबर + 10 लीटर गोमूत्र + 2 किग्रा गुड़ + 2 किग्रा बेसन + 1 मुट्ठी सजीव मिट्टी को 180 लीटर पानी में 48 घंटे रखें। 1 एकड़ में बहाएं।', style: TextStyle(color: Colors.white, fontSize: 13, height: 1.4)),
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
