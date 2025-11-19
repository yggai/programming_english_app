import 'package:flutter/material.dart';
import 'package:programming_english_flutter/core/services/text_to_speech_service.dart';
import 'package:programming_english_flutter/core/widgets/word_card.dart';
import 'package:programming_english_flutter/word_model.dart';

class WordListPage extends StatefulWidget {
  const WordListPage({super.key});

  @override
  State<WordListPage> createState() => _WordListPageState();
}

class _WordListPageState extends State<WordListPage> {
  final TextEditingController _searchController = TextEditingController();
  List<Word> _words = [];
  List<Word> _filteredWords = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _initializeTTS();
    _loadWords();
    _searchController.addListener(_filterWords);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _initializeTTS() async {
    await TextToSpeechService().initialize();
  }

  Future<void> _loadWords() async {
    // 模拟加载单词数据
    await Future.delayed(const Duration(seconds: 1));
    
    final sampleWords = [
      Word(
        id: 1,
        word: 'function',
        translation: '函数',
        definition: '一个可重用的代码块，执行特定任务',
        example: 'The calculateSum function returns the total of two numbers.',
        difficulty: 'beginner',
        category: 'function',
        pronunciation: '/ˈfʌŋkʃən/',
      ),
      Word(
        id: 2,
        word: 'variable',
        translation: '变量',
        definition: '用于存储数据的命名容器',
        example: 'Declare a variable to store the user name.',
        difficulty: 'beginner',
        category: 'basic',
        pronunciation: '/ˈvɛriəbəl/',
      ),
      Word(
        id: 3,
        word: 'algorithm',
        translation: '算法',
        definition: '解决问题或完成任务的一系列步骤',
        example: 'The sorting algorithm arranges data in ascending order.',
        difficulty: 'intermediate',
        category: 'data_structure',
        pronunciation: '/ˈælɡəˌrɪðəm/',
      ),
      Word(
        id: 4,
        word: 'polymorphism',
        translation: '多态',
        definition: '对象可以采取多种形式的能力',
        example: 'Polymorphism allows methods to behave differently based on the object.',
        difficulty: 'advanced',
        category: 'object_oriented',
        pronunciation: '/ˌpɑlɪˈmɔrfɪzəm/',
      ),
      Word(
        id: 5,
        word: 'exception',
        translation: '异常',
        definition: '程序执行期间发生的错误或意外事件',
        example: 'Handle the exception to prevent application crashes.',
        difficulty: 'intermediate',
        category: 'error_handling',
        pronunciation: '/ɪkˈsɛpʃən/',
      ),
    ];

    setState(() {
      _words = sampleWords;
      _filteredWords = sampleWords;
      _isLoading = false;
    });
  }

  void _filterWords() {
    final query = _searchController.text.toLowerCase();
    setState(() {
      _filteredWords = _words.where((word) {
        return word.word.toLowerCase().contains(query) ||
               word.translation.toLowerCase().contains(query) ||
               word.definition.toLowerCase().contains(query);
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('单词列表'),
        actions: [
          IconButton(
            icon: const Icon(Icons.volume_up),
            onPressed: () {
              _showLanguageDialog();
            },
            tooltip: '语音设置',
          ),
        ],
      ),
      body: Column(
        children: [
          // 搜索框
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: '搜索单词...',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                filled: true,
                fillColor: Colors.grey[50],
              ),
            ),
          ),
          
          // 单词列表
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _filteredWords.isEmpty
                    ? const Center(
                        child: Text(
                          '没有找到匹配的单词',
                          style: TextStyle(fontSize: 16),
                        ),
                      )
                    : ListView.builder(
                        itemCount: _filteredWords.length,
                        itemBuilder: (context, index) {
                          final word = _filteredWords[index];
                          return WordCard(
                            word: word,
                            onTap: () {
                              _showWordDetail(word);
                            },
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }

  void _showWordDetail(Word word) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(word.word),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              if (word.pronunciation != null)
                Text(
                  '音标: ${word.pronunciation}',
                  style: const TextStyle(fontStyle: FontStyle.italic),
                ),
              const SizedBox(height: 8),
              Text('翻译: ${word.translation}'),
              const SizedBox(height: 8),
              Text('定义: ${word.definition}'),
              const SizedBox(height: 8),
              Text('例句: ${word.example}'),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ElevatedButton.icon(
                    onPressed: () => word.speakWord(),
                    icon: const Icon(Icons.volume_up),
                    label: const Text('朗读单词'),
                  ),
                  ElevatedButton.icon(
                    onPressed: () => word.speakExample(),
                    icon: const Icon(Icons.play_arrow),
                    label: const Text('朗读例句'),
                  ),
                ],
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('关闭'),
          ),
        ],
      ),
    );
  }

  void _showLanguageDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('语音设置'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('选择发音语言:'),
            const SizedBox(height: 16),
            ListTile(
              title: const Text('美式英语'),
              onTap: () {
                TextToSpeechService().setLanguage("en-US");
                Navigator.of(context).pop();
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('已切换到美式英语')),
                );
              },
            ),
            ListTile(
              title: const Text('英式英语'),
              onTap: () {
                TextToSpeechService().setLanguage("en-GB");
                Navigator.of(context).pop();
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('已切换到英式英语')),
                );
              },
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('取消'),
          ),
        ],
      ),
    );
  }
}