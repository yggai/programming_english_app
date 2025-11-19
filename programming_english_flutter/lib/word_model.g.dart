// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'word_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Word _$WordFromJson(Map<String, dynamic> json) => Word(
      id: (json['id'] as num).toInt(),
      word: json['word'] as String,
      translation: json['translation'] as String,
      example: json['example'] as String,
      difficulty: json['difficulty'] as String? ?? 'beginner',
      definition: json['definition'] as String? ?? '',
      pronunciation: json['pronunciation'] as String?,
      category: json['category'] as String?,
    );

Map<String, dynamic> _$WordToJson(Word instance) => <String, dynamic>{
      'id': instance.id,
      'word': instance.word,
      'translation': instance.translation,
      'example': instance.example,
      'difficulty': instance.difficulty,
      'definition': instance.definition,
      'pronunciation': instance.pronunciation,
      'category': instance.category,
    };

ApiResponse _$ApiResponseFromJson(Map<String, dynamic> json) => ApiResponse(
      success: json['success'] as bool,
      data: (json['data'] as List<dynamic>?)
          ?.map((e) => Word.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$ApiResponseToJson(ApiResponse instance) =>
    <String, dynamic>{
      'success': instance.success,
      'data': instance.data,
    };
