from typing import Dict, Any

class BaseConfig:
    """
    Base configuration class that other config classes inherit from.
    Provides a method to convert the configuration to a dictionary.
    """
    def to_dict(self) -> Dict[str, Any]:
        """Converts the configuration object to a dictionary."""
        return {key: value for key, value in self.__dict__.items() if value is not None}
