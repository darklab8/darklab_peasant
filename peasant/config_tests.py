from . import config
import json
import os
import pytest


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

        with pytest.raises(config.NotFoundValueAndNotDefinedDefault):
            cfg.get_str("rnd_str")
        with pytest.raises(config.NotFoundValueAndNotDefinedDefault):
            cfg.get_bool("debug2")
    finally:
        os.remove(str(config.env_path))


def test_config_grab_env_vars():
    cfg = config.Config()
    os.environ["PEASANT_DEBUG"] = "true"
    assert cfg.get_bool("debug") == True
    with pytest.raises(config.NotFoundValueAndNotDefinedDefault):
        assert cfg.get_bool("debug2") == None
