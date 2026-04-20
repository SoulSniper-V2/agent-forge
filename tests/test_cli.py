from pathlib import Path

from click.testing import CliRunner

from agent_forge.cli import main, to_class_name


def test_to_class_name_normalizes_slugs():
    assert to_class_name("demo-bot") == "DemoBot"
    assert to_class_name("research_bot_v2") == "ResearchBotV2"
    assert to_class_name("123-agent") == "123Agent"


def test_create_generates_valid_scaffold():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            ["create", "demo-bot", "--provider", "openai", "--type", "chat", "--docker"],
        )

        assert result.exit_code == 0, result.output

        root = Path("demo-bot")
        assert (root / "README.md").exists()
        assert (root / ".gitignore").exists()
        assert (root / "tests" / "test_agent.py").exists()

        main_py = (root / "main.py").read_text()
        test_py = (root / "tests" / "test_agent.py").read_text()

        assert "DemoBotAgent" in main_py
        assert "Demo-BotAgent" not in test_py
        assert "TestClient" in test_py


def test_create_without_docker_skips_container_files():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(main, ["create", "tiny-agent", "--no-docker"])

        assert result.exit_code == 0, result.output

        root = Path("tiny-agent")
        assert not (root / "Dockerfile").exists()
        assert not (root / "docker-compose.yml").exists()
