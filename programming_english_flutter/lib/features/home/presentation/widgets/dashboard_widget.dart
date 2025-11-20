import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';
import '../../../../core/services/text_to_speech_service.dart';

class DashboardWidget extends StatelessWidget {
  const DashboardWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildWelcomeSection(),
          const SizedBox(height: 24),
          _buildStatsSection(),
          const SizedBox(height: 24),
          _buildQuickActions(),
          const SizedBox(height: 24),
          _buildRecentWords(),
        ],
      ),
    );
  }

  Widget _buildWelcomeSection() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [AppColors.primary, AppColors.primaryLight],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          const CircleAvatar(
            radius: 30,
            backgroundColor: Colors.white,
            child: Icon(Icons.person, size: 30, color: AppColors.primary),
          ),
          const SizedBox(width: 16),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '欢迎回来！',
                style: AppTextStyles.heading3.copyWith(color: Colors.white),
              ),
              Text(
                '继续你的编程英语学习之旅',
                style: AppTextStyles.bodyMedium.copyWith(color: Colors.white70),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStatsSection() {
    return Row(
      children: [
        _buildStatCard('已学单词', '1,234', Icons.book, Colors.blue),
        const SizedBox(width: 12),
        _buildStatCard('连续打卡', '7天', Icons.local_fire_department, Colors.orange),
        const SizedBox(width: 12),
        _buildStatCard('掌握程度', '85%', Icons.trending_up, Colors.green),
      ],
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(height: 8),
            Text(value, style: AppTextStyles.heading3),
            Text(title, style: AppTextStyles.bodySmall),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickActions() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('快捷操作', style: AppTextStyles.heading3),
        const SizedBox(height: 12),
        Row(
          children: [
            _buildActionButton('开始学习', Icons.play_arrow, AppColors.primary),
            const SizedBox(width: 12),
            _buildActionButton('复习单词', Icons.refresh, AppColors.secondary),
            const SizedBox(width: 12),
            _buildActionButton('测试', Icons.quiz, Colors.orange),
          ],
        ),
      ],
    );
  }

  Widget _buildActionButton(String text, IconData icon, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
      ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(height: 8),
            Text(text, style: AppTextStyles.bodyMedium),
          ],
        ),
      ),
    );
  }

  Widget _buildRecentWords() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('最近学习', style: AppTextStyles.heading3),
        const SizedBox(height: 12),
        _buildWordCard('function', '函数', 'A block of reusable code'),
        const SizedBox(height: 8),
        _buildWordCard('variable', '变量', 'A storage location with a name'),
        const SizedBox(height: 8),
        _buildWordCard('array', '数组', 'A collection of elements'),
      ],
    );
  }

  Widget _buildWordCard(String word, String chinese, String definition) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.border),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(word, style: AppTextStyles.heading3),
                Text(chinese, style: AppTextStyles.bodyMedium),
                Text(definition, style: AppTextStyles.bodySmall),
              ],
            ),
          ),
          IconButton(
            icon: const Icon(Icons.volume_up, color: AppColors.primary),
            onPressed: () {
              TextToSpeechService().speak(word);
            },
          ),
        ],
      ),
    );
  }
}