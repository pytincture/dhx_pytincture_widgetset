# chart.py
from typing import Any, Callable, List, Dict, Union
import js
import json
from pyodide.ffi import create_proxy

from .chart_config import ChartConfig

class Chart:
    """
    Python wrapper for DHTMLX Chart.

    This class provides a Pythonic interface to the DHTMLX Chart JavaScript library.
    It supports initialization with a configuration object, API methods, events, and properties.

    :param config: The configuration object for the chart (instance of ChartConfig or subclass).
    :param widget_parent: The parent DOM element for the chart (optional).
    """
    def __init__(self, config: ChartConfig, widget_parent: Any = None):
        """Initializes the chart instance with the given configuration."""
        self.chart = js.dhx.Chart.new(widget_parent, js.JSON.parse(json.dumps(config.to_dict())))

    """ Chart API Functions """

    def destructor(self) -> None:
        """Removes a chart instance and releases the occupied resources."""
        self.chart.destructor()

    def each_series(self, handler: Callable[[List[Dict[str, Any]]], Any]) -> List[Any]:
        """
        Iterates over chart series.

        :param handler: A callable that receives the list of series and returns a list of results.
        :return: List of results from the handler.
        """
        proxy_handler = create_proxy(handler)
        return self.chart.eachSeries(proxy_handler)

    def get_series(self, id: str) -> Dict[str, Any]:
        """
        Returns an object with configuration of a specified series.

        :param id: The ID of the series.
        :return: Dictionary of series configuration.
        """
        return self.chart.getSeries(id)

    def paint(self) -> None:
        """Repaints a chart on a page."""
        self.chart.paint()

    def set_config(self, config: Dict[str, Any]) -> None:
        """
        Sets configuration of a chart.

        :param config: Dictionary of configuration options.
        """
        self.chart.setConfig(js.JSON.parse(json.dumps(config)))

    def png(self, config: Dict[str, Any] = {}) -> None:
        """
        Exports a chart to a PNG file.

        :param config: Optional export configuration.
        """
        self.chart.png(js.JSON.parse(json.dumps(config)))

    def pdf(self, config: Dict[str, Any] = {}) -> None:
        """
        Exports a chart to a PDF file.

        :param config: Optional export configuration.
        """
        self.chart.pdf(js.JSON.parse(json.dumps(config)))

    """ Chart Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """
        Helper to add event handlers dynamically.

        :param event_name: The name of the event (e.g., 'resize').
        :param handler: The callable to handle the event.
        """
        event_proxy = create_proxy(handler)
        self.chart.events[event_name] = event_proxy

    def resize(self, handler: Callable[[int, int], None]) -> None:
        """
        Fires on changing the size of the chart container.

        :param handler: Callable that receives width and height.
        """
        self.add_event_handler('resize', handler)

    def serie_click(self, handler: Callable[[str, str], None]) -> None:
        """
        Fires on clicking a series.

        :param handler: Callable that receives series ID and item ID.
        """
        self.add_event_handler('serieClick', handler)

    def toggle_series(self, handler: Callable[[str, Union[Dict[str, Any], None]], None]) -> None:
        """
        Fires on toggle on/off a series in a legend.

        :param handler: Callable that receives series ID and series config (or None).
        """
        self.add_event_handler('toggleSeries', handler)

    """ Chart Properties """

    @property
    def css(self) -> str:
        """Gets the style classes added to the chart."""
        return self.chart.css

    @css.setter
    def css(self, value: str) -> None:
        """Sets style classes for the chart."""
        self.chart.css = value

    @property
    def data(self) -> List[Dict[str, Any]]:
        """Gets the array of data objects set into the chart."""
        return self.chart.data

    @data.setter
    def data(self, value: List[Dict[str, Any]]) -> None:
        """Sets the array of data objects for the chart."""
        self.chart.data = value

    @property
    def export_styles(self) -> Union[bool, List[str]]:
        """Gets the styles sent to the export service."""
        return self.chart.exportStyles

    @export_styles.setter
    def export_styles(self, value: Union[bool, List[str]]) -> None:
        """Sets the styles for export."""
        self.chart.exportStyles = value

    @property
    def legend(self) -> Dict[str, Any]:
        """Gets the configuration of the chart legend."""
        return self.chart.legend

    @legend.setter
    def legend(self, value: Dict[str, Any]) -> None:
        """Sets the configuration of the chart legend."""
        self.chart.legend = value

    @property
    def max_points(self) -> int:
        """Gets the maxPoints value for averaging large datasets."""
        return self.chart.maxPoints

    @max_points.setter
    def max_points(self, value: int) -> None:
        """Sets the maxPoints value."""
        self.chart.maxPoints = value

    @property
    def scales(self) -> Dict[str, Any]:
        """Gets the configuration of chart scales."""
        return self.chart.scales

    @scales.setter
    def scales(self, value: Dict[str, Any]) -> None:
        """Sets the configuration of chart scales."""
        self.chart.scales = value

    @property
    def series(self) -> List[Dict[str, Any]]:
        """Gets the configuration of chart series."""
        return self.chart.series

    @series.setter
    def series(self, value: List[Dict[str, Any]]) -> None:
        """Sets the configuration of chart series."""
        self.chart.series = value

    @property
    def type(self) -> str:
        """Gets the type of the chart."""
        return self.chart.type

    @type.setter
    def type(self, value: str) -> None:
        """Sets the type of the chart."""
        self.chart.type = value
