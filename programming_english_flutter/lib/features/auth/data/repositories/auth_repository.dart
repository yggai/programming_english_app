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

  AuthRepositoryImpl({Dio? dio}) : _dio = dio ?? Dio();

  @override
  Future<LoginResponse> login(String username, String password) async {
    try {
      final response = await _dio.post(
        '${AppConstants.baseUrl}/api/v1/auth/login',
        data: LoginRequest(username: username, password: password).toJson(),
      );
      
      return LoginResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw Exception('登录失败: ${e.response?.data['message'] ?? '网络错误'}');
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