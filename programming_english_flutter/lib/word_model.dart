import 'package:json_annotation/json_annotation.dart';
import 'package:programming_english_flutter/core/services/text_to_speech_service.dart';

part 'word_model.g.dart';

@JsonSerializable()
class Word {
  final int id;
  final String word;
  final String translation;
  final String example;
  final String difficulty;
  final String definition;
  final String? pronunciation;
  final String? category;

  Word({
    required this.id,
    required this.word,
    required this.translation,
    required this.example,
    this.difficulty = 'beginner',
    this.definition = '',
    this.pronunciation,
    this.category,
  });

  factory Word.fromJson(Map<String, dynamic> json) => _$WordFromJson(json);
  Map<String, dynamic> toJson() => _$WordToJson(this);

  // 发音方法
  Future<void> speakWord() async {
    await TextToSpeechService().speak(word);
  }

  // 发音例句方法
  Future<void> speakExample() async {
    await TextToSpeechService().speak(example);
  }
}

@JsonSerializable()
class ApiResponse {
  final bool success;
  final List<Word>? data;

  ApiResponse({required this.success, this.data});

  factory ApiResponse.fromJson(Map<String, dynamic> json) => _$ApiResponseFromJson(json);
  Map<String, dynamic> toJson() => _$ApiResponseToJson(this);
}