import pytest

from src.config.settings import load_settings


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("LOGGER__LEVEL", "LOUD"),
        ("DATABASE__URL", "postgresql://u:p@localhost/db"),
    ],
)
def test_invalid_env_exits_with_variable_name(
    monkeypatch: pytest.MonkeyPatch, name: str, value: str
) -> None:
    monkeypatch.setenv(name, value)

    with pytest.raises(SystemExit, match=name):
        load_settings()
