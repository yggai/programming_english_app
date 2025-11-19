import 'package:flutter_tts/flutter_tts.dart';

class TextToSpeechService {
  static final TextToSpeechService _instance = TextToSpeechService._internal();
  factory TextToSpeechService() => _instance;
  TextToSpeechService._internal();

  FlutterTts? _flutterTts;

  Future<void> initialize() async {
    _flutterTts = FlutterTts();
    
    // 设置语言为英语
    await _flutterTts!.setLanguage("en-US");
    
    // 设置语速
    await _flutterTts!.setSpeechRate(0.5);
    
    // 设置音量
    await _flutterTts!.setVolume(1.0);
    
    // 设置音调
    await _flutterTts!.setPitch(1.0);
  }

  Future<void> speak(String text) async {
    if (_flutterTts == null) {
      await initialize();
    }
    
    if (text.isNotEmpty) {
      await _flutterTts!.speak(text);
    }
  }

  Future<void> stop() async {
    if (_flutterTts != null) {
      await _flutterTts!.stop();
    }
  }

  Future<void> setLanguage(String language) async {
    if (_flutterTts != null) {
      await _flutterTts!.setLanguage(language);
    }
  }

  Future<void> setSpeechRate(double rate) async {
    if (_flutterTts != null) {
      await _flutterTts!.setSpeechRate(rate);
    }
  }
}