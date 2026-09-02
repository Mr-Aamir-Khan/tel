from telegram import LabeledPrice

from config import PRICE_STARS


async def send_membership_invoice(
    bot,
    chat_id,
    user_id
):

    prices = [
        LabeledPrice(
            label="30-Day Premium Membership",
            amount=PRICE_STARS
        )
    ]

    await bot.send_invoice(
        chat_id=chat_id,
        title="Premium Membership",
        description=(
            "30-day membership to the "
            "private premium community."
        ),
        payload=f"membership:{user_id}",
        currency="XTR",
        prices=prices,
        provider_token=""
    )
