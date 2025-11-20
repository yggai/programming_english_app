import 'package:flutter_tts/flutter_tts.dart';

class TextToSpeechService {
  static final TextToSpeechService _instance = TextToSpeechService._internal();
  factory TextToSpeechService() => _instance;
  TextToSpeechService._internal();

  FlutterTts? _flutterTts;

  Future<void> initialize() async {
    _flutterTts = FlutterTts();
    await _flutterTts!.awaitSpeakCompletion(true);
    try {
      await _flutterTts!.setLanguage("en-US");
      final availableUS = await _flutterTts!.isLanguageAvailable("en-US");
      if (availableUS is bool && availableUS == false) {
        await _flutterTts!.setLanguage("en-GB");
      }
    } catch (_) {}
    await _flutterTts!.setSpeechRate(0.5);
    await _flutterTts!.setVolume(1.0);
    await _flutterTts!.setPitch(1.0);
  }

  Future<void> speak(String text) async {
    if (_flutterTts == null) {
      await initialize();
    }
    if (text.isEmpty) {
      return;
    }
    try {
      await _flutterTts!.speak(text);
    } catch (_) {}
  }

  Future<void> stop() async {
    if (_flutterTts != null) {
      await _flutterTts!.stop();
    }
  }

  Future<void> setLanguage(String language) async {
    if (_flutterTts != null) {
      try {
        final available = await _flutterTts!.isLanguageAvailable(language);
        if (available is bool && available) {
          await _flutterTts!.setLanguage(language);
        }
      } catch (_) {}
    }
  }

  Future<void> setSpeechRate(double rate) async {
    if (_flutterTts != null) {
      await _flutterTts!.setSpeechRate(rate);
    }
  }
}