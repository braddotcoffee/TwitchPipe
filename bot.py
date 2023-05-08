import yaml
import logging
from twitchio.ext import commands
from discord_webhook import DiscordWebhook


def load_config():
    with open("config.yaml", "r") as stream:
        return yaml.safe_load(stream)


class Bot(commands.Bot):
    def __init__(self, access_token, webhook_url):
        super().__init__(
            token=access_token, prefix="?", initial_channels=["braddoeslife"]
        )
        self.webhook_url = webhook_url

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        logging.info(f"Logged in as | {self.nick}")
        logging.info(f"User id is | {self.user_id}")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        message_str = f"[{message.author.name}]: {message.content}"
        webhook = DiscordWebhook(
            self.webhook_url, content=message_str, rate_limit_retry=True
        )
        webhook.execute()


def main():
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    bot = Bot(config["twitch"]["access_token"], config["discord"]["webhook_url"])
    bot.run()


if __name__ == "__main__":
    main()
