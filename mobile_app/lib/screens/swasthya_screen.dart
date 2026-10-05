import 'package:flutter/material.dart';

class SwasthyaScreen extends StatelessWidget {
  const SwasthyaScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        title: const Text('🩺 स्वास्थ्य व SOS हेल्पलाइन', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text('🚨 आपातकालीन टोल-फ्री हेल्पलाइन:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Color(0xFFF87171))),
          const SizedBox(height: 10),
          Row(
            children: [
              _buildSosCard('108', 'एम्बुलेंस'),
              const SizedBox(width: 8),
              _buildSosCard('102', 'जननी सेवा'),
              const SizedBox(width: 8),
              _buildSosCard('112', 'आपातकाल'),
            ],
          ),
          const SizedBox(height: 16),
          Card(
            color: const Color(0xFF1E293B),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: const Padding(
              padding: EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('🐍 सांप काटने पर प्राथमिक उपचार', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Colors.white)),
                  SizedBox(height: 8),
                  Text('1. मरीज को शांत रखें और अंग को बिल्कुल न हिलाएं (लकड़ी की पट्टी बांधें)।\n2. चीरा न लगाएं और मुंह से न चूसें।\n3. तुरंत सरकारी अस्पताल जाकर Anti-Snake Venom (ASV) का मुफ्त टीका लगवाएं।', style: TextStyle(color: Color(0xFFCBD5E1), fontSize: 13, height: 1.5)),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          Card(
            color: const Color(0xFF1E293B),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: const Padding(
              padding: EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('💧 घर पर ORS घोल बनाने की विधि', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Colors.white)),
                  SizedBox(height: 8),
                  Text('1 लीटर उबले ठंडे पानी में 6 छोटी चम्मच चीनी + आधा चम्मच नमक घोलें। दस्त व उल्टी में जीवनरक्षक।', style: TextStyle(color: Color(0xFFCBD5E1), fontSize: 13, height: 1.5)),
                ],
              ),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildSosCard(String number, String label) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(
          color: const Color(0xFF7F1D1D).withOpacity(0.4),
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: const Color(0xFFEF4444)),
        ),
        child: Column(
          children: [
            Text(number, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFFFCA5A5))),
            const SizedBox(height: 2),
            Text(label, style: const TextStyle(fontSize: 11, color: Color(0xFFCBD5E1))),
          ],
        ),
      ),
    );
  }
}
