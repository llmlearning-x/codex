import argparse
import json
from datetime import datetime
import smtplib
from email.message import EmailMessage
from pathlib import Path

SCENES = [
    "AI质检专家",
    "AI+云监管",
    "进度",
    "造价",
    "智能问答",
    "智能问数",
    "工程文档智能生成",
    "工程文档智能审核",
]

CONFIG_PATH = Path(__file__).with_name("config.json")


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_args():
    parser = argparse.ArgumentParser(description="Generate and send AI scene daily report")
    parser.add_argument("--date", help="Date in YYYY-MM-DD format", required=True)
    for scene in SCENES:
        parser.add_argument(f"--{scene}", dest=scene, help=f"Progress for {scene}")
    return parser.parse_args()


def format_report(date: datetime, progress_map):
    weekday_map = "一二三四五六日"
    weekday = weekday_map[date.weekday()]
    lines = [f"# {date.year} 年 {date.month} 月 {date.day} 日(星期 {weekday})AI场景日报"]
    for i, scene in enumerate(SCENES, start=1):
        progress = progress_map.get(scene) or "无"
        lines.append(f"场景 {i}：{scene}")
        lines.append(f"场景进展：{progress}\n")
    return "\n".join(lines)


def send_mail(subject: str, body: str, config):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = config.get("from")
    msg["To"] = ",".join(config.get("to", []))
    if config.get("cc"):
        msg["Cc"] = ",".join(config.get("cc", []))
    try:
        with smtplib.SMTP(config.get("smtp_server", "localhost"), config.get("smtp_port", 25)) as smtp:
            if config.get("username") and config.get("password"):
                smtp.login(config["username"], config["password"])
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def main():
    args = get_args()
    date = datetime.strptime(args.date, "%Y-%m-%d")
    progress_map = {scene: getattr(args, scene) for scene in SCENES}
    report = format_report(date, progress_map)
    config = load_config()
    weekday_map = "一二三四五六日"
    subject = f"{date.year} 年 {date.month} 月 {date.day} 日(星期 {weekday_map[date.weekday()]})AI 应用场景日报"
    status = send_mail(subject, report, config)
    filled_count = sum(1 for p in progress_map.values() if p)
    print("邮件发送成功" if status else "邮件发送失败")
    print(f"已填写工作日报的场景数: {filled_count}")


if __name__ == "__main__":
    main()
