import pytest

from src.config.settings import load_settings


def test_invalid_env_exits_with_variable_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOGGER__LEVEL", "LOUD")

    with pytest.raises(SystemExit, match="LOGGER__LEVEL"):
        load_settings()
