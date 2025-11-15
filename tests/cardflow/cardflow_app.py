"""Demo harness for the CardFlow widget (vehicle repair work orders)."""

import os
import sys
from typing import Dict, List, Optional

from dhxpyt.layout import CellConfig, LayoutConfig, MainWindow
from dhxpyt.cardflow import CardFlow, CardFlowConfig, CardFlowColumnConfig


class CardFlowDemo(MainWindow):
    layout_config = LayoutConfig(
        type="line",
        rows=[CellConfig(id="flow", height="100%")],
    )

    def __init__(self) -> None:
        super().__init__()
        self.set_theme(os.getenv("CARDFLOW_APP_THEME", "dark"))
        self._cardflow: Optional[CardFlow] = None
        self._orders: List[Dict[str, str]] = []

    def load_ui(self) -> None:  # type: ignore[override]
        config = self._build_config()
        self._orders = config.data or []
        self._cardflow = self.add_cardflow("flow", cardflow_config=config)
        if not self._cardflow:
            return

        self._cardflow.on_card_expand(self._on_card_expand)
        self._cardflow.on_card_collapse(self._log_event("cardCollapse"))
        self._cardflow.on_options(self._log_event("cardOptions"))

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------

    def _build_config(self) -> CardFlowConfig:
        columns = [
            CardFlowColumnConfig(id="ticket", header="Ticket #", width="130px"),
            CardFlowColumnConfig(id="vehicle", header="Vehicle", width="220px"),
            CardFlowColumnConfig(id="technician", header="Technician", width="170px"),
            CardFlowColumnConfig(
                id="status",
                header="Status",
                width="150px",
            ),
            CardFlowColumnConfig(
                id="promise_time",
                header="Promise",
                width="140px",
                dataType="time",
                dataFormat="HH:MM AM/PM",
                applyFormat=True,
            ),
            CardFlowColumnConfig(id="bay", header="Bay", width="110px"),
            {"type": "stretch"},
        ]

        data = [
            {
                "id": "order-101",
                "ticket": "RO-101",
                "vehicle": "2019 Ford F-150",
                "technician": "Alex Rivera",
                "status": "Diagnostics",
                "promise_time": "09:30 AM",
                "bay": "Bay 2",
                "_color": "#2563eb",
            },
            {
                "id": "order-102",
                "ticket": "RO-102",
                "vehicle": "2012 Nissan Altima",
                "technician": "Alex Rivera",
                "status": "Waiting Parts",
                "promise_time": "11:45 AM",
                "bay": "Bay 5",
            },
            {
                "id": "order-103",
                "ticket": "RO-103",
                "vehicle": "2021 Honda Civic",
                "technician": "Bailey Kim",
                "status": "Intake",
                "promise_time": "12:15 PM",
                "bay": "Staging",
                "_color": "#d97706",
            },
            {
                "id": "order-104",
                "ticket": "RO-104",
                "vehicle": "2020 Tesla Model 3",
                "technician": "Bailey Kim",
                "status": "Repair",
                "promise_time": "02:05 PM",
                "bay": "Bay 4",
            },
            {
                "id": "order-105",
                "ticket": "RO-105",
                "vehicle": "2017 BMW X5",
                "technician": "Marco Diaz",
                "status": "Quality Check",
                "promise_time": "03:40 PM",
                "bay": "Bay 7",
                "_color": "#0891b2",
            },
        ]

        option_items = [
            {"id": "details", "value": "View Details"},
            {"id": "reassign", "value": "Reassign"},
            {"id": "hold", "value": "Place on Hold"},
            {"id": "cancel", "value": "Cancel Ticket"},
        ]

        return CardFlowConfig(
            columns=columns,
            data=data,
            sortHeader="Repair Workflow",
            optionItems=option_items,
            showHeader=True,
            showSort=True,
            showDataHeaders=True,
            fontSize="13px",
            defaultExpandedHeight="280px",
        )

    # ------------------------------------------------------------------
    # Event helpers
    # ------------------------------------------------------------------

    def _on_card_expand(self, card_id: str, *_args) -> None:
        print(f"[cardflow_app] cardExpand: {card_id}")
        if not self._cardflow:
            return
        order = next((item for item in self._orders if item["id"] == card_id), None)
        if not order:
            return
        accent = order.get("_color") or "#2563eb"
        self._cardflow.set_row_color(card_id, accent)

    @staticmethod
    def _log_event(name: str):
        def handler(*args, **kwargs):
            payload = args[0] if args else None
            print(f"[cardflow_app] {name}: {payload}")
        return handler


if __name__ == "__main__" and sys.platform != "emscripten":
    from pytincture import launch_service

    launch_service(modules_folder=".")
