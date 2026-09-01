import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def default_for(path: str, class_name: str, argument: str):
    module = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            initializer = next(
                item for item in node.body
                if isinstance(item, ast.FunctionDef) and item.name == "__init__"
            )
            positional = initializer.args.args[-len(initializer.args.defaults):]
            defaults = dict(zip((item.arg for item in positional), initializer.args.defaults))
            return ast.literal_eval(defaults[argument])
    raise AssertionError(f"{class_name}.{argument} was not found")


class BrowserContentSecurityContractTests(unittest.TestCase):
    def test_html_rendering_defaults_are_off(self):
        cases = (
            ("dhxpyt/grid/grid_config.py", "GridColumnConfig"),
            ("dhxpyt/grid/grid_config.py", "GridConfig"),
            ("dhxpyt/listbox/listbox_config.py", "ListboxConfig"),
            ("dhxpyt/combobox/combobox_config.py", "ComboboxConfig"),
        )
        for path, class_name in cases:
            with self.subTest(class_name=class_name):
                self.assertIs(default_for(path, class_name, "htmlEnable"), False)

    def test_chat_never_trusts_model_html_or_same_origin_artifacts(self):
        source = (ROOT / "dhxpyt/dhxsrc/chat.js").read_text(encoding="utf-8")
        self.assertIn('sandbox="allow-scripts"', source)
        self.assertNotIn('sandbox="allow-scripts allow-same-origin"', source)
        self.assertNotIn("marked.parse(text)", source)
        self.assertNotIn("exec(textwrap.dedent(code)", source)
        self.assertIn("event.origin !== \"null\"", source)
        self.assertIn("connect-src 'none'", source)

    def test_chat_history_and_preview_diagnostics_are_bounded_and_opt_in(self):
        source = (ROOT / "dhxpyt/dhxsrc/chat.js").read_text(encoding="utf-8")
        self.assertIn("DEFAULT_MAX_MESSAGES = 100", source)
        self.assertIn("MAX_ARTIFACT_CONSOLE_ENTRIES = 100", source)
        self.assertIn("includeArtifactConsoleInSend: false", source)
        self.assertIn('this._persistenceMode === "local"', source)
        self.assertIn('this._persistenceMode === "session"', source)
        self.assertIn("this.options.maxStorageBytes", source)

        config_module = ast.parse(
            (ROOT / "dhxpyt/chat/chat_config.py").read_text(encoding="utf-8")
        )
        chat_config = next(
            node for node in config_module.body
            if isinstance(node, ast.ClassDef) and node.name == "ChatConfig"
        )
        wanted = {
            "max_messages",
            "persistence",
            "include_artifact_console_in_send",
        }
        defaults = {}
        for node in chat_config.body:
            if (
                isinstance(node, ast.AnnAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id in wanted
                and node.value is not None
            ):
                defaults[node.target.id] = ast.literal_eval(node.value)
        self.assertEqual(defaults["max_messages"], 100)
        self.assertIsNone(defaults["persistence"])
        self.assertIs(defaults["include_artifact_console_in_send"], False)

    def test_data_driven_html_paths_apply_the_sanitizer(self):
        suite = (ROOT / "dhxpyt/dhxsrc/suite.js").read_text(encoding="utf-8")
        cardpanel = (ROOT / "dhxpyt/dhxsrc/cardpanel.js").read_text(encoding="utf-8")
        cardflow = (ROOT / "dhxpyt/dhxsrc/cardflow.js").read_text(encoding="utf-8")
        self.assertIn("htmlEnable ? dhxpytSanitizeHtml(content)", suite)
        self.assertIn('node[".innerHTML"] = dhxpytSanitizeHtml(html)', suite)
        self.assertIn("appendSanitizedHtml(content, card.contentHtml)", cardpanel)
        self.assertIn("icon.textContent = card.icon", cardpanel)
        self.assertIn("${escapeHtml(value)}", cardflow)
        self.assertIn("${escapeHtml(col.header)}", cardflow)


if __name__ == "__main__":
    unittest.main()
