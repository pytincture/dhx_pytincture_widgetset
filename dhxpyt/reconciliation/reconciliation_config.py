from typing import Any, Dict, List, Union

class ReconciliationConfig:
    """
    Configuration class for the Reconciliation widget.
    """
    def __init__(self,
                 data: List[Dict[str, Any]] = None,
                ):
        """
        Initializes the reconciliation configuration with the provided data.
        Args:
            data (List[Dict[str, Any]], optional): A list of dictionaries containing the Reconciliation data. Defaults to None.
        """        
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ReconciliationConfig into a dictionary format.
        """
        config_dict = {
            "data": self.data,
        }

        return {k: v for k, v in config_dict.items() if v is not None}
