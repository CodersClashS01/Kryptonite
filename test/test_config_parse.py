def test_config_parse():
    from config import config
    assert config.token == "NO TOKEN"
