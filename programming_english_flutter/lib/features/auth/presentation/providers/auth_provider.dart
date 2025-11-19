import 'package:flutter/foundation.dart';
import '../../data/repositories/auth_repository.dart';
import '../../data/models/auth_models.dart';

class AuthProvider extends ChangeNotifier {
  final AuthRepository _authRepository;
  
  AuthProvider({AuthRepository? authRepository})
      : _authRepository = authRepository ?? AuthRepositoryImpl() {
    _checkLoginStatus();
  }

  bool _isLoading = false;
  bool _isInitialized = false;
  String? _error;
  UserInfo? _user;

  bool get isLoading => _isLoading;
  bool get isInitialized => _isInitialized;
  String? get error => _error;
  UserInfo? get user => _user;
  bool get isAuthenticated => _user != null;

  Future<void> _checkLoginStatus() async {
    try {
      final token = await _authRepository.getToken();
      if (token != null && token.isNotEmpty) {
        // 这里可以添加验证token有效性的逻辑
        // 暂时使用模拟用户数据
        _user = UserInfo(id: 1, username: '用户', email: 'user@example.com');
      }
    } catch (e) {
      debugPrint('检查登录状态失败: $e');
    } finally {
      _isInitialized = true;
      notifyListeners();
    }
  }

  Future<bool> login(String username, String password) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _authRepository.login(username, password);
      
      if (response.success && response.data != null) {
        _user = response.data!.user;
        await _authRepository.saveToken(response.data!.accessToken);
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _error = response.message;
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();
    
    try {
      await _authRepository.logout();
      _user = null;
      _error = null;
    } catch (e) {
      debugPrint('退出登录时发生错误: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}