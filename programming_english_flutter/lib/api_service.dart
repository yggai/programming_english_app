import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'word_model.dart';

class ApiService {
  static String get baseUrl {
    if (kIsWeb) return 'http://localhost:8000';
    if (Platform.isAndroid) return 'http://10.0.2.2:8000';
    return 'http://localhost:8000';
  }
  static const String tokenKey = 'auth_token';

  // 保存token
  static Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(tokenKey, token);
  }

  // 获取token
  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(tokenKey);
  }

  // 删除token
  static Future<void> removeToken() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(tokenKey);
  }

  // 获取请求头
  static Future<Map<String, String>> getHeaders() async {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    
    final token = await getToken();
    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }
    
    return headers;
  }

  // 用户登录
  static Future<Map<String, dynamic>> login(String username, String password) async {
    final url = Uri.parse('$baseUrl/api/v1/auth/login');
    final headers = await getHeaders();

    try {
      final response = await http.post(
        url,
        headers: headers,
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        final errorData = jsonDecode(response.body);
        throw Exception(errorData['message'] ?? '登录失败');
      }
    } catch (e) {
      throw Exception('网络连接失败: $e');
    }
  }

  // 用户登出
  static Future<void> logout() async {
    try {
      final url = Uri.parse('$baseUrl/api/v1/auth/logout');
      final headers = await getHeaders();
      
      await http.post(url, headers: headers);
    } catch (e) {
      // 即使服务器登出失败，也要清除本地token
    } finally {
      await removeToken();
    }
  }

  // 检查登录状态
  static Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }

  // 获取单词列表
  static Future<List<Word>> getWords({int page = 1, int size = 20}) async {
    final url = Uri.parse('$baseUrl/api/v1/words?page=$page&size=$size');
    final headers = await getHeaders();

    try {
      final response = await http.get(url, headers: headers);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['success'] && data['data'] != null) {
          final items = data['data']['items'] as List;
          return items.map((item) => Word.fromJson(item)).toList();
        }
      }
      
      return [];
    } catch (e) {
      throw Exception('获取单词列表失败: $e');
    }
  }

  // 搜索单词
  static Future<List<Word>> searchWords(String query) async {
    final url = Uri.parse('$baseUrl/api/v1/words/search?q=$query');
    final headers = await getHeaders();

    try {
      final response = await http.get(url, headers: headers);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['success'] && data['data'] != null) {
          final items = data['data']['items'] as List;
          return items.map((item) => Word.fromJson(item)).toList();
        }
      }
      
      return [];
    } catch (e) {
      throw Exception('搜索单词失败: $e');
    }
  }

  // 添加单词
  static Future<bool> addWord(Word word) async {
    final url = Uri.parse('$baseUrl/api/v1/words');
    final headers = await getHeaders();

    try {
      final response = await http.post(
        url,
        headers: headers,
        body: jsonEncode(word.toJson()),
      );

      return response.statusCode == 201;
    } catch (e) {
      throw Exception('添加单词失败: $e');
    }
  }

  // 更新单词
  static Future<bool> updateWord(Word word) async {
    final url = Uri.parse('$baseUrl/api/v1/words/${word.id}');
    final headers = await getHeaders();

    try {
      final response = await http.put(
        url,
        headers: headers,
        body: jsonEncode(word.toJson()),
      );

      return response.statusCode == 200;
    } catch (e) {
      throw Exception('更新单词失败: $e');
    }
  }

  // 删除单词
  static Future<bool> deleteWord(int id) async {
    final url = Uri.parse('$baseUrl/api/v1/words/$id');
    final headers = await getHeaders();

    try {
      final response = await http.delete(url, headers: headers);
      return response.statusCode == 200;
    } catch (e) {
      throw Exception('删除单词失败: $e');
    }
  }
}