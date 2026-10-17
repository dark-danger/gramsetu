import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
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

  late List<Map<String, String>> _messages;

  bool _isGenerating = false;
  String _currentServerStatus = 'Checking server...';

  @override
  void initState() {
    super.initState();
    _resetWelcomeMessage();
    _checkServer();
  }

  void _resetWelcomeMessage() {
    String welcome;
    if (_aiService.currentLanguage == AppLanguage.english) {
      welcome = 'Hello! I am **GramSetu AI**.\n\n'
          'Your 100% offline assistant for farming, fertilizers, machinery, government schemes, and rural healthcare.\n\n'
          '👉 Ask any question in English by typing or speaking!';
    } else if (_aiService.currentLanguage == AppLanguage.hinglish) {
      welcome = 'Namaste! Main **GramSetu AI** hoon.\n\n'
          'Bina internet ke kheti, khad, krishi yantra, sarkari yojanaayein aur swasthya ke sahi uttar paayein.\n\n'
          '👉 Apna sawaal Hinglish ya Hindi me likhkar poochein!';
    } else {
      welcome = 'नमस्ते! मैं **ग्रामसेतु AI** हूँ।\n\n'
          'बिना इंटरनेट के खेती, खाद-बीज, कृषि यंत्र, सरकारी योजनाएं व प्राथमिक उपचार के सटीक उत्तर प्राप्त करें।\n\n'
          '👉 अपना सवाल नीचे लिखकर या बोलकर पूछें!';
    }

    _messages = [
      {'role': 'assistant', 'content': welcome}
    ];
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

  String _getLanguageLabel() {
    switch (_aiService.currentLanguage) {
      case AppLanguage.english:
        return 'English';
      case AppLanguage.hinglish:
        return 'Hinglish';
      case AppLanguage.hindi:
      default:
        return 'हिंदी';
    }
  }

  void _showLanguageSelector() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E293B),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Row(
                children: [
                  Icon(Icons.language, color: Color(0xFF4ADE80), size: 24),
                  SizedBox(width: 10),
                  Text(
                    'भाषा चुनें / Select Language',
                    style: TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
              const SizedBox(height: 18),
              _buildLanguageOption(
                title: '🇮🇳 हिंदी (Hindi)',
                subtitle: 'खेती, खाद व योजनाओं की पूरी जानकारी हिंदी में',
                lang: AppLanguage.hindi,
              ),
              const SizedBox(height: 10),
              _buildLanguageOption(
                title: '🇬🇧 English',
                subtitle: 'All farming advisories & tools in English',
                lang: AppLanguage.english,
              ),
              const SizedBox(height: 10),
              _buildLanguageOption(
                title: '🔤 Hinglish',
                subtitle: 'Kheti aur sarkari yojanaayein Hinglish me',
                lang: AppLanguage.hinglish,
              ),
              const SizedBox(height: 16),
            ],
          ),
        );
      },
    );
  }

  Widget _buildLanguageOption({
    required String title,
    required String subtitle,
    required AppLanguage lang,
  }) {
    final isSelected = _aiService.currentLanguage == lang;
    return InkWell(
      onTap: () {
        setState(() {
          _aiService.setLanguage(lang);
          _messages.add({
            'role': 'assistant',
            'content': lang == AppLanguage.english
                ? '🌐 **Language switched to English!**\nHow can I help you with farming, crops, tools, or schemes today?'
                : lang == AppLanguage.hinglish
                    ? '🌐 **Language switched to Hinglish!**\nAb aap kheti, khad ya yojanao ke bare me Hinglish me pooch sakte hain.'
                    : '🌐 **भाषा बदलकर हिंदी कर दी गई है!**\nआप खेती, फसल, खाद या योजनाओं के बारे में क्या पूछना चाहते हैं?'
          });
        });
        Navigator.pop(context);
        _scrollToBottom();
      },
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: isSelected ? const Color(0xFF0F2E23) : const Color(0xFF0F172A),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected ? const Color(0xFF22C55E) : const Color(0xFF334155),
            width: isSelected ? 1.8 : 1,
          ),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      color: isSelected ? const Color(0xFF4ADE80) : Colors.white,
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 3),
                  Text(
                    subtitle,
                    style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 12),
                  ),
                ],
              ),
            ),
            if (isSelected)
              const Icon(Icons.check_circle, color: Color(0xFF22C55E), size: 22),
          ],
        ),
      ),
    );
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
                // Language Switcher Badge
                InkWell(
                  onTap: _showLanguageSelector,
                  borderRadius: BorderRadius.circular(16),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: const Color(0xFF10B981), width: 1.2),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.language, size: 15, color: Color(0xFF34D399)),
                        const SizedBox(width: 4),
                        Text(
                          _getLanguageLabel(),
                          style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                        ),
                        const Icon(Icons.arrow_drop_down, size: 16, color: Colors.white70),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 4),
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
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
              itemCount: _messages.length,
              itemBuilder: (context, idx) {
                final msg = _messages[idx];
                final isBot = msg['role'] == 'assistant';
                return Align(
                  alignment: isBot ? Alignment.centerLeft : Alignment.centerRight,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 14),
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                    constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.88),
                    decoration: BoxDecoration(
                      color: isBot ? const Color(0xFF1E293B) : const Color(0xFF065F46),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: isBot ? const Color(0xFF334155) : const Color(0xFF10B981),
                        width: 1.1,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.2),
                          blurRadius: 4,
                          offset: const Offset(0, 2),
                        )
                      ],
                    ),
                    child: isBot
                        ? MarkdownBody(
                            data: msg['content']!,
                            selectable: true,
                            styleSheet: MarkdownStyleSheet(
                              p: const TextStyle(color: Color(0xFFF1F5F9), fontSize: 14, height: 1.55),
                              strong: const TextStyle(color: Color(0xFF86EFAC), fontWeight: FontWeight.bold),
                              h1: const TextStyle(color: Color(0xFF4ADE80), fontSize: 17, fontWeight: FontWeight.bold, height: 1.4),
                              h2: const TextStyle(color: Color(0xFF4ADE80), fontSize: 16, fontWeight: FontWeight.bold, height: 1.4),
                              h3: const TextStyle(color: Color(0xFF6EE7B7), fontSize: 15, fontWeight: FontWeight.bold, height: 1.3),
                              listBullet: const TextStyle(color: Color(0xFF4ADE80), fontSize: 14),
                              code: const TextStyle(backgroundColor: Color(0xFF0F172A), color: Color(0xFF38BDF8), fontSize: 12),
                              codeblockDecoration: BoxDecoration(
                                color: const Color(0xFF0F172A),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: const Color(0xFF334155)),
                              ),
                              blockquote: const TextStyle(color: Color(0xFF94A3B8), fontStyle: FontStyle.italic),
                            ),
                          )
                        : Text(
                            msg['content']!,
                            style: const TextStyle(color: Colors.white, fontSize: 14.5, height: 1.4),
                          ),
                  ),
                );
              },
            ),
          ),
          // Quick prompt chips
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            child: Row(
              children: [
                _buildQuickChip('🚜 Rabi Farming Tools', 'farming tool bta ravi crop grow krna k liye'),
                _buildQuickChip('🧪 3 Acre Khad', '3 acre gehu me kitna khad lagega'),
                _buildQuickChip('🏛️ PM-Kisan', 'pm kisan samman nidhi'),
                _buildQuickChip('🌾 Peela Ratua', 'gehu me peela ratua rog'),
              ],
            ),
          ),
          // Input Box
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
                        decoration: InputDecoration(
                          hintText: _aiService.currentLanguage == AppLanguage.english
                              ? 'Ask: Tools, crops, fertilizer, schemes...'
                              : 'पूछें: गेहूं, खाद, दवाई, कृषि यंत्र, योजना...',
                          hintStyle: const TextStyle(color: Color(0xFF64748B), fontSize: 13),
                          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
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

  Widget _buildQuickChip(String label, String prompt) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: ActionChip(
        backgroundColor: const Color(0xFF1E293B),
        side: const BorderSide(color: Color(0xFF334155)),
        label: Text(label, style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11)),
        onPressed: () => _sendMessage(prompt),
      ),
    );
  }
}
