from . import types
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class SettingsB(BaseModel):
    debug: bool = False
    driver_version: types.ChromeDriverVersion = types.ChromeDriverVersion("114.0.5735.90")
    celery_redis_host: types.RedisHostAddress = types.RedisHostAddress("redis://localhost:6379/0")
    selenium_await_time: types.Seconds = types.Seconds(30)
    selenium_attempts_solving_captcha: int = 4
    selenium_delay: types.Seconds = types.Seconds(1)

    discord_channel_health: types.DiscordWebhookUrl
    discord_channel_news: types.DiscordWebhookUrl
    telegram_bot_token: types.TelegramBotToken
    telegram_channel_health: types.TelegramChannelID
    telegram_channel_news: types.TelegramChannelID
    log_level: types.LogLevel = types.LogLev.DEBUG
    selenium_reg_link: types.GovRegistryLink
    twocaptcha_api_key: types.TwoCatpchaApiKey
    test_mode: bool

class Settings(BaseSettings, SettingsB):
    model_config = SettingsConfigDict(env_prefix='', case_sensitive=False,)
