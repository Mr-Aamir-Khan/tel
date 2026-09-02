from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

from config import (
    PRICE_STARS,
    SUPPORT_USERNAME
)

from utils.helpers import get_membership


def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "✨ Explore",
                callback_data="explore"
            ),

            InlineKeyboardButton(
                "💎 Buy with Stars",
                callback_data="buy"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 My Membership",
                callback_data="membership"
            )
        ],

        [
            InlineKeyboardButton(
                "📜 Rules",
                callback_data="rules"
            ),

            InlineKeyboardButton(
                "🆘 Support",
                callback_data="support"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "🔞 Welcome!\n\n"

        "This is a private premium "
        "18+ community.\n\n"

        "By continuing, you confirm that "
        "you are 18+ and that accessing "
        "adult content is legal in your "
        "location.\n\n"

        "Choose an option below:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "home":

        await query.edit_message_text(
            "🏠 Main Menu\n\n"
            "Choose an option:",
            reply_markup=main_menu()
        )

    elif query.data == "explore":

        text = (
            "✨ Premium Membership\n\n"

            "• Private members-only community\n"
            "• Premium updates\n"
            "• Exclusive member content\n"
            "• 30-day access\n\n"

            f"Price: ⭐ {PRICE_STARS} Stars"
        )

        keyboard = [

            [
                InlineKeyboardButton(
                    "💎 Buy with Stars",
                    callback_data="buy"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="home"
                )
            ]

        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "membership":

        expires_at = get_membership(
            query.from_user.id
        )

        if (
            expires_at
            and expires_at.timestamp()
            > __import__("time").time()
        ):

            text = (
                "📋 My Membership\n\n"

                "Status: ✅ Active\n\n"

                f"Expires: "
                f"{expires_at.strftime('%d %B %Y')}"
            )

        else:

            text = (
                "📋 My Membership\n\n"
                "Status: ❌ Not active"
            )

        keyboard = [

            [
                InlineKeyboardButton(
                    "💎 Buy / Renew",
                    callback_data="buy"
                )
            ],

            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="home"
                )
            ]

        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "rules":

        text = (
            "📜 Rules\n\n"

            "1. Members must be 18+.\n"
            "2. Do not share private access links.\n"
            "3. Do not redistribute paid content.\n"
            "4. Respect members and creators.\n"
            "5. Only lawful and consensual content "
            "involving adults is permitted."
        )

        keyboard = [

            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="home"
                )
            ]

        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "support":

        if SUPPORT_USERNAME:

            keyboard = [

                [
                    InlineKeyboardButton(
                        "💬 Contact Support",
                        url=(
                            f"https://t.me/"
                            f"{SUPPORT_USERNAME}"
                        )
                    )
                ],

                [
                    InlineKeyboardButton(
                        "⬅️ Back",
                        callback_data="home"
                    )
                ]

            ]

            text = (
                "🆘 Support\n\n"
                "For payment or membership "
                "problems, contact support."
            )

        else:

            keyboard = [

                [
                    InlineKeyboardButton(
                        "⬅️ Back",
                        callback_data="home"
                    )
                ]

            ]

            text = (
                "🆘 Support\n\n"
                "Please contact the administrator."
            )

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
