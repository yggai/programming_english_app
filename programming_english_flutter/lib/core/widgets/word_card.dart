import 'package:flutter/material.dart';
import 'package:programming_english_flutter/word_model.dart';
import 'pronunciation_button.dart';

class WordCard extends StatelessWidget {
  final Word word;
  final VoidCallback? onTap;

  const WordCard({
    super.key,
    required this.word,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 单词标题和发音按钮
              Row(
                children: [
                  Expanded(
                    child: Text(
                      word.word,
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: Theme.of(context).primaryColor,
                      ),
                    ),
                  ),
                  PronunciationButton(
                    text: word.word,
                    onPressed: () => word.speakWord(),
                  ),
                ],
              ),
              
              // 音标（如果有）
              if (word.pronunciation != null) ...[
                const SizedBox(height: 8),
                Text(
                  word.pronunciation!,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontStyle: FontStyle.italic,
                    color: Colors.grey[600],
                  ),
                ),
              ],
              
              const SizedBox(height: 12),
              
              // 翻译
              Text(
                '翻译：${word.translation}',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  fontWeight: FontWeight.w500,
                ),
              ),
              
              const SizedBox(height: 8),
              
              // 定义
              Text(
                '定义：${word.definition}',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              
              const SizedBox(height: 12),
              
              // 例句
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey[50],
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.grey[200]!),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          '例句：',
                          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: Colors.grey[600],
                          ),
                        ),
                        const Spacer(),
                        PronunciationButton(
                          text: word.example,
                          tooltip: '朗读例句',
                          icon: Icons.play_arrow,
                          onPressed: () => word.speakExample(),
                        ),
                      ],
                    ),
                    const SizedBox(height: 4),
                    Text(
                      word.example,
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ],
                ),
              ),
              
              const SizedBox(height: 8),
              
              // 标签
              Row(
                children: [
                  Chip(
                    label: Text(
                      word.difficulty,
                      style: const TextStyle(fontSize: 12),
                    ),
                    backgroundColor: _getDifficultyColor(word.difficulty),
                  ),
                  const SizedBox(width: 8),
                  Chip(
                    label: Text(
                      word.category ?? 'basic',
                      style: const TextStyle(fontSize: 12),
                    ),
                    backgroundColor: Colors.blue[100],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getDifficultyColor(String difficulty) {
    switch (difficulty.toLowerCase()) {
      case 'beginner':
        return Colors.green[100]!;
      case 'intermediate':
        return Colors.orange[100]!;
      case 'advanced':
        return Colors.red[100]!;
      default:
        return Colors.grey[100]!;
    }
  }
}