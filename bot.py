from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import config
import time

WARN_LIMIT = 3
warns = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌹 CK ERROR OFFICIAL BOT\n\n"
        "Powerful Group Management Bot\n"
        "Use /help to see commands"
    )

# HELP
async def help_cmd(update: Update, context):
    await update.message.reply_text(
        "🌹 *CK ERROR OFFICIAL BOT*\n\n"
        "/rules - Group rules\n"
        "/warn - Warn user\n"
        "/ban - Ban user\n"
        "/kick - Kick user\n"
        "/mute <min> - Mute user\n"
        "/unmute - Unmute user\n"
        "/lock <type>\n"
        "/unlock <type>\n"
        "/pin /unpin",
        parse_mode="Markdown"
    )

# RULES
async def rules(update: Update, context):
    await update.message.reply_text(
        "📜 Group Rules:\n"
        "1. No spam\n"
        "2. No links\n"
        "3. Respect admins"
    )

# ADMIN CHECK
async def is_admin(update):
    admins = await update.effective_chat.get_administrators()
    return update.effective_user.id in [a.user.id for a in admins]

# WARN SYSTEM
async def warn(update: Update, context):
    if not await is_admin(update):
        return
    user = update.message.reply_to_message.from_user.id
    warns[user] = warns.get(user, 0) + 1

    if warns[user] >= WARN_LIMIT:
        await update.effective_chat.ban_member(user)
        await update.message.reply_text("🚫 User banned (warn limit reached)")
    else:
        await update.message.reply_text(f"⚠ Warn {warns[user]}/{WARN_LIMIT}")

# BAN
async def ban(update: Update, context):
    if not await is_admin(update):
        return
    user = update.message.reply_to_message.from_user.id
    await update.effective_chat.ban_member(user)
    await update.message.reply_text("🚫 User banned")

# KICK
async def kick(update: Update, context):
    if not await is_admin(update):
        return
    user = update.message.reply_to_message.from_user.id
    await update.effective_chat.ban_member(user)
    await update.effective_chat.unban_member(user)
    await update.message.reply_text("👢 User kicked")

# MUTE
async def mute(update: Update, context):
    if not await is_admin(update):
        return
    mins = int(context.args[0])
    user = update.message.reply_to_message.from_user.id
    until = int(time.time() + mins * 60)
    await update.effective_chat.restrict_member(
        user,
        ChatPermissions(can_send_messages=False),
        until_date=until
    )
    await update.message.reply_text(f"🔇 Muted for {mins} minutes")

# UNMUTE
async def unmute(update: Update, context):
    if not await is_admin(update):
        return
    user = update.message.reply_to_message.from_user.id
    await update.effective_chat.restrict_member(
        user,
        ChatPermissions(can_send_messages=True)
    )
    await update.message.reply_text("🔊 User unmuted")

# AUTO DELETE LINKS
async def anti_link(update: Update, context):
    if "http" in update.message.text:
        await update.message.delete()

# MAIN
app = ApplicationBuilder().token(config.BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_link))

app.run_polling()
