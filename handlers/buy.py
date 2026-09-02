from telegram import Update

from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
)

from services.payment import send_membership_invoice


async def buy_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await send_membership_invoice(
        bot=context.bot,
        chat_id=query.from_user.id,
        user_id=query.from_user.id
    )


async def pre_checkout(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.pre_checkout_query

    await query.answer(ok=True)


def get_buy_handlers():

    return [
        CallbackQueryHandler(
            buy_callback,
            pattern="^buy$"
        ),

        PreCheckoutQueryHandler(
            pre_checkout
        )
    ]
