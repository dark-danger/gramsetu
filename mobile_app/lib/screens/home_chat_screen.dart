import 'package:flutter/material.dart';

class HomeChatScreen extends StatefulWidget {
  const HomeChatScreen({super.key});

  @override
  State<HomeChatScreen> createState() => _HomeChatScreenState();
}

class _HomeChatScreenState extends State<HomeChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [
    {
      'sender': 'bot',
      'text': 'नमस्ते! मैं **ग्रामसेतु AI** हूँ। बिना इंटरनेट के खेती, योजना, स्वास्थ्य व ज़मीन नाप के सवाल पूछें। माइक दबाकर बोलें या लिखें।'
    }
  ];
  bool _isListening = false;

  void _sendMessage(String text) {
    if (text.trim().isEmpty) return;
    setState(() {
      _messages.add({'sender': 'user', 'text': text});
      _messages.add({
        'sender': 'bot',
        'text': '🌱 **ग्रामसेतु समाधान:**\nआपके प्रश्न पर ऑन-डिवाइस Qwen 2.5 इंजन द्वारा सटीक ग्रामीण सलाह तैयार की जा रही है।'
      });
    });
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        title: Row(
          children: const [
            Text('🌾 ', style: TextStyle(fontSize: 20)),
            Text('GramSetu AI', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            Spacer(),
            Chip(
              label: Text('⚡ 100% OFFLINE', style: TextStyle(fontSize: 10, color: Color(0xFF4ADE80))),
              backgroundColor: Color(0xFF14532D),
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(14),
              itemCount: _messages.length,
              itemBuilder: (context, idx) {
                final msg = _messages[idx];
                final isBot = msg['sender'] == 'bot';
                return Align(
                  alignment: isBot ? Alignment.centerLeft : Alignment.centerRight,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    padding: const EdgeInsets.all(12),
                    constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.82),
                    decoration: BoxDecoration(
                      color: isBot ? const Color(0xFF1E293B) : const Color(0xFF1E3A8A),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(
                        color: isBot ? const Color(0xFF334155) : const Color(0xFF2563EB),
                      ),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          msg['text']!,
                          style: const TextStyle(color: Colors.white, fontSize: 13, height: 1.4),
                        ),
                        if (isBot) ...[
                          const SizedBox(height: 6),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: const [
                              Text('⚡ Qwen 2.5 Engine', style: TextStyle(fontSize: 10, color: Color(0xFF4ADE80))),
                              Text('🔊 सुनें', style: TextStyle(fontSize: 11, color: Color(0xFF94A3B8))),
                            ],
                          )
                        ]
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
            decoration: const BoxDecoration(
              color: Color(0xFF0F172A),
              border: Border(top: BorderSide(color: Color(0xFF334155))),
            ),
            child: Row(
              children: [
                GestureDetector(
                  onTap: () => setState(() => _isListening = !_isListening),
                  child: Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      color: _isListening ? Colors.red : const Color(0xFF15803D),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.mic, color: Colors.white),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: const TextStyle(color: Colors.white, fontSize: 14),
                    decoration: const InputDecoration(
                      hintText: 'माइक दबाएं या यहाँ लिखें...',
                      hintStyle: TextStyle(color: Color(0xFF94A3B8)),
                      border: InputBorder.none,
                    ),
                    onSubmitted: _sendMessage,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send, color: Color(0xFF4ADE80)),
                  onPressed: () => _sendMessage(_controller.text),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
