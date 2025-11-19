import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';

class LearnWidget extends StatelessWidget {
  const LearnWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildLearningProgress(),
          const SizedBox(height: 24),
          _buildLearningModes(),
          const SizedBox(height: 24),
          _buildRecommendedContent(),
        ],
      ),
    );
  }

  Widget _buildLearningProgress() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('学习进度', style: AppTextStyles.heading3),
          const SizedBox(height: 16),
          _buildProgressItem('基础词汇', 0.75, '75%'),
          const SizedBox(height: 12),
          _buildProgressItem('进阶词汇', 0.45, '45%'),
          const SizedBox(height: 12),
          _buildProgressItem('专业术语', 0.30, '30%'),
        ],
      ),
    );
  }

  Widget _buildProgressItem(String title, double progress, String percentage) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(title, style: AppTextStyles.bodyMedium),
            Text(percentage, style: AppTextStyles.bodySmall),
          ],
        ),
        const SizedBox(height: 4),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: progress,
            backgroundColor: AppColors.divider,
            valueColor: const AlwaysStoppedAnimation<Color>(AppColors.primary),
            minHeight: 8,
          ),
        ),
      ],
    );
  }

  Widget _buildLearningModes() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('学习模式', style: AppTextStyles.heading3),
        const SizedBox(height: 12),
        _buildModeCard(
          '闪卡学习',
          '通过卡片记忆单词',
          Icons.credit_card,
          AppColors.primary,
          () {
            // 导航到闪卡学习
          },
        ),
        const SizedBox(height: 12),
        _buildModeCard(
          '拼写练习',
          '练习单词拼写',
          Icons.spellcheck,
          Colors.purple,
          () {
            // 导航到拼写练习
          },
        ),
        const SizedBox(height: 12),
        _buildModeCard(
          '听力训练',
          '提升编程英语听力',
          Icons.hearing,
          Colors.orange,
          () {
            // 导航到听力训练
          },
        ),
      ],
    );
  }

  Widget _buildModeCard(
    String title,
    String description,
    IconData icon,
    Color color,
    VoidCallback onTap,
  ) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.border),
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(icon, color: color, size: 24),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: AppTextStyles.bodyLarge),
                  Text(description, style: AppTextStyles.bodySmall),
                ],
              ),
            ),
            const Icon(Icons.chevron_right, color: AppColors.textHint),
          ],
        ),
      ),
    );
  }

  Widget _buildRecommendedContent() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('推荐内容', style: AppTextStyles.heading3),
        const SizedBox(height: 12),
        _buildContentCard(
          'JavaScript基础词汇',
          '10个单元 · 200个单词',
          'assets/images/js.png',
          AppColors.primary,
        ),
        const SizedBox(height: 12),
        _buildContentCard(
          'Python编程术语',
          '8个单元 · 160个单词',
          'assets/images/python.png',
          Colors.blue,
        ),
      ],
    );
  }

  Widget _buildContentCard(
    String title,
    String subtitle,
    String imagePath,
    Color color,
  ) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.border),
      ),
      child: Row(
        children: [
          Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(Icons.code, color: color, size: 30),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: AppTextStyles.bodyLarge),
                Text(subtitle, style: AppTextStyles.bodySmall),
              ],
            ),
          ),
          ElevatedButton(
            onPressed: () {
              // 开始学习
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: color,
              minimumSize: const Size(80, 36),
              padding: const EdgeInsets.symmetric(horizontal: 16),
            ),
            child: const Text('开始'),
          ),
        ],
      ),
    );
  }
}