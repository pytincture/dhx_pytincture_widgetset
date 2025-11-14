from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union


def _clean_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove keys whose value is ``None`` so we do not leak unset options into
    the JavaScript layer. Nested dictionaries are preserved intact so callers
    can explicitly pass nulls where required.
    """
    return {key: value for key, value in payload.items() if value is not None}


@dataclass
class KanbanCardConfig:
    """
    Represents a single card rendered on the Kanban board.
    """
    id: str
    title: str
    status: str
    description: Optional[str] = None
    lane: Optional[str] = None
    assignee: Optional[str] = None
    avatar: Optional[str] = None
    priority: Optional[str] = None
    due: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    progress: Optional[int] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    template: Optional[Any] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "description": self.description,
            "lane": self.lane,
            "assignee": self.assignee,
            "avatar": self.avatar,
            "priority": self.priority,
            "due": self.due,
            "tags": self.tags or None,
            "progress": self.progress,
            "meta": self.meta or None,
            "template": self.template,
        }
        payload.update(self.extra or {})
        return _clean_dict(payload)


@dataclass
class KanbanColumnConfig:
    """
    High level column configuration. Columns own the cards rendered inside of
    them and control limits and affordances.
    """
    id: str
    title: str
    limit: Optional[int] = None
    allow_drop: bool = True
    allow_add: bool = True
    collapsed: bool = False
    badge: Optional[str] = None
    order: Optional[int] = None
    empty_text: Optional[str] = None
    add_button_text: Optional[str] = None
    template: Optional[Any] = None
    cards: List[Union[KanbanCardConfig, Dict[str, Any]]] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cards_payload: List[Dict[str, Any]] = []
        for card in self.cards:
            if hasattr(card, "to_dict"):
                cards_payload.append(card.to_dict())
            elif isinstance(card, dict):
                cards_payload.append(card)
            else:
                raise TypeError(f"Unsupported card representation: {type(card)!r}")

        payload = {
            "id": self.id,
            "title": self.title,
            "limit": self.limit,
            "allowDrop": self.allow_drop,
            "allowAdd": self.allow_add,
            "collapsed": self.collapsed,
            "badge": self.badge,
            "order": self.order,
            "emptyText": self.empty_text,
            "addButtonText": self.add_button_text,
            "template": self.template,
            "cards": cards_payload,
        }
        payload.update(self.extra or {})
        return _clean_dict(payload)


@dataclass
class KanbanLaneConfig:
    """
    Optional swimlane configuration that groups columns by `lane_field`.
    """
    id: str
    title: str
    description: Optional[str] = None
    order: Optional[int] = None
    collapsed: bool = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "order": self.order,
            "collapsed": self.collapsed,
        }
        payload.update(self.extra or {})
        return _clean_dict(payload)


@dataclass
class KanbanConfig:
    """
    Top level configuration payload for the custom Kanban widget.
    """
    columns: List[Union[KanbanColumnConfig, Dict[str, Any]]] = field(default_factory=list)
    cards: List[Union[KanbanCardConfig, Dict[str, Any]]] = field(default_factory=list)
    lanes: Optional[List[Union[KanbanLaneConfig, Dict[str, Any]]]] = None
    lane_field: str = "lane"
    enable_lanes: bool = False
    allow_card_drag: bool = True
    allow_column_reorder: bool = False
    add_column_text: Optional[str] = None
    add_card_text: Optional[str] = "Add card"
    title: Optional[str] = None
    description: Optional[str] = None
    theme: str = "auto"
    card_template: Optional[Any] = None
    column_template: Optional[Any] = None
    empty_board_text: Optional[str] = None
    board_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        columns_payload: List[Dict[str, Any]] = []
        for column in self.columns:
            if hasattr(column, "to_dict"):
                columns_payload.append(column.to_dict())
            elif isinstance(column, dict):
                columns_payload.append(column)
            else:
                raise TypeError(f"Unsupported column representation: {type(column)!r}")

        cards_payload: List[Dict[str, Any]] = []
        for card in self.cards:
            if hasattr(card, "to_dict"):
                cards_payload.append(card.to_dict())
            elif isinstance(card, dict):
                cards_payload.append(card)
            else:
                raise TypeError(f"Unsupported card representation: {type(card)!r}")

        lanes_payload: Optional[List[Dict[str, Any]]] = None
        if self.lanes is not None:
            lanes_payload = []
            for lane in self.lanes:
                if hasattr(lane, "to_dict"):
                    lanes_payload.append(lane.to_dict())
                elif isinstance(lane, dict):
                    lanes_payload.append(lane)
                else:
                    raise TypeError(f"Unsupported lane representation: {type(lane)!r}")

        payload: Dict[str, Any] = {
            "columns": columns_payload,
            "cards": cards_payload,
            "lanes": lanes_payload,
            "laneField": self.lane_field,
            "enableLanes": self.enable_lanes,
            "allowCardDrag": self.allow_card_drag,
            "allowColumnReorder": self.allow_column_reorder,
            "addColumnText": self.add_column_text,
            "addCardText": self.add_card_text,
            "title": self.title,
            "description": self.description,
            "theme": self.theme,
            "cardTemplate": self.card_template,
            "columnTemplate": self.column_template,
            "emptyBoardText": self.empty_board_text,
            "boardId": self.board_id,
        }
        payload.update(self.extra or {})
        return _clean_dict(payload)
