from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import wikipedia

# Set your bot token here
TOKEN = ""

# Set the default language (optional)
wikipedia.set_lang("en")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Hi! I'm a Wiki Bot.\n\n"
        "Send me any topic, and I’ll give you a short summary from Wikipedia."
    )

# Help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("❓ Just send me a word or phrase to search on Wikipedia.")

# Wikipedia search handler
async def search_wikipedia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text
    try:
        summary = wikipedia.summary(query, sentences=3)
        await update.message.reply_text(f"📘 {summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        options = '\n'.join(e.options[:5])
        await update.message.reply_text(
            f"🔍 Your search was too broad. Try one of these:\n\n{options}"
        )
    except wikipedia.exceptions.PageError:
        await update.message.reply_text("❌ No results found. Try a different keyword.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ An error occurred: {str(e)}")

# Main function to start the bot
def main() -> None:
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_wikipedia))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
