import 'package:flutter/material.dart';
import '../../../../core/services/health_check_service.dart';

class NetworkDebugInfo extends StatelessWidget {
  const NetworkDebugInfo({super.key});

  Future<bool> _testConnection() async {
    return await HealthCheckService.checkServerHealth();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: _testConnection(),
      builder: (context, snapshot) {
        final isConnected = snapshot.data ?? false;
        
        return Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: isConnected ? Colors.green.withValues(alpha: 0.1) : Colors.red.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Row(
            children: [
              Icon(
                isConnected ? Icons.check_circle : Icons.error,
                color: isConnected ? Colors.green : Colors.red,
                size: 20,
              ),
              const SizedBox(width: 8),
              Text(
                isConnected ? '服务器连接正常' : '无法连接服务器',
                style: TextStyle(
                  color: isConnected ? Colors.green : Colors.red,
                  fontSize: 12,
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}