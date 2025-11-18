import 'package:flutter/material.dart';
import 'api_service.dart';
import 'login_page.dart';

class AuthGuard {
  static Future<bool> checkAuthStatus() async {
    try {
      return await ApiService.isLoggedIn();
    } catch (e) {
      return false;
    }
  }

  static Widget requireAuth({required Widget child}) {
    return FutureBuilder<bool>(
      future: checkAuthStatus(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 20),
                  Text(
                    '检查登录状态...',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.grey,
                    ),
                  ),
                ],
              ),
            ),
          );
        }

        if (snapshot.hasData && snapshot.data == true) {
          return child;
        } else {
          return const LoginPage();
        }
      },
    );
  }
}