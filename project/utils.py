from datetime import timedelta

import telebot
from django.conf import settings
from django.utils.timezone import localtime, now
from django.conf import settings

from .models import Company, CompanyToken

def send_otp_code(number: str, code: int):
    bot = telebot.TeleBot(settings.BOT_TOKEN)

    expired_at = (localtime(now()) + timedelta(minutes=5)).strftime("%H:%M")

    message = (
        "🔔 <b>Telefon raqami uchun tasdiqlash kodi:</b>\n\n"
        f"📞 <b>Telefon:</b> <code>{number}</code>\n"
        f"🔓 <b>Kod:</b> <code>{code}</code>\n"
        f"⏳ <b>Yaroqlilik muddati:</b> <code>{expired_at}</code>\n\n"
        "ℹ️ Iltimos, kodni hech kim bilan ulashmang!"
    )

    bot.send_message("-1002354764356", message, message_thread_id=236, parse_mode="HTML")

    print(f"Kod yuborildi: {number} -> {code}")


def generate_token_for_company(company):
    token, created = CompanyToken.objects.get_or_create(company=company)
    return token.key
