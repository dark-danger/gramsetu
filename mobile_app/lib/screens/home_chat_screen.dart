import 'package:flutter/material.dart';
import '../services/ai_engine_service.dart';

class HomeChatScreen extends StatefulWidget {
  const HomeChatScreen({super.key});

  @override
  State<HomeChatScreen> createState() => _HomeChatScreenState();
}

class _HomeChatScreenState extends State<HomeChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final AIEngineService _aiService = AIEngineService();

  final List<Map<String, String>> _messages = [
    {
      'role': 'assistant',
      'content': 'नमस्ते! मैं **ग्रामसेतु AI** हूँ।\nबिना इंटरनेट के खेती, खाद-बीज, सरकारी योजनाएं, प्राथमिक उपचार व IoT हार्डवेयर के सटीक उत्तर प्राप्त करें।\n\nलिखकर या बोलकर पूछें!'
    }
  ];

  bool _isGenerating = false;
  String _currentServerStatus = 'Checking server...';

  @override
  void initState() {
    super.initState();
    _checkServer();
  }

  Future<void> _checkServer() async {
    final url = await _aiService.checkServerConnectivity();
    if (mounted) {
      setState(() {
        _currentServerStatus = url != null ? '⚡ Qwen 2.5 Live ($url)' : '🌱 100% Offline RAG Engine';
      });
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 250),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _sendMessage(String text) async {
    final prompt = text.trim();
    if (prompt.isEmpty || _isGenerating) return;

    _controller.clear();
    setState(() {
      _messages.add({'role': 'user', 'content': prompt});
      _messages.add({'role': 'assistant', 'content': '...'});
      _isGenerating = true;
    });
    _scrollToBottom();

    // Prepare history
    final history = _messages
        .take(_messages.length - 2)
        .map((m) => {'role': m['role']!, 'content': m['content']!})
        .toList();

    String accumulated = '';
    final lastIndex = _messages.length - 1;

    try {
      await for (final token in _aiService.generateStreamingChat(prompt, history: history)) {
        if (!mounted) break;
        accumulated += token;
        setState(() {
          _messages[lastIndex]['content'] = accumulated;
        });
        _scrollToBottom();
      }
    } catch (e) {
      setState(() {
        _messages[lastIndex]['content'] = '❌ Error: $e';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isGenerating = false;
        });
        _scrollToBottom();
      }
    }
  }

  void _showServerSettingsModal() {
    final textController = TextEditingController(text: _aiService.activeServerUrl);
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E293B),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '⚙️ GramSetu Server Connection',
                style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              const Text(
                'Enter local PC / Laptop IP (e.g. http://192.168.1.59:8000 or http://10.0.2.2:8000 for Emulator):',
                style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12),
              ),
              const SizedBox(height: 10),
              TextField(
                controller: textController,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  filled: true,
                  fillColor: const Color(0xFF0F172A),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                ),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF10B981),
                  minimumSize: const Size(double.infinity, 44),
                ),
                onPressed: () {
                  AIEngineService.serverBaseUrl = textController.text.trim();
                  _aiService.activeServerUrl = textController.text.trim();
                  Navigator.pop(ctx);
                  _checkServer();
                },
                child: const Text('Save & Reconnect', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
              )
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0B0F17),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        elevation: 0,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text('🌾 ', style: TextStyle(fontSize: 18)),
                const Text('GramSetu AI', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.white)),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.settings, color: Colors.white70, size: 20),
                  onPressed: _showServerSettingsModal,
                ),
              ],
            ),
            Text(
              _currentServerStatus,
              style: const TextStyle(fontSize: 11, color: Color(0xFF34D399)),
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(14),
              itemCount: _messages.length,
              itemBuilder: (context, idx) {
                final msg = _messages[idx];
                final isBot = msg['role'] == 'assistant';
                return Align(
                  alignment: isBot ? Alignment.centerLeft : Alignment.centerRight,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                    constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.84),
                    decoration: BoxDecoration(
                      color: isBot ? const Color(0xFF1E293B) : const Color(0xFF047857),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: isBot ? const Color(0xFF334155) : const Color(0xFF10B981),
                      ),
                    ),
                    child: Text(
                      msg['content']!,
                      style: const TextStyle(color: Colors.white, fontSize: 14, height: 1.45),
                    ),
                  ),
                );
              },
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
            decoration: const BoxDecoration(
              color: Color(0xFF0F172A),
              border: Border(top: BorderSide(color: Color(0xFF1E293B))),
            ),
            child: SafeArea(
              child: Row(
                children: [
                  Expanded(
                    child: Container(
                      decoration: BoxDecoration(
                        color: const Color(0xFF1E293B),
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(color: const Color(0xFF334155)),
                      ),
                      child: TextField(
                        controller: _controller,
                        style: const TextStyle(color: Colors.white, fontSize: 14),
                        decoration: const InputDecoration(
                          hintText: 'पूछें: गेहूं, खाद, दवाई, IoT, योजना...',
                          hintStyle: TextStyle(color: Color(0xFF64748B), fontSize: 13),
                          contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                          border: InputBorder.none,
                        ),
                        onSubmitted: _sendMessage,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  CircleAvatar(
                    backgroundColor: const Color(0xFF10B981),
                    radius: 22,
                    child: IconButton(
                      icon: const Icon(Icons.send_rounded, color: Colors.white, size: 20),
                      onPressed: () => _sendMessage(_controller.text),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
