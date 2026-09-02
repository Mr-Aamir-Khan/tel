import os

from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import (
    BOT_TOKEN,
    CHANNEL_ID,
    MEMBERSHIP_DAYS,
)

from handlers.start import (
    start_command,
    button_handler,
)

from handlers.buy import (
    get_buy_handlers,
)

from utils.helpers import (
    init_database,
    save_member,
)


# =========================================================
# TEMPORARY: CHECK CHAT ID
# =========================================================

async def channel_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat = update.effective_chat

    await update.message.reply_text(
        f"Current chat ID: {chat.id}"
    )


# =========================================================
# SUCCESSFUL PAYMENT
# =========================================================

async def successful_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    payment = update.message.successful_payment

    user = update.effective_user

    payment_id = (
        payment.telegram_payment_charge_id
    )

    expires_at = save_member(
        user_id=user.id,
        username=user.username or "",
        payment_id=payment_id,
        membership_days=MEMBERSHIP_DAYS
    )

    invite_link = None

    try:

        invite = await context.bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1
        )

        invite_link = invite.invite_link

    except Exception as error:

        print("Channel invite error:", error)

    if invite_link:

        text = (
            "✅ Payment Successful!\n\n"
            "Your membership is active.\n\n"
            f"Expires: {expires_at.strftime('%d %B %Y')}\n\n"
            "🔐 Your private channel invite:\n"
            f"{invite_link}\n\n"
            "⚠️ Do not share this invite link."
        )

    else:

        text = (
            "✅ Payment Successful!\n\n"
            "Your membership has been activated.\n\n"
            "However, the channel invite "
            "could not be generated automatically.\n\n"
            "Please contact support."
        )

    await update.message.reply_text(text)


# =========================================================
# UNKNOWN MESSAGE
# =========================================================

async def unknown_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Please use /start to open the menu."
    )


# =========================================================
# MAIN
# =========================================================

def main():

    init_database()

    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # /start
    application.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )

    # TEMPORARY /id command
    application.add_handler(
        CommandHandler(
            "id",
            channel_id
        )
    )

    # Main menu buttons
    application.add_handler(
        CallbackQueryHandler(
            button_handler,
            pattern="^(explore|membership|rules|support|home)$"
        )
    )

    # Buy + pre-checkout
    for handler in get_buy_handlers():
        application.add_handler(handler)

    # Successful Telegram Stars payment
    application.add_handler(
        MessageHandler(
            filters.SUCCESSFUL_PAYMENT,
            successful_payment
        )
    )

    # Unknown messages
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            unknown_message
        )
    )

    print("✅ Bot is running...")

    

    port = int(os.environ.get("PORT", 10000))

    application.run_webhook(
    listen="0.0.0.0",
    port=port,
    url_path=BOT_TOKEN,
    
    webhook_url=f"https://my-telegram-bot.onrender.com/{BOT_TOKEN}",

)



if __name__ == "__main__":
    main()
