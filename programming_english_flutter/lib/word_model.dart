import 'package:json_annotation/json_annotation.dart';

part 'word_model.g.dart';

@JsonSerializable()
class Word {
  final int id;
  final String word;
  final String translation;
  final String example;

  Word({
    required this.id,
    required this.word,
    required this.translation,
    required this.example,
  });

  factory Word.fromJson(Map<String, dynamic> json) => _$WordFromJson(json);
  Map<String, dynamic> toJson() => _$WordToJson(this);
}

@JsonSerializable()
class ApiResponse {
  final bool success;
  final List<Word>? data;

  ApiResponse({required this.success, this.data});

  factory ApiResponse.fromJson(Map<String, dynamic> json) => _$ApiResponseFromJson(json);
  Map<String, dynamic> toJson() => _$ApiResponseToJson(this);
}