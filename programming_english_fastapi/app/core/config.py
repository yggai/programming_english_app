"""YAML配置文件加载和管理"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path

class YAMLConfig:
    """YAML配置文件管理器"""
    
    def __init__(self, config_path: str = None):
        """初始化配置管理器"""
        if config_path is None:
            # 默认配置文件路径
            base_dir = Path(__file__).parent.parent.parent
            config_path = base_dir / "config.yaml"
        
        self.config_path = Path(config_path)
        self._config_data = None
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config_data = yaml.safe_load(file)
        except FileNotFoundError:
            # 如果配置文件不存在，创建默认配置
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认配置文件"""
        default_config = {
            'app': {
                'name': 'Programming English API',
                'version': '2.0.0',
                'description': 'A FastAPI application for learning programming English',
                'debug': True
            },
            'server': {
                'host': '0.0.0.0',
                'port': 8000,
                'reload': True,
                'log_level': 'info'
            },
            'database': {
                'url': 'sqlite:///./programming_english.db',
                'echo': False,
                'pool_size': 5,
                'max_overflow': 10
            },
            'security': {
                'secret_key': 'your-secret-key-change-this-in-production',
                'algorithm': 'HS256',
                'access_token_expire_minutes': 30
            },
            'cors': {
                'allow_origins': ['*'],
                'allow_credentials': True,
                'allow_methods': ['*'],
                'allow_headers': ['*']
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'testing': {
                'database_url': 'sqlite:///./test.db',
                'echo': False
            }
        }
        
        self._config_data = default_config
        
        # 创建配置文件
        with open(self.config_path, 'w', encoding='utf-8') as file:
            yaml.dump(default_config, file, default_flow_style=False, allow_unicode=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持点语法"""
        keys = key.split('.')
        value = self._config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """获取配置节"""
        return self.get(section, {})
    
    @property
    def app(self) -> Dict[str, Any]:
        """应用配置"""
        return self.get_section('app')
    
    @property
    def server(self) -> Dict[str, Any]:
        """服务器配置"""
        return self.get_section('server')
    
    @property
    def database(self) -> Dict[str, Any]:
        """数据库配置"""
        return self.get_section('database')
    
    @property
    def security(self) -> Dict[str, Any]:
        """安全配置"""
        return self.get_section('security')
    
    @property
    def cors(self) -> Dict[str, Any]:
        """CORS配置"""
        return self.get_section('cors')


# 创建全局配置实例
config = YAMLConfig()

# 快捷访问配置项
APP_NAME = config.app.get('name', 'Programming English API')
APP_VERSION = config.app.get('version', '1.0.0')
APP_DESCRIPTION = config.app.get('description', 'Programming English Learning API')
DEBUG = config.app.get('debug', True)

SERVER_HOST = config.server.get('host', '0.0.0.0')
SERVER_PORT = config.server.get('port', 8000)
SERVER_RELOAD = config.server.get('reload', True)
SERVER_LOG_LEVEL = config.server.get('log_level', 'info')

DATABASE_URL = config.database.get('url', 'sqlite:///./programming_english.db')
DATABASE_ECHO = config.database.get('echo', False)
DATABASE_POOL_SIZE = config.database.get('pool_size', 5)
DATABASE_MAX_OVERFLOW = config.database.get('max_overflow', 10)

SECRET_KEY = config.security.get('secret_key', 'your-secret-key-change-this-in-production')
ALGORITHM = config.security.get('algorithm', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = config.security.get('access_token_expire_minutes', 30)

CORS_ALLOW_ORIGINS = config.cors.get('allow_origins', ['*'])
CORS_ALLOW_CREDENTIALS = config.cors.get('allow_credentials', True)
CORS_ALLOW_METHODS = config.cors.get('allow_methods', ['*'])
CORS_ALLOW_HEADERS = config.cors.get('allow_headers', ['*'])