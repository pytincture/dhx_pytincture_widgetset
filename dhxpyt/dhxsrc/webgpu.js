(function () {
    const state = {
        supported: typeof navigator !== "undefined" && !!navigator.gpu,
        enabled: false,
        ready: false,
        reason: null,
    };

    const widgetPrefs = new Map();
    let adapter = null;
    let device = null;

    function normalizeOptions(opts) {
        if (!opts || typeof opts !== "object") return {};
        return {
            adapterOptions: opts.adapterOptions || undefined,
            deviceOptions: opts.deviceOptions || undefined,
        };
    }

    async function enable(options = {}) {
        if (!state.supported) {
            state.reason = "WebGPU is not available (missing navigator.gpu)";
            return status();
        }
        if (state.enabled && state.ready) {
            return status();
        }

        try {
            const normalized = normalizeOptions(options);
            adapter = await navigator.gpu.requestAdapter(normalized.adapterOptions);
            if (!adapter) {
                state.reason = "Unable to acquire GPU adapter";
                return status();
            }
            device = await adapter.requestDevice(normalized.deviceOptions);
            state.enabled = true;
            state.ready = true;
            state.reason = null;
            device.lost.then((info) => {
                state.ready = false;
                state.enabled = false;
                state.reason = `Device lost: ${info.message || "unknown"}`;
            });
        } catch (err) {
            state.reason = err && err.message ? err.message : "Failed to initialize WebGPU";
        }
        return status();
    }

    function status() {
        return {
            supported: state.supported,
            enabled: state.enabled,
            ready: state.ready,
            reason: state.reason,
        };
    }

    function enableWidget(widgetId, flag = true) {
        if (!widgetId) return;
        if (flag) {
            widgetPrefs.set(widgetId, true);
        } else {
            widgetPrefs.delete(widgetId);
        }
    }

    function widgetEnabled(widgetId) {
        return !!(widgetId && widgetPrefs.get(widgetId) && state.ready);
    }

    function getDevice() {
        if (!state.ready || !device) {
            throw new Error("WebGPU device not ready");
        }
        return device;
    }

    globalThis.customdhx = globalThis.customdhx || {};
    globalThis.customdhx.webgpu = {
        enable,
        status,
        enableWidget,
        widgetEnabled,
        getDevice,
    };
})();
