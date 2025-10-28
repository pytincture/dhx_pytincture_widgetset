from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CardPanelCardConfig:
    """
    Represents an individual card shown inside the CardPanel widget.
    """
    id: str
    title: str
    subtitle: Optional[str] = None
    pill: Optional[str] = None
    icon: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "pill": self.pill,
            "icon": self.icon,
        }
        data.update(self.extra or {})
        return {key: value for key, value in data.items() if value is not None}


@dataclass
class CardPanelConfig:
    """
    High-level configuration for the CardPanel widget.
    """
    title: str = "Data Sources"
    description: str = "Manage and connect to various data sources with intelligent profiling and lineage tracking."
    searchable: bool = True
    auto_filter: bool = True
    cards: List[Any] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        cards_payload: List[Dict[str, Any]] = []
        for card in self.cards:
            if hasattr(card, "to_dict"):
                cards_payload.append(card.to_dict())
            elif isinstance(card, dict):
                cards_payload.append(card)
            else:
                raise TypeError(f"Unsupported card configuration type: {type(card)!r}")

        config_dict = {
            "title": self.title,
            "description": self.description,
            "searchable": self.searchable,
            "autoFilter": self.auto_filter,
            "cards": cards_payload,
        }
        return config_dict
