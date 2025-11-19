import 'package:flutter/foundation.dart';
import 'package:dio/dio.dart';
import '../models/auth_models.dart';
import '../../../../core/constants/app_constants.dart';

abstract class AuthRepository {
  Future<LoginResponse> login(String username, String password);
  Future<void> logout();
  Future<String?> getToken();
  Future<void> saveToken(String token);
  Future<void> clearToken();
}

class AuthRepositoryImpl implements AuthRepository {
  final Dio _dio;

  AuthRepositoryImpl({Dio? dio}) : _dio = dio ?? _createDio();

  
  static Dio _createDio() {
    final dio = Dio();
    
    // 配置基础选项
    dio.options = BaseOptions(
      baseUrl: AppConstants.baseUrl,
      connectTimeout: AppConstants.apiTimeout,
      receiveTimeout: AppConstants.apiTimeout,
      sendTimeout: AppConstants.apiTimeout,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    );
    
    // 添加拦截器
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          debugPrint('请求: ${options.method} ${options.path}');
          handler.next(options);
        },
        onResponse: (response, handler) {
          debugPrint('响应: ${response.statusCode}');
          handler.next(response);
        },
        onError: (DioException error, handler) {
          debugPrint('错误: ${error.message}');
          handler.next(error);
        },
      ),
    );
    
    return dio;
  }

  @override
  Future<LoginResponse> login(String username, String password) async {
    try {
      final response = await _dio.post(
        '/api/v1/auth/login',
        data: LoginRequest(username: username, password: password).toJson(),
      );
      final data = response.data;
      if (data is Map<String, dynamic>) {
        if (data.containsKey('success')) {
          return LoginResponse.fromJson(data);
        }
        if (data.containsKey('access_token')) {
          final loginData = LoginData(
            accessToken: data['access_token'] ?? '',
            refreshToken: data['refresh_token'] ?? '',
            user: UserInfo(id: 0, username: username, email: ''),
          );
          return LoginResponse(success: true, message: '登录成功', data: loginData);
        }
      }
      return LoginResponse(success: false, message: '服务器返回格式不正确', data: null);
    } on DioException catch (e) {
      String errorMessage = '网络连接失败';
      
      if (e.type == DioExceptionType.connectionTimeout) {
        errorMessage = '连接超时，请检查网络';
      } else if (e.type == DioExceptionType.receiveTimeout) {
        errorMessage = '接收超时，请检查网络';
      } else if (e.type == DioExceptionType.badResponse) {
        errorMessage = e.response?.data?['message'] ?? '服务器错误';
      } else if (e.type == DioExceptionType.connectionError) {
        errorMessage = '无法连接到服务器，请检查网络设置';
      } else {
        errorMessage = '网络错误: ${e.message}';
      }
      
      throw Exception(errorMessage);
    }
  }

  @override
  Future<void> logout() async {
    await clearToken();
  }

  @override
  Future<String?> getToken() async {
    // 实际项目中这里会从本地存储获取token
    return null;
  }

  @override
  Future<void> saveToken(String token) async {
    // 实际项目中这里会保存token到本地存储
  }

  @override
  Future<void> clearToken() async {
    // 实际项目中这里会清除本地存储的token
  }
}