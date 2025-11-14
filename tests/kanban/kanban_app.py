"""Minimal harness to exercise the custom Kanban widget."""

import os
import sys
from typing import Optional

from dhxpyt.layout import CellConfig, LayoutConfig, MainWindow
from dhxpyt.kanban import (
    Kanban,
    KanbanCardConfig,
    KanbanColumnConfig,
    KanbanConfig,
    KanbanLaneConfig,
)


class KanbanDemo(MainWindow):
    layout_config = LayoutConfig(
        type="line",
        rows=[CellConfig(id="kanban", height="100%")],
    )

    def __init__(self) -> None:
        super().__init__()
        self.set_theme(os.getenv("KANBAN_APP_THEME", "dark"))
        self._kanban: Optional[Kanban] = None

    def load_ui(self) -> None:  # type: ignore[override]
        config = self._build_config()
        # The layout helper wires the widget asynchronously, so we stash
        # a callback to capture the Python wrapper instance once ready.
        self.add_kanban(
            "kanban",
            kanban_config=config,
            kanban_callback=self._on_kanban_ready,
        )

    # ------------------------------------------------------------------
    # Kanban assembly
    # ------------------------------------------------------------------

    def _build_config(self) -> KanbanConfig:
        columns = [
            KanbanColumnConfig(
                id="check_in",
                title="Check-In",
                empty_text="No vehicles waiting at intake.",
                allow_add=False,
            ),
            KanbanColumnConfig(
                id="diagnostics",
                title="Diagnostics",
                empty_text="No vehicles on diagnostic bays.",
                allow_add=False,
            ),
            KanbanColumnConfig(
                id="awaiting_parts",
                title="Awaiting Parts",
                empty_text="All parts received.",
                allow_add=False,
            ),
            KanbanColumnConfig(
                id="repair",
                title="Repair In Progress",
                empty_text="No active repairs.",
                allow_add=False,
            ),
            KanbanColumnConfig(
                id="quality_check",
                title="Quality Check",
                empty_text="Nothing waiting on QC.",
                allow_add=False,
            ),
            KanbanColumnConfig(
                id="ready",
                title="Ready for Pickup",
                empty_text="No vehicles staged for delivery.",
                allow_add=False,
            ),
        ]

        unassigned_cards = [
            KanbanCardConfig(
                id="RO-7768",
                title="2014 Dodge Ram — ABS warning",
                status="check_in",
                description="Customer reported intermittent ABS light; needs diagnostic.",
                lane="unassigned",
                tags=["pending"],
            ),
            KanbanCardConfig(
                id="RO-7772",
                title="2012 Nissan Altima — A/C warm",
                status="check_in",
                description="Vehicle dropped overnight, estimate pending approval.",
                lane="unassigned",
                tags=["pending"],
            ),
        ]

        work_order_cards = [
            KanbanCardConfig(
                id="RO-7781",
                title="2019 Ford F-150 — Misfire under load",
                status="diagnostics",
                description="Scan PCM, verify coil harness, road test for knock events.",
                lane="alex",
                priority="High",
                due="10:30",
                tags=["Bay 2", "powertrain"],
            ),
            KanbanCardConfig(
                id="RO-7794",
                title="2021 Honda Civic — Brake pulsation",
                status="check_in",
                description="Measure rotor runout, prep lathe, torque sequence review.",
                lane="alex",
                tags=["Bay 5", "brakes"],
            ),
            KanbanCardConfig(
                id="RO-7802",
                title="2017 BMW X5 — Oil leak at pan",
                status="awaiting_parts",
                description="Confirm leak source, order gasket set, capture photos.",
                lane="bailey",
                tags=["Bay 7", "drivetrain"],
            ),
            KanbanCardConfig(
                id="RO-7816",
                title="2020 Tesla Model 3 — Suspension clunk",
                status="diagnostics",
                description="Inspect upper control arms, retorque knuckle bolts.",
                lane="bailey",
                tags=["Bay 4", "suspension", "ev"],
            ),
            KanbanCardConfig(
                id="RO-7828",
                title="2015 Jeep Wrangler — Transfer case swap",
                status="repair",
                description="Replace case assembly, refill ATF, recalibrate speed sensor.",
                lane="marco",
                progress=50,
                tags=["Bay 3", "4x4"],
            ),
            KanbanCardConfig(
                id="RO-7835",
                title="2018 Subaru Outback — Timing belt service",
                status="awaiting_parts",
                description="Install belt kit, replace water pump, bleed cooling system.",
                lane="marco",
                tags=["Bay 6", "maintenance"],
            ),
            KanbanCardConfig(
                id="RO-7842",
                title="2022 Chevy Silverado — ADAS calibration",
                status="quality_check",
                description="Align radar bracket, run static calibration, document results.",
                lane="taylor",
                tags=["Bay 1", "electronics"],
            ),
            KanbanCardConfig(
                id="RO-7851",
                title="2016 Toyota Camry — HVAC inoperative",
                status="repair",
                description="Diagnose blend door actuator, evac/recharge refrigerant.",
                lane="taylor",
                progress=20,
                tags=["Bay 8", "hvac"],
            ),
            KanbanCardConfig(
                id="RO-7864",
                title="2013 Audi A4 — Final detail & delivery",
                status="ready",
                description="Complete road test, wash exterior, stage paperwork for pickup.",
                lane="taylor",
                tags=["Bay 1", "delivery"],
            ),
        ]

        cards = unassigned_cards + work_order_cards

        lanes = [
            KanbanLaneConfig(id="unassigned", title="Unassigned Intake"),
            KanbanLaneConfig(id="alex", title="Alex Rivera", description="Drivability and diagnostic specialist"),
            KanbanLaneConfig(id="bailey", title="Bailey Kim", description="Suspension and EV systems"),
            KanbanLaneConfig(id="marco", title="Marco Diaz", description="Heavy-line drivetrain repairs"),
            KanbanLaneConfig(id="taylor", title="Taylor Singh", description="HVAC and advanced electronics"),
        ]

        return KanbanConfig(
            title="Vehicle Repair Workflow",
            description=(
                "Columns represent the repair status pipeline, while rows list the unassigned queue followed by "
                "each technician's bay."
            ),
            columns=columns,
            cards=cards,
            lanes=lanes,
            enable_lanes=True,
            add_column_text=None,
            add_card_text=None,
            theme=os.getenv("KANBAN_BOARD_THEME", "auto"),
            empty_board_text="Drag work orders onto a technician to assign.",
            extra={
                "signals": {"lastRefresh": "manual"}
            },
        )

    # ------------------------------------------------------------------
    # Event wiring
    # ------------------------------------------------------------------

    def _on_kanban_ready(self, board: Kanban) -> None:
        self._kanban = board
        board.on_card_click(self._log_event("cardClick"))
        board.on_card_move(self._log_event("cardMove"))
        board.on_card_create(self._log_event("cardCreate"))
        board.on_column_create(self._log_event("columnCreate"))
        board.on_column_toggle(self._log_event("columnToggle"))

    @staticmethod
    def _log_event(name: str):
        def handler(payload):
            print(f"[kanban_app] {name}: {payload}")
        return handler


if __name__ == "__main__" and sys.platform != "emscripten":
    from pytincture import launch_service

    launch_service(modules_folder=".")
