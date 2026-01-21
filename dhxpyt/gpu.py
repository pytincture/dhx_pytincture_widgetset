"""
Lightweight WebGPU bridge for Pyodide environments.

Only two touchpoints are exposed:
1) enable_webgpu(**opts): initialize WebGPU globally (adapter/device options optional)
2) webgpu_status(): inspect availability and readiness
"""
import json
from typing import Any, Dict

import js


async def enable_webgpu(**options: Any) -> Dict[str, Any]:
    """
    Attempt to enable WebGPU globally via the frontend helper.

    Example:
        await enable_webgpu(adapterOptions={"powerPreference": "high-performance"})
    """
    helper = getattr(js.customdhx, "webgpu", None)
    if not helper or not hasattr(helper, "enable"):
        return {"supported": False, "enabled": False, "ready": False, "reason": "webgpu helper missing"}

    opts = js.JSON.parse(json.dumps(options or {}))
    result = await helper.enable(opts)
    return result.to_py() if hasattr(result, "to_py") else result


def webgpu_status() -> Dict[str, Any]:
    """
    Return the current WebGPU support/readiness status reported by the frontend.
    """
    helper = getattr(js.customdhx, "webgpu", None)
    if not helper or not hasattr(helper, "status"):
        return {"supported": False, "enabled": False, "ready": False, "reason": "webgpu helper missing"}

    result = helper.status()
    return result.to_py() if hasattr(result, "to_py") else result
