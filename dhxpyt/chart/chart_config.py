# chart_config.py
from typing import List, Union, Dict, Any, Optional

class ControlConfig:
    """Base class for control configurations."""
    def to_dict(self) -> Dict[str, Any]:
        """Converts the configuration object to a dictionary, excluding None values."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

class ChartConfig(ControlConfig):
    """
    Base configuration class for DHTMLX Chart.

    This class provides the common configuration options for all chart types.
    Subclasses should be used for specific chart types to ensure correct configuration
    and to enforce required properties based on the chart type.

    Note: Not all properties are applicable to all chart types. Refer to the documentation
    of subclasses for type-specific requirements and usage.

    :param type: The type of the chart (e.g., "line", "bar"). Required.
    :param series: Configuration of chart series as a list of dictionaries. Required for all types.
    :param scales: Configuration of chart scales as a dictionary. Required for some types (e.g., line, bar).
    :param data: An array of data objects to set into the chart. Optional.
    :param legend: Configuration of the chart legend as a dictionary. Optional for most types, required for Treemap.
    :param css: Style classes to add to the chart. Optional.
    :param max_points: Displays an average number of values if the dataset is too large. Optional, mainly for line/spline.
    :param export_styles: Defines styles sent to the export service. Defaults to False.
    """
    def __init__(self,
                 type: str,
                 series: List[Dict[str, Any]],
                 scales: Optional[Dict[str, Any]] = None,
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 max_points: Optional[int] = None,
                 export_styles: Union[bool, List[str]] = False):
        self.type = type
        self.series = series
        self.scales = scales
        self.data = data
        self.legend = legend
        self.css = css
        self.max_points = max_points
        self.export_styles = export_styles

class LineChartConfig(ChartConfig):
    """
    Configuration for Line chart.

    Required properties:
    - series: List of series configurations (e.g., [{id: "A", value: "company A", color: "#81C4E8", strokeWidth: 3}, ...])
    - scales: Dictionary of scales (e.g., {"bottom": {text: "month"}, "left": {max: 100}})

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration (e.g., {series: ["A"], halign: "right"}).
    - css: Custom CSS classes.
    - max_points: Average values for large datasets.
    - export_styles: Export styles.

    Example usage:
        config = LineChartConfig(series=[...], scales={...})
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 scales: Dict[str, Any],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 max_points: Optional[int] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="line", series=series, scales=scales, data=data, legend=legend,
                         css=css, max_points=max_points, export_styles=export_styles)

class SplineChartConfig(ChartConfig):
    """
    Configuration for Spline chart.

    Required properties:
    - series: List of series configurations (e.g., [{id: "A", value: "company A", color: "#81C4E8", strokeWidth: 3}, ...])
    - scales: Dictionary of scales (e.g., {"bottom": {text: "month"}, "left": {max: 100}})

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration.
    - css: Custom CSS classes.
    - max_points: Average values for large datasets.
    - export_styles: Export styles.

    Example usage:
        config = SplineChartConfig(series=[...], scales={...})
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 scales: Dict[str, Any],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 max_points: Optional[int] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="spline", series=series, scales=scales, data=data, legend=legend,
                         css=css, max_points=max_points, export_styles=export_styles)

class BarChartConfig(ChartConfig):
    """
    Configuration for Bar chart.

    Required properties:
    - series: List of series configurations (e.g., [{id: "A", value: "company A", fill: "#81C4E8"}, ...])
    - scales: Dictionary of scales (e.g., {"bottom": {text: "month"}, "left": {max: 100}})

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration.
    - css: Custom CSS classes.
    - max_points: Average values for large datasets (if applicable).
    - export_styles: Export styles.

    Example usage:
        config = BarChartConfig(series=[...], scales={...})
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 scales: Dict[str, Any],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 max_points: Optional[int] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="bar", series=series, scales=scales, data=data, legend=legend,
                         css=css, max_points=max_points, export_styles=export_styles)

class XBarChartConfig(ChartConfig):
    """
    Configuration for X-Bar (horizontal Bar) chart.

    Required properties:
    - series: List of series configurations.
    - scales: Dictionary of scales.

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration.
    - css: Custom CSS classes.
    - max_points: Average values for large datasets (if applicable).
    - export_styles: Export styles.

    Example usage:
        config = XBarChartConfig(series=[...], scales={...})
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 scales: Dict[str, Any],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 max_points: Optional[int] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="x-bar", series=series, scales=scales, data=data, legend=legend,
                         css=css, max_points=max_points, export_styles=export_styles)

class AreaChartConfig(ChartConfig):
    """
    Configuration for Area chart.

    Required properties:
    - series: List of series configurations (e.g., [{id: "A", value: "company A", color: "#81C4E8", strokeWidth: 3}, ...])
    - scales: Dictionary of scales.

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration.
    - css: Custom CSS classes.
    - max_points: Average values for large datasets (if applicable).
    - export_styles: Export styles.

    Example usage:
        config = AreaChartConfig(series=[...], scales={...})
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 scales: Dict[str, Any],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 max_points: Optional[int] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="area", series=series, scales=scales, data=data, legend=legend,
                         css=css, max_points=max_points, export_styles=export_styles)

class SplineAreaChartConfig(ChartConfig):
    """
    Configuration for SplineArea chart.

    Required properties:
    - series: List of series configurations.
    - scales: Dictionary of scales.

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration.
    - css: Custom CSS classes.
    - max_points: Average values for large datasets (if applicable).
    - export_styles: Export styles.

    Example usage:
        config = SplineAreaChartConfig(series=[...], scales={...})
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 scales: Dict[str, Any],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 max_points: Optional[int] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="splineArea", series=series, scales=scales, data=data, legend=legend,
                         css=css, max_points=max_points, export_styles=export_styles)

class PieChartConfig(ChartConfig):
    """
    Configuration for Pie chart.

    Required properties:
    - series: List of series configurations (e.g., [{value: "value", color: "color", text: "month"}])

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration (e.g., {values: {text: "id", color: "color"}}).
    - css: Custom CSS classes.
    - export_styles: Export styles.

    Note: Scales and max_points are not applicable.

    Example usage:
        config = PieChartConfig(series=[...])
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="pie", series=series, data=data, legend=legend,
                         css=css, export_styles=export_styles)

class Pie3DChartConfig(ChartConfig):
    """
    Configuration for Pie 3D chart.

    Required properties:
    - series: List of series configurations.

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration.
    - css: Custom CSS classes.
    - export_styles: Export styles.

    Note: Scales and max_points are not applicable.

    Example usage:
        config = Pie3DChartConfig(series=[...])
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="pie3D", series=series, data=data, legend=legend,
                         css=css, export_styles=export_styles)

class DonutChartConfig(ChartConfig):
    """
    Configuration for Donut chart.

    Required properties:
    - series: List of series configurations.

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration.
    - css: Custom CSS classes.
    - export_styles: Export styles.

    Note: Scales and max_points are not applicable.

    Example usage:
        config = DonutChartConfig(series=[...])
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="donut", series=series, data=data, legend=legend,
                         css=css, export_styles=export_styles)

class RadarChartConfig(ChartConfig):
    """
    Configuration for Radar chart.

    Required properties:
    - series: List of series configurations (e.g., [{id: "A", value: "company A", color: "#81C4E8", pointColor: "#81C4E8"}])
    - scales: Dictionary of scales (e.g., {"radial": {value: "month", maxTicks: 10}})

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration.
    - css: Custom CSS classes.
    - max_points: Average values for large datasets (if applicable).
    - export_styles: Export styles.

    Example usage:
        config = RadarChartConfig(series=[...], scales={...})
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 scales: Dict[str, Any],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 max_points: Optional[int] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="radar", series=series, scales=scales, data=data, legend=legend,
                         css=css, max_points=max_points, export_styles=export_styles)

class ScatterChartConfig(ChartConfig):
    """
    Configuration for Scatter chart.

    Required properties:
    - series: List of series configurations (e.g., [{id: "A_B", value: "value A", valueY: "value B", color: "#81C4E8", pointType: "circle"}])
    - scales: Dictionary of scales (e.g., {"bottom": {title: "value B"}, "left": {title: "value A"}})

    Optional properties:
    - data: Dataset to parse.
    - legend: Legend configuration.
    - css: Custom CSS classes.
    - max_points: Average values for large datasets (if applicable).
    - export_styles: Export styles.

    Example usage:
        config = ScatterChartConfig(series=[...], scales={...})
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 scales: Dict[str, Any],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 max_points: Optional[int] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="scatter", series=series, scales=scales, data=data, legend=legend,
                         css=css, max_points=max_points, export_styles=export_styles)

class TreeMapChartConfig(ChartConfig):
    """
    Configuration for Treemap chart.

    Required properties:
    - series: List of series configurations (e.g., [{value: "value", text: "name", stroke: "#eeeeee"}])
    - legend: Legend configuration (e.g., {type: "groupName", treeSeries: [...]} or {type: "range", treeSeries: [...]})

    Optional properties:
    - data: Dataset to parse (e.g., with parent-child relationships for groups).
    - css: Custom CSS classes.
    - export_styles: Export styles.

    Note: Scales and max_points are not applicable. Legend is required.

    Example usage:
        config = TreeMapChartConfig(series=[...], legend={...}, data=[...])
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 legend: Dict[str, Any],
                 data: Optional[List[Dict[str, Any]]] = None,
                 css: Optional[str] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="treeMap", series=series, legend=legend, data=data,
                         css=css, export_styles=export_styles)

class CalendarHeatMapChartConfig(ChartConfig):
    """
    Configuration for Calendar Heatmap chart.

    Required properties:
    - series: List of series configurations (e.g., [{value: "value", date: "date", positiveColor: "#04deb6", negativeColor: "#ff457a", weekStart: "monday", startDate: "01/03/22", endDate: "01/07/24"}])

    Optional properties:
    - data: Dataset to parse (e.g., [{value: 50, date: new Date(2022, 2, 2)}, ...]).
    - legend: Legend configuration (e.g., {values: {text: "Calendar heatmap chart"}}).
    - css: Custom CSS classes.
    - export_styles: Export styles.

    Note: Scales and max_points are not applicable. Use startDate and endDate in series for custom ranges.

    Example usage:
        config = CalendarHeatMapChartConfig(series=[...], data=[...])
    """
    def __init__(self,
                 series: List[Dict[str, Any]],
                 data: Optional[List[Dict[str, Any]]] = None,
                 legend: Optional[Dict[str, Any]] = None,
                 css: Optional[str] = None,
                 export_styles: Union[bool, List[str]] = False):
        super().__init__(type="calendarHeatMap", series=series, data=data, legend=legend,
                         css=css, export_styles=export_styles)
