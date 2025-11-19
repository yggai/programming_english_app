import 'package:flutter/foundation.dart';
import 'package:dio/dio.dart';
import '../constants/app_constants.dart';

class HealthCheckService {
  static final Dio _dio = Dio();

  static Future<bool> checkServerHealth() async {
    try {
      _dio.options.connectTimeout = const Duration(seconds: 5);
      final response = await _dio.get('${AppConstants.baseUrl}/api/v1/health');
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('服务器健康检查失败: $e');
      return false;
    }
  }

  static Future<Map<String, dynamic>> getServerInfo() async {
    try {
      final response = await _dio.get('${AppConstants.baseUrl}/api/v1/info');
      return response.data as Map<String, dynamic>;
    } catch (e) {
      return {
        'status': 'error',
        'message': e.toString(),
      };
    }
  }
}