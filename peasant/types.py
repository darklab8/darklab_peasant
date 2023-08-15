from typing import NewType

DiscordWebhookUrl = NewType("DiscordWebhookUrl", str)
TelegramChannelID = NewType("TelegramChannelID", str)
TelegramBotToken = NewType("TelegramBotToken", str)
RedisHostAddress = NewType("RedisHostAddress", str)
ChromeDriverVersion = NewType("ChromeDriverVersion", str)
LogLevel = NewType("LogLevel", str)
SeleniumLink = NewType("SeleniumLink", str)
GovRegistryLink = NewType("GovRegistryLink", SeleniumLink)
Seconds = NewType("Seconds", int)