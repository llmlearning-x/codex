# codex

这是一个简单的示例仓库，包含用于生成并发送 AI 场景日报的脚本 `daily_report.py`。

## 使用方法
1. 在仓库根目录下创建 `config.json`，配置发件人、收件人以及 SMTP 服务信息。示例配置如下：

```json
{
  "from": "sender@example.com",
  "to": ["receiver@example.com"],
  "cc": ["cc@example.com"],
  "smtp_server": "smtp.example.com",
  "smtp_port": 25,
  "username": "user",
  "password": "pass"
}
```

2. 运行脚本生成并发送日报：

```bash
python daily_report.py --date 2025-07-25 \
  --AI质检专家 "完成模型调试" \
  --AI+云监管 "部署上线" \
  --进度 "按计划推进" \
  --造价 "无" \
  --智能问答 "" \
  --智能问数 "数据整理" \
  --工程文档智能生成 "" \
  --工程文档智能审核 "初步测试"
```

脚本会根据输入自动生成日报并发送到配置文件中指定的邮箱地址，随后在控制台输出邮件发送状态以及填写了进展的场景数量。
