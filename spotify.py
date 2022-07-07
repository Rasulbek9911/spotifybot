import logging
import requests

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}\n enter the name of the music!",
    )


def url_short(longurl):
    url = "https://url-shortener-service.p.rapidapi.com/shorten"

    payload = f"url={longurl}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "121b25f3f2mshda49a84042c1068p1c2baajsnd6f425e6a152",
        "X-RapidAPI-Host": "url-shortener-service.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.json()['result_url']


def spotify(music_text):
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download"

    querystring = {"track": music_text}

    headers = {
        "X-RapidAPI-Key": "121b25f3f2mshda49a84042c1068p1c2baajsnd6f425e6a152",
        "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.json()['status']:
        print(f"{response.json()['youtubeVideo']['title']}\n{response.json()['youtubeVideo']['audio'][0]['url']}")
        return f"{response.json()['youtubeVideo']['title']}\n{response.json()['youtubeVideo']['audio'][0]['url']}"

    return "music not found"


def you_id(id):
    url = "https://ytstream-download-youtube-videos.p.rapidapi.com/dl"

    querystring = {"id": id, "geo": "DE"}

    headers = {
        "X-RapidAPI-Key": "121b25f3f2mshda49a84042c1068p1c2baajsnd6f425e6a152",
        "X-RapidAPI-Host": "ytstream-download-youtube-videos.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.json()['link']['18'][0])
    return f"{response.json()['title']}\n{response.json()['link']['18'][0]}"


async def youtobe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = update.message.text.split()[1]
    print(id)
    await update.message.reply_text(you_id(id))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(spotify(update.message.text))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("1996578306:AAFp5cUKvjDoYldUjgQ-3sYG416CLLcnfj0").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('youtobe', youtobe))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
