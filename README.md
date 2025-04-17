# 青龙脚本项目管理

## 项目结构
```
qinglong-js/
├── scripts/          # 脚本目录
│   ├── python/      # Python脚本
│   └── js/          # JavaScript脚本
├── config/          # 配置文件
│   └── config.yml   # 基础配置
├── logs/            # 执行日志
├── requirements.txt # Python依赖
└── package.json     # Node.js依赖
```

## 使用说明
1. Python脚本需安装依赖：`pip install -r requirements.txt`
2. 配置文件路径：`config/config.yml`
3. 日志自动存储在logs目录
4. 添加新脚本到对应语言目录