"""Simple demo harness for the CardPanel widget with a Python-driven template."""

import os
import sys
from typing import Optional

from dhxpyt.layout import CellConfig, LayoutConfig, MainWindow
from dhxpyt.cardpanel import CardPanel, CardPanelCardConfig, CardPanelConfig


class CardPanelDemo(MainWindow):
    layout_config = LayoutConfig(
        type="line",
        rows=[CellConfig(id="panel", height="100%")],
    )

    def __init__(self) -> None:
        super().__init__()
        self.set_theme(os.getenv("CARDPANEL_APP_THEME", "dark"))
        self._panel: Optional[CardPanel] = None

    def load_ui(self) -> None:  # type: ignore[override]
        config = self._build_config()
        self._panel = self.add_cardpanel("panel", cardpanel_config=config)
        if self._panel:
            self._panel.on_card_click(self._log_event("cardClick"))
            self._panel.on_view(self._log_event("view"))

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------

    def _build_config(self) -> CardPanelConfig:
        descriptor_template = {
            "tag": "article",
            "class": "cp-card",
            "dataset": {"cardId": "{id}"},
            "children": [
                {
                    "tag": "header",
                    "class": "cp-card__header",
                    "children": [
                        {
                            "tag": "div",
                            "class": "cp-card__badge",
                            "text": "{pill}",
                        },
                        {
                            "tag": "div",
                            "class": "cp-card__titlewrap",
                            "children": [
                                {"tag": "h3", "class": "cp-card__title", "text": "{title}"},
                                {"tag": "p", "class": "cp-card__subtitle", "text": "{subtitle}"},
                            ],
                        },
                    ],
                },
                {
                    "tag": "section",
                    "class": "cp-card__summary",
                    "text": "{summary}",
                },
                {
                    "tag": "ul",
                    "class": "cp-card__meta",
                    "children": [
                        {
                            "tag": "li",
                            "children": [
                                {"tag": "span", "class": "material-symbols-rounded", "text": "schedule"},
                                {"tag": "span", "text": "{updated}"},
                            ],
                        },
                        {
                            "tag": "li",
                            "children": [
                                {"tag": "span", "class": "material-symbols-rounded", "text": "link"},
                                {"tag": "span", "text": "{type}"},
                            ],
                        },
                    ],
                },
                {
                    "tag": "footer",
                    "class": "cp-card__footer",
                    "children": [
                        {
                            "tag": "button",
                            "class": "cp-card__action",
                            "text": "{cta}",
                            "attrs": {"data-id": "{id}"},
                        }
                    ],
                },
            ],
        }

        cards = [
            CardPanelCardConfig(
                id="datasource-analytics",
                title="Analytics Warehouse",
                subtitle="Snowflake · us-east-1",
                pill="Production",
                extra={
                    "summary": "Sales dashboards, retention cohorts, and usage insights updated hourly.",
                    "updated": "Refreshed 12 minutes ago",
                    "type": "Snowflake",
                    "cta": "Open workspace",
                },
            ),
            CardPanelCardConfig(
                id="datasource-lake",
                title="Raw Event Lake",
                subtitle="s3://company-lakehouse",
                pill="Gold",
                extra={
                    "summary": "S3-backed Delta tables with raw clickstream and mobile telemetry.",
                    "updated": "Synced yesterday at 23:40",
                    "type": "S3 + Delta",
                    "cta": "Browse catalog",
                },
            ),
            CardPanelCardConfig(
                id="datasource-finance",
                title="Finance Mart",
                subtitle="BigQuery · fin-prod",
                pill="Finance",
                extra={
                    "summary": "Revenue recognition and AP/AR extracts with row-level security policies.",
                    "updated": "Refreshed 3 hours ago",
                    "type": "BigQuery",
                    "cta": "Review policies",
                },
            ),
        ]

        return CardPanelConfig(
            title="Live Data Sources",
            description=(
                "Browse curated connections across teams. Templates below are built entirely from "
                "Python dictionaries — no custom JavaScript required."
            ),
            searchable=True,
            search_placeholder="Search data catalog…",
            auto_filter=True,
            cards=cards,
            view_button_text="Inspect",
            card_template=descriptor_template,
        )

    # ------------------------------------------------------------------
    # Event helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _log_event(name: str):
        def handler(payload):
            print(f"[cardpanel_app] {name}: {payload}")
        return handler


if __name__ == "__main__" and sys.platform != "emscripten":
    from pytincture import launch_service
    launch_service(modules_folder=".")
