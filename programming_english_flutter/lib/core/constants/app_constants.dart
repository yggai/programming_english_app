class AppConstants {
  // App信息
  static const String appName = 'Programming English';
  static const String appVersion = '1.0.0';
  
  // API配置 - 使用内网IP
  static const String baseUrl = 'http://192.168.1.5:8000'; // 内网IP
  static const Duration apiTimeout = Duration(seconds: 30);
  
  // 存储键名
  static const String authTokenKey = 'auth_token';
  static const String userPrefsKey = 'user_preferences';
  
  // 分页配置
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;
  
  // 验证规则
  static const int minUsernameLength = 3;
  static const int maxUsernameLength = 50;
  static const int minPasswordLength = 6;
}