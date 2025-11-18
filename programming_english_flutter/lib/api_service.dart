import 'dart:convert';
import 'package:http/http.dart' as http;
import 'word_model.dart';

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android模拟器访问本地主机

  static Future<List<Word>> getWords() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/words'));
      
      if (response.statusCode == 200) {
        final apiResponse = ApiResponse.fromJson(json.decode(response.body));
        if (apiResponse.success && apiResponse.data != null) {
          return apiResponse.data!;
        } else {
          throw Exception('API返回失败');
        }
      } else {
        throw Exception('请求失败: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('获取单词列表失败: $e');
    }
  }

  static Future<Word> getRandomWord() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/random-word'));
      
      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = json.decode(response.body);
        if (responseData['success'] == true && responseData['data'] != null) {
          return Word.fromJson(responseData['data']);
        } else {
          throw Exception('API返回失败');
        }
      } else {
        throw Exception('请求失败: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('获取随机单词失败: $e');
    }
  }
}