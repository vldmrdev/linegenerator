import pytest

from linegenerator.presets import LogPreset

# TODO: add tests


class TestLogPreset:
    def test_has_at_least_nginx(self):
        assert hasattr(LogPreset, "NGINX")
        assert isinstance(LogPreset.NGINX, LogPreset)

    def test_value_is_string(self):
        assert isinstance(LogPreset.NGINX.value, str)
        assert len(LogPreset.NGINX.value) > 0

    def test_str_enum_behavior(self):
        assert str(LogPreset.NGINX) == LogPreset.NGINX.value
        assert f"Prefix: {LogPreset.NGINX}" == f"Prefix: {LogPreset.NGINX.value}"
        assert isinstance(LogPreset.NGINX, str)

    def test_get_valid_preset_by_name(self):
        assert LogPreset.get_preset("nginx") is LogPreset.NGINX
        assert LogPreset.get_preset("NGINX") is LogPreset.NGINX
        assert LogPreset.get_preset("Nginx") is LogPreset.NGINX

    def test_get_invalid_preset_raises_error(self):
        """Метод get_preset() должен выбрасывать ValueError при неверном имени"""
        with pytest.raises(ValueError, match="Unknown preset 'unknown'"):
            LogPreset.get_preset("unknown")

    def test_get_invalid_preset_includes_available_list(self):
        """Сообщение об ошибке должно содержать список доступных пресетов"""
        try:
            LogPreset.get_preset("unknown")
            pytest.fail("Expected ValueError")
        except ValueError as e:
            msg = str(e)
            assert "NGINX" in msg
            assert "Available:" in msg

    def test_member_names_are_correct(self):
        """Проверяем, что _member_names_ содержит правильные имена"""
        assert "NGINX" in LogPreset._member_names_

    def test_direct_access_via_enum_name(self):
        """Прямой доступ к .NGINX работает"""
        assert LogPreset["NGINX"] is LogPreset.NGINX
