from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


def user_config_source(settings: BaseSettings) -> dict[str, Any]:
    encoding = settings.__config__.env_file_encoding
    return json.loads(Path("config.json").read_text(encoding))


class Settings(BaseSettings):
    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings
