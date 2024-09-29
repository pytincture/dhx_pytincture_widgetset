from typing import List, Union, Dict, Any

class ControlConfig:
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

class ChartConfig(ControlConfig):
    """Configuration class for Chart."""
    def __init__(self,
                 type: str,
                 series: List[Dict[str, Any]],
                 scales: Dict[str, Any],
                 data: List[Dict[str, Any]] = None,
                 legend: Dict[str, Any] = None,
                 css: str = None,
                 max_points: int = None,
                 export_styles: Union[bool, List[str]] = False):
        self.type = type
        self.series = series
        self.scales = scales
        self.data = data
        self.legend = legend
        self.css = css
        self.max_points = max_points
        self.export_styles = export_styles