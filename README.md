# 青龙脚本项目管理

## 项目结构
```
qinglong-js/
├── poll_urls.py      # 主执行脚本
├── config/          # 配置文件
└── config.yml      # 基础配置
├── logs/            # 执行日志（JSON格式）
├── requirements.txt # Python依赖
└── README.md        # 项目文档
```

## 使用说明
1. Python脚本需安装依赖：`pip install -r requirements.txt`
2. 配置文件路径：`config.yml`
3. 日志以JSON格式自动存储在logs目录
4. 新增脚本直接添加到项目根目录