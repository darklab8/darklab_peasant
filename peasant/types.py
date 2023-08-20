from typing import NewType, Type

DiscordWebhookUrl = NewType("DiscordWebhookUrl", str)
TelegramChannelID = NewType("TelegramChannelID", str)
TelegramBotToken = NewType("TelegramBotToken", str)
RedisHostAddress = NewType("RedisHostAddress", str)
ChromeDriverVersion = NewType("ChromeDriverVersion", str)
LogLevel = NewType("LogLevel", str)
SeleniumLink = NewType("SeleniumLink", str)
GovRegistryLink = NewType("GovRegistryLink", SeleniumLink)
Seconds = NewType("Seconds", int)
TwoCatpchaApiKey = NewType("TwoCatpchaApiKey", str)

ExcType = Type[Exception]

class LogLev:
    """
    Change to Enum later :smile:
    """

    DEBUG = LogLevel("DEBUG")
    INFO = LogLevel("INFO")
    ERROR = LogLevel("ERROR")
    PANIC = LogLevel("PANIC")
