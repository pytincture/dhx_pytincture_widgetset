from typing import Any, Callable, List, Dict, Union
import js
import json
from pyodide.ffi import create_proxy

from .chart_config import ChartConfig

class Chart:
    def __init__(self, config: ChartConfig, widget_parent: Any = None):
        """Initializes the chart instance."""
        self.chart = js.dhx.Chart.new(widget_parent, js.JSON.parse(json.dumps(config.to_dict())))

    """ Chart API Functions """

    def destructor(self) -> None:
        """Removes a chart instance and releases the occupied resources."""
        self.chart.destructor()

    def each_series(self, handler: Callable[[List[Dict[str, Any]]], Any]) -> List[Any]:
        """Iterates over chart series."""
        proxy_handler = create_proxy(handler)
        return self.chart.eachSeries(proxy_handler)

    def get_series(self, id: str) -> Dict[str, Any]:
        """Returns an object with configuration of a specified series."""
        return self.chart.getSeries(id)

    def paint(self) -> None:
        """Repaints a chart on a page."""
        self.chart.paint()

    def set_config(self, config: Dict[str, Any]) -> None:
        """Sets configuration of a chart."""
        self.chart.setConfig(js.JSON.parse(json.dumps(config)))

    def png(self, config: Dict[str, Any] = {}) -> None:
        """Exports a chart to a PNG file."""
        self.chart.png(js.JSON.parse(json.dumps(config)))

    def pdf(self, config: Dict[str, Any] = {}) -> None:
        """Exports a chart to a PDF file."""
        self.chart.pdf(js.JSON.parse(json.dumps(config)))

    """ Chart Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.chart.events[event_name] = event_proxy

    def resize(self, handler: Callable[[int, int], None]) -> None:
        """Fires on changing the size of the chart container."""
        self.add_event_handler('resize', handler)

    def serie_click(self, handler: Callable[[str, str], None]) -> None:
        """Fires on clicking a series."""
        self.add_event_handler('serieClick', handler)

    def toggle_series(self, handler: Callable[[str, Union[Dict[str, Any], None]], None]) -> None:
        """Fires on toggle on/off a series in a legend."""
        self.add_event_handler('toggleSeries', handler)

    """ Chart Properties """

    @property
    def css(self) -> str:
        """Optional. Adds style classes to the chart."""
        return self.chart.css

    @css.setter
    def css(self, value: str) -> None:
        self.chart.css = value

    @property
    def data(self) -> List[Dict[str, Any]]:
        """Optional. Specifies an array of data objects to set into the chart."""
        return self.chart.data

    @data.setter
    def data(self, value: List[Dict[str, Any]]) -> None:
        self.chart.data = value

    @property
    def export_styles(self) -> Union[bool, List[str]]:
        """Optional. Defines the styles that will be sent to the export service when exporting Chart."""
        return self.chart.exportStyles

    @export_styles.setter
    def export_styles(self, value: Union[bool, List[str]]) -> None:
        self.chart.exportStyles = value

    @property
    def legend(self) -> Dict[str, Any]:
        """Optional. Defines the configuration of a chart legend."""
        return self.chart.legend

    @legend.setter
    def legend(self, value: Dict[str, Any]) -> None:
        self.chart.legend = value

    @property
    def max_points(self) -> int:
        """Optional. Displays an average number of values if data set is too large."""
        return self.chart.maxPoints

    @max_points.setter
    def max_points(self, value: int) -> None:
        self.chart.maxPoints = value

    @property
    def scales(self) -> Dict[str, Any]:
        """Required. Defines configuration of scales for certain chart types."""
        return self.chart.scales

    @scales.setter
    def scales(self, value: Dict[str, Any]) -> None:
        self.chart.scales = value

    @property
    def series(self) -> List[Dict[str, Any]]:
        """Required. Defines configuration of chart series."""
        return self.chart.series

    @series.setter
    def series(self, value: List[Dict[str, Any]]) -> None:
        self.chart.series = value

    @property
    def type(self) -> str:
        """Required. Specifies the type of a chart."""
        return self.chart.type

    @type.setter
    def type(self, value: str) -> None:
        self.chart.type = value
