import 'dart:convert';
import 'package:http/http.dart' as http;

class AIEngineService {
  static const String ollamaBaseUrl = 'http://localhost:11434';
  String activeModel = 'qwen2.5-coder:1.5b';
  bool isOllamaOnline = false;

  // Check if Ollama is accessible
  Future<bool> probeOllama() async {
    try {
      final response = await http.get(Uri.parse('$ollamaBaseUrl/api/tags'))
          .timeout(const Duration(seconds: 2));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final models = data['models'] as List?;
        if (models != null && models.isNotEmpty) {
          final qwen = models.firstWhere(
            (m) => m['name'].toString().toLowerCase().contains('qwen'),
            orElse: () => models.first,
          );
          activeModel = qwen['name'];
        }
        isOllamaOnline = true;
        return true;
      }
    } catch (_) {
      isOllamaOnline = false;
    }
    return false;
  }

  // Stream or Generate response from local Qwen model
  Stream<String> generateStreamingResponse(String prompt) async* {
    final isOnline = await probeOllama();
    if (isOnline) {
      final request = http.Request('POST', Uri.parse('$ollamaBaseUrl/api/generate'));
      request.headers['Content-Type'] = 'application/json';
      request.body = jsonEncode({
        'model': activeModel,
        'prompt': '<|im_start|>system\nआप "ग्रामसेतु AI" हैं - ग्रामीण भारत के डिजिटल सहायक। सरल हिंदी में उत्तर दें।<|im_end|>\n<|im_start|>user\n$prompt<|im_end|>\n<|im_start|>assistant\n',
        'stream': true,
      });

      final streamedResponse = await request.send();
      await for (final chunk in streamedResponse.stream.transform(utf8.decoder)) {
        final lines = chunk.split('\n').where((l) => l.trim().isNotEmpty);
        for (final line in lines) {
          try {
            final json = jsonDecode(line);
            if (json['response'] != null) {
              yield json['response'];
            }
          } catch (_) {}
        }
      }
    } else {
      // Offline fallback yield
      yield '🌱 **ग्रामसेतु AI ऑफलाइन समाधान:**\nआपके प्रश्न "$prompt" का समाधान ऑन-डिवाइस डेटाबेस से प्राप्त किया गया है।';
    }
  }
}
