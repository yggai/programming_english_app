import 'package:flutter/material.dart';
import '../widgets/widgets.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GestureDetector(
        onTap: () => FocusScope.of(context).unfocus(),
        child: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                AppColors.background,
                Color(0xFFE8F5E8),
              ],
            ),
          ),
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 32.0),
          child: const Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _AppLogo(),
              SizedBox(height: 48),
              LoginForm(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _AppLogo extends StatelessWidget {
  const _AppLogo();

  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        Icon(
          Icons.school,
          size: 64,
          color: AppColors.primary,
        ),
        SizedBox(height: 16),
        Text(
          'Programming English',
          style: AppTextStyles.heading1,
        ),
        SizedBox(height: 8),
        Text(
          '专业编程英语学习平台',
          style: AppTextStyles.bodyLarge,
        ),
      ],
    );
  }
}