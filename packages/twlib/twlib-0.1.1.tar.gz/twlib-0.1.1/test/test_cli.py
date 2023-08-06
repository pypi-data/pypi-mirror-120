import pytest
from typer.testing import CliRunner

from twlib.git_open import app

runner = CliRunner()


class TestGitOpen:
    @pytest.mark.parametrize(
        ("path", "url"),
        (
            (
                "/Users/Q187392/dev/ENERGY-SERVICES/powerpool-v3/powerpool/service/simulation",
                "https://git.energyservices.cloud/energy-services/powerpool-v3/powerpool.git",
            ),
            (".", "https://github.com/sysid/twlib"),
        ),
    )
    def test_git_open(self, mocker, path, url):
        # result = runner.invoke(app, path)
        mocked = mocker.patch("twlib.git_open.webbrowser.open")
        result = runner.invoke(app, path)
        print(result.stdout)
        assert result.exit_code == 0
        assert url in result.stdout
