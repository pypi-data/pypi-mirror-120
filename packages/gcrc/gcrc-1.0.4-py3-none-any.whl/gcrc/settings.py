from pydantic import BaseSettings


class Settings(BaseSettings):
    # Keep at minimum this many tags
    KEEP_TAGS_MIN: int = 10

    # Only clean up things older than this many days
    KEEP_TAGS_DAYS: int = 14

    # Keep more `KEEP_TAGS_MIN` instances of any tags matching these regexes
    KEEP_EXTRA: list[str] = ["^latest$", "^(master|main)-"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


conf = Settings()
