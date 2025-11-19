import 'package:flutter/material.dart';
import '../../../../core/theme/app_text_styles.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Programming English'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              // 处理登出逻辑
            },
          ),
        ],
      ),
      body: const Center(
        child: Text(
          '欢迎使用编程英语学习平台',
          style: AppTextStyles.heading2,
        ),
      ),
    );
  }
}