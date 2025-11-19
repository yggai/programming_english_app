import 'package:flutter/foundation.dart';
import '../../data/repositories/auth_repository.dart';
import '../../data/models/auth_models.dart';

class AuthProvider extends ChangeNotifier {
  final AuthRepository _authRepository;
  
  AuthProvider({AuthRepository? authRepository})
      : _authRepository = authRepository ?? AuthRepositoryImpl();

  bool _isLoading = false;
  String? _error;
  UserInfo? _user;

  bool get isLoading => _isLoading;
  String? get error => _error;
  UserInfo? get user => _user;
  bool get isAuthenticated => _user != null;

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
    await _authRepository.logout();
    _user = null;
    _error = null;
    notifyListeners();
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}