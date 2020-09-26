from configparser import ConfigParser

from pyrogram import Client


class YamlBot(Client):
    def __init__(self, name):
        """Custom Client for YAM-Bot."""
        name = name.lower()
        config_file = f"{name}.ini"

        config = ConfigParser()
        config.read(config_file)

        plugins = dict(root=f"{name}.plugins", )

        super().__init__(
            name,
            config_file=config_file,
            workers=16,
            plugins=plugins,
            workdir="./",
            app_version="YamlBot v1.1",
        )

    async def start(self):
        await super().start()
        print("YamlBot started. Hi.")

    async def stop(self, *args):
        await super().stop()
        print("YamlBot stopped. Bye.")
