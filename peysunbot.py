from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 توکن ربات
TOKEN = "8058269849:AAETdPzyoPx2G9IAJ7fLAak2wMJkION_eiI"
ADMIN_CHAT_ID = 315028406  # آیدی عددی مدیر

# حافظه ساده برای وضعیت کاربران
user_states = {}
known_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in known_users:
        return
    known_users.add(user_id)

    keyboard = [
        ["📩 شروع همکاری"],
        ["📞 تماس با ما", "📄 پلن‌ها و قیمت‌ها"],
        ["ℹ️ درباره ما", "🖼 نمونه کارها"],
        ["❓ سوالات متداول", "🔗 شبکه‌های اجتماعی"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    welcome_text = (
        "سلام و خوش آمدید به پیسان وب! 🌞\n\n"
        "🔷 پیسان وب یک پلتفرم حرفه‌ای سایت‌ساز است که به شما اجازه می‌دهد بدون هیچ دانش برنامه‌نویسی، یک سایت زیبا و کامل بسازید – مناسب برای فروشگاه‌ها، شرکت‌ها، رستوران‌ها، موزیک، املاک و...\n\n"
        "💰 همکاری با ما:\nما به نمایندگان فروش و بازاریاب‌ها **۴۰٪ پورسانت دائمی** می‌دهیم!\n"
        "یعنی هر بار مشتری شما پلن تمدید کند، شما هم درآمد خواهید داشت.\n\n"
        "📦 امکانات پیسان وب:\n"
        "✅ سایت‌ساز Drag & Drop حرفه‌ای\n"
        "✅ بیش از ۱۰۰ قالب آماده\n"
        "✅ قابلیت فروشگاهی با درگاه پرداخت\n"
        "✅ سئو پیشرفته و اتصال به گوگل\n"
        "✅ دامنه اختصاصی + ایمیل شرکتی\n"
        "✅ پشتیبانی ۲۴ ساعته و آموزش کامل\n\n"
        "برای شروع کافی‌ست یکی از گزینه‌ها را از منوی زیر انتخاب کنید 👇"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "📩 شروع همکاری":
        user_states[user_id] = "waiting_for_name"
        await update.message.reply_text("لطفا نام کامل خود را وارد کنید:")

    elif user_states.get(user_id) == "waiting_for_name":
        context.user_data['name'] = text
        user_states[user_id] = "waiting_for_phone"
        await update.message.reply_text("حالا شماره تماس خود را وارد کنید:")

    elif user_states.get(user_id) == "waiting_for_phone":
        name = context.user_data.get('name', 'ناشناخته')
        phone = text
        user_states.pop(user_id, None)
        context.user_data.clear()

        await update.message.reply_text("✅ اطلاعات شما ثبت شد. کارشناسان ما به زودی با شما تماس می‌گیرند.")
        message = f"درخواست همکاری جدید:\n🧑‍💼 نام: {name}\n📞 تماس با ما: {phone}\n\n🆔 @{update.message.from_user.username or 'ندارد'}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

    elif text == "📄 پلن‌ها و قیمت‌ها":
        await update.message.reply_text(
            "💡 پلن پایه: ۱۹۰ هزار تومان/ماه\n"
            "🚀 پلن حرفه‌ای: ۳۹۰ هزار تومان/ماه\n"
            "🏆 پلن طلایی: ۶۹۰ هزار تومان/ماه\n\n"
            "همه پلن‌ها شامل دامنه رایگان، هاست، SSL، پشتیبانی ۲۴ ساعته و قالب‌های آماده هستند."
        )

    elif text == "📞 تماس با ما":
        await update.message.reply_text(
            "برای تماس با پشتیبانی پیسان وب:\n📱 0911XXX1234\n📧 support@peysunweb.com"
        )

    elif text == "ℹ️ درباره ما":
        await update.message.reply_text(
            "پیسان وب یک پلتفرم سایت‌ساز حرفه‌ای ایرانیه که هدفش کمک به کسب‌وکارها برای ساخت سایت بدون نیاز به کدنویسی هست."
        )

    elif text == "🖼 نمونه کارها":
        await update.message.reply_text(
            "🎨 نمونه سایت‌های طراحی‌شده:\n"
            "1. فروشگاهی: https://example1.com\n"
            "2. شرکتی: https://example2.com\n"
            "3. رستوران: https://example3.com"
        )

    elif text == "❓ سوالات متداول":
        await update.message.reply_text(
            "❓ آیا می‌توانم سایت فروشگاهی بسازم؟\n✅ بله\n\n"
            "❓ آیا نیاز به دانش برنامه‌نویسی دارم؟\n✅ خیر\n\n"
            "❓ چند قالب آماده وجود دارد؟\n✅ بیش از ۱۰۰ قالب حرفه‌ای"
        )

    elif text == "🔗 شبکه‌های اجتماعی":
        await update.message.reply_text(
            "📱 شبکه‌های اجتماعی ما:\n"
            "📸 اینستاگرام: https://instagram.com/Peysunweb\n"
            "🔗 لینکدین: https://linkedin.com/in/Peysunweb\n"
            "▶️ یوتیوب: https://youtube.com/@Peysunweb\n"
            "📣 کانال تلگرام: https://t.me/peysunweb"
        )

    else:
        await update.message.reply_text("دستور ناشناخته. لطفا از دکمه‌های منو استفاده کنید.")

# ساخت و اجرای ربات
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("ربات روشنه... برو تلگرام تست کن!")
app.run_polling()
