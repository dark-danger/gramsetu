import 'package:flutter/material.dart';

class YojanaScreen extends StatelessWidget {
  const YojanaScreen({super.key});

  final List<Map<String, String>> _schemes = const [
    {
      'title': 'PM-किसान सम्मान निधि',
      'benefit': '₹6,000 / वर्ष',
      'desc': '3 किस्तों में ₹2000-₹2000 सीधे बैंक खाते में। e-KYC व भूलेख अंकन अनिवार्य।'
    },
    {
      'title': 'आयुष्मान भारत (PM-JAY)',
      'benefit': '₹5 लाख मुफ्त इलाज',
      'desc': 'सूचीबद्ध निजी व सरकारी अस्पतालों में कैशलेस इलाज। 70+ बुजुर्गों के लिए वय वंदना कार्ड।'
    },
    {
      'title': 'किसान क्रेडिट कार्ड (KCC)',
      'benefit': '4% रियायती ब्याज',
      'desc': '₹3 लाख तक का सस्ता कृषि ऋण। ₹1.60 लाख तक बिना ज़मीन बंधक।'
    },
    {
      'title': 'PM-कुसुम सोलर पंप योजना',
      'benefit': '60-90% सब्सिडी',
      'desc': 'खेतों में सिंचाई हेतु 3HP से 10HP सोलर पंप पर भारी सरकारी अनुदान।'
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        title: const Text('🏛️ सरकारी योजनाएं (Govt Schemes)', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _schemes.length,
        itemBuilder: (context, idx) {
          final s = _schemes[idx];
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            color: const Color(0xFF1E293B),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(s['title']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Colors.white)),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: const Color(0xFF14532D),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(s['benefit']!, style: const TextStyle(color: Color(0xFF4ADE80), fontWeight: FontWeight.bold, fontSize: 11)),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Text(s['desc']!, style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 13, height: 1.4)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
