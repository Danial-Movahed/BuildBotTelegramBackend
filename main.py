import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, MenuButton, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters, Application
from credentials import BOT_TOKEN, BOT_USERNAME
import json

LoadedProjects = {}


async def SetupAll(update: Update, callback: CallbackContext):
    await update.get_bot().set_chat_menu_button(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonWebApp(web_app=WebAppInfo(
            "https://danial-movahed.github.io/"),
            text="Open menu")
    )

    kb = [
        [KeyboardButton(
            "Open Menu",
            web_app=WebAppInfo("https://danial-movahed.github.io/")
        )],
        [KeyboardButton(
            "Help commands",
            web_app=WebAppInfo(
                "https://danial-movahed.github.io/help/commands")
        )]
    ]

    await update.message.reply_text(
        "Hello. Welcome to Danial's build bot. Check out menu for a gui or help for list of commands.",
        reply_markup=ReplyKeyboardMarkup(kb)
    )


async def web_app_data(update: Update, context: CallbackContext):
    data = json.loads(update.message.web_app_data.data)
    message = ""
    kb = [
        [KeyboardButton(
            "Open Dashboard",
            web_app=WebAppInfo(
                "https://danial-movahed.github.io/menus/projectloaded.html")
        )],
        [KeyboardButton(
            "Help commands",
            web_app=WebAppInfo(
                "https://danial-movahed.github.io/help/commands")
        )]
    ]
    if data["type"] == "Load":
        LoadedProjects[update.effective_user.id] = data["Project"]
        message = f"Loaded project {data['Project']}"

    elif data["type"] == "Unload":
        LoadedProjects[update.effective_user.id] = ""
        kb = [
            [KeyboardButton(
                "Open Menu",
                web_app=WebAppInfo("https://danial-movahed.github.io/")
            )],
            [KeyboardButton(
                "Help commands",
                web_app=WebAppInfo(
                    "https://danial-movahed.github.io/help/commands")
            )]
        ]
        message = "Unloaded project: " + data["Project"]

    elif data["type"] == "ConsoleStart":
        message = data["URL"]

    elif data["type"] == "InfoSet":
        message = f"Successfully set server info: \nServer Address: {data['Address']}\nServer Port: {data['Port']}"
        kb = [
            [KeyboardButton(
                "Open Menu",
                web_app=WebAppInfo("https://danial-movahed.github.io/")
            )],
            [KeyboardButton(
                "Help commands",
                web_app=WebAppInfo(
                    "https://danial-movahed.github.io/help/commands")
            )]
        ]

    await update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardMarkup(kb)
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', SetupAll))
    application.add_handler(MessageHandler(
        filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    print(
        f"Your bot is listening! Navigate to https://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()
