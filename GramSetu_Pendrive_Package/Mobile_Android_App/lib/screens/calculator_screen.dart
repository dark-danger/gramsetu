import 'package:flutter/material.dart';

class CalculatorScreen extends StatefulWidget {
  const CalculatorScreen({super.key});

  @override
  State<CalculatorScreen> createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  double _acres = 1.0;

  @override
  Widget build(BuildContext context) {
    final puccaBigha = (_acres * 1.6).toStringAsFixed(2);
    final kacchaBigha = (_acres * 4.8).toStringAsFixed(2);
    final sqYards = (_acres * 4840).round();

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        title: const Text('📐 ज़मीन नाप व खाद कैलकुलेटर', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            color: const Color(0xFF1E293B),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('📐 एकड़ ⇄ बीघा परिवर्तक (Land Converter)', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 12),
                  TextField(
                    keyboardType: TextInputType.number,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      labelText: 'रकबा (एकड़ में दर्ज करें):',
                      border: OutlineInputBorder(),
                    ),
                    onChanged: (val) => setState(() => _acres = double.tryParse(val) ?? 1.0),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      _buildUnitBox('$puccaBigha बीघा', 'पक्का बीघा (UP/Raj)'),
                      const SizedBox(width: 8),
                      _buildUnitBox('$kacchaBigha बीघा', 'कच्चा बीघा (UP)'),
                    ],
                  ),
                  const SizedBox(height: 8),
                  _buildUnitBox('$sqYards वर्ग गज', 'कुल क्षेत्रफल (Sq. Yards)'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            color: const Color(0xFF1E293B),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('🧪 गेहूं हेतु खाद की मात्रा ($_acres एकड़ के लिए):', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFF4ADE80))),
                  const SizedBox(height: 10),
                  Text('• DAP (18:46:0): ${(_acres * 1.0).toStringAsFixed(1)} बैग (50 किग्रा)', style: const TextStyle(color: Colors.white, fontSize: 13)),
                  const SizedBox(height: 6),
                  Text('• यूरिया: ${(_acres * 2.0).toStringAsFixed(1)} बैग (45 किग्रा)', style: const TextStyle(color: Colors.white, fontSize: 13)),
                  const SizedBox(height: 6),
                  Text('• पोटाश (MOP): ${(_acres * 0.5).toStringAsFixed(1)} बैग (50 किग्रा)', style: const TextStyle(color: Colors.white, fontSize: 13)),
                ],
              ),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildUnitBox(String val, String label) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: const Color(0xFF0F172A),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: const Color(0xFF334155)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(val, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFFA78BFA))),
            const SizedBox(height: 2),
            Text(label, style: const TextStyle(fontSize: 11, color: Color(0xFF94A3B8))),
          ],
        ),
      ),
    );
  }
}
