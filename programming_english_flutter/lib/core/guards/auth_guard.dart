import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../features/auth/presentation/providers/auth_provider.dart';
import '../../features/auth/presentation/pages/login_page.dart';
import '../routes/app_routes.dart';

class AuthGuard {
  static Widget buildWrapper({
    required Widget child,
    required BuildContext context,
  }) {
    return Consumer<AuthProvider>(
      builder: (context, authProvider, _) {
        // 如果正在初始化，显示加载页面
        if (!authProvider.isInitialized) {
          return const Scaffold(
            body: Center(
              child: CircularProgressIndicator(),
            ),
          );
        }

        // 如果未登录，显示登录页面
        if (!authProvider.isAuthenticated) {
          return const LoginPage();
        }

        // 如果已登录，显示传入的页面
        return child;
      },
    );
  }

  static Future<void> checkAndRedirect(BuildContext context) async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    
    // 等待初始化完成
    while (!authProvider.isInitialized) {
      await Future.delayed(const Duration(milliseconds: 100));
    }

    // 如果未登录，重定向到登录页面
    if (!authProvider.isAuthenticated && context.mounted) {
      Navigator.of(context).pushNamedAndRemoveUntil(
        AppRoutes.login,
        (route) => false,
      );
    }
  }
}
