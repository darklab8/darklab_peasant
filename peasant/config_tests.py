from . import config
import json
import os


def test_config_not_exists():
    config.env_path = config.project_path / "not_existing.env.json"
    cfg = config.Config()


def test_json_config_exists():
    config.env_path = config.project_path / "existing.env.json"

    try:
        with open(str(config.env_path), "w") as file:
            file.write(
                json.dumps(
                    dict(
                        PEASANT_DEBUG=True,
                        PEASANT_RANDOM_STR="abc",
                    )
                )
            )
        cfg = config.Config()

        assert cfg.get_bool("debug") == True
        assert cfg.get_str("random_str") == "abc"
        assert cfg.get_str("rnd_str") == ""
        assert cfg.get_bool("debug2") == None
    finally:
        os.remove(str(config.env_path))


def test_config_grab_env_vars():
    cfg = config.Config()
    os.environ["PEASANT_DEBUG"] = "true"
    assert cfg.get_bool("debug") == True
    assert cfg.get_bool("debug2") == None
