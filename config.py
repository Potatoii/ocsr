from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DECIMER",
    settings_files=[
        "settings.toml",
        "settings.dev.toml"
    ]
)
