import 'package:flutter/material.dart';

class PronunciationButton extends StatefulWidget {
  final String text;
  final String? tooltip;
  final IconData icon;
  final VoidCallback? onPressed;

  const PronunciationButton({
    super.key,
    required this.text,
    this.tooltip,
    this.icon = Icons.volume_up,
    this.onPressed,
  });

  @override
  State<PronunciationButton> createState() => _PronunciationButtonState();
}

class _PronunciationButtonState extends State<PronunciationButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _scaleAnimation;
  bool _isPlaying = false;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 200),
      vsync: this,
    );
    _scaleAnimation = Tween<double>(
      begin: 1.0,
      end: 0.9,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  void _handlePress() {
    setState(() {
      _isPlaying = true;
    });

    _animationController.forward().then((_) {
      _animationController.reverse();
    });

    // 模拟播放完成
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        setState(() {
          _isPlaying = false;
        });
      }
    });

    widget.onPressed?.call();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _scaleAnimation,
      builder: (context, child) {
        return Transform.scale(
          scale: _scaleAnimation.value,
          child: Tooltip(
            message: widget.tooltip ?? '发音',
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                borderRadius: BorderRadius.circular(20),
                onTap: _isPlaying ? null : _handlePress,
                child: Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: _isPlaying 
                        ? Theme.of(context).primaryColor.withOpacity(0.3)
                        : Colors.transparent,
                    border: Border.all(
                      color: Theme.of(context).primaryColor,
                      width: 1,
                    ),
                  ),
                  child: Icon(
                    widget.icon,
                    color: _isPlaying 
                        ? Theme.of(context).primaryColor
                        : Theme.of(context).primaryColor.withOpacity(0.7),
                    size: 20,
                  ),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}