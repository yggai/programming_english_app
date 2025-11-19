class LoginRequest {
  final String username;
  final String password;

  LoginRequest({
    required this.username,
    required this.password,
  });

  Map<String, dynamic> toJson() => {
        'username': username,
        'password': password,
      };
}

class LoginResponse {
  final bool success;
  final String message;
  final LoginData? data;

  LoginResponse({
    required this.success,
    required this.message,
    this.data,
  });

  factory LoginResponse.fromJson(Map<String, dynamic> json) => LoginResponse(
        success: json['success'] ?? false,
        message: json['message'] ?? '',
        data: json['data'] != null ? LoginData.fromJson(json['data']) : null,
      );
}

class LoginData {
  final String accessToken;
  final String refreshToken;
  final UserInfo user;

  LoginData({
    required this.accessToken,
    required this.refreshToken,
    required this.user,
  });

  factory LoginData.fromJson(Map<String, dynamic> json) => LoginData(
        accessToken: json['access_token'] ?? '',
        refreshToken: json['refresh_token'] ?? '',
        user: UserInfo.fromJson(json['user'] ?? {}),
      );
}

class UserInfo {
  final int id;
  final String username;
  final String email;

  UserInfo({
    required this.id,
    required this.username,
    required this.email,
  });

  factory UserInfo.fromJson(Map<String, dynamic> json) => UserInfo(
        id: json['id'] ?? 0,
        username: json['username'] ?? '',
        email: json['email'] ?? '',
      );
}