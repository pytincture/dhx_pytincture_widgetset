/* global window, document */

// Applies CSS custom properties to one or more selectors by injecting a scoped style tag.
// Expects a mapping { selector: { "--var": "value", ... }, ... }.
(function () {
    const STYLE_ID = "dhxpyt-theme-vars";

    function toCssRule(selector, vars) {
        const body = Object.keys(vars || {})
            .map((key) => `${key}: ${vars[key]};`)
            .join(" ");
        return body ? `${selector} { ${body} }` : "";
    }

    function applyCssVars(mapping) {
        if (!mapping || typeof mapping !== "object") return;
        const style = document.getElementById(STYLE_ID) || (() => {
            const el = document.createElement("style");
            el.id = STYLE_ID;
            document.head.appendChild(el);
            return el;
        })();

        const rules = Object.keys(mapping)
            .map((selector) => toCssRule(selector, mapping[selector]))
            .filter(Boolean)
            .join("\n");

        style.textContent = rules;
    }

    window.customdhx = window.customdhx || {};
    window.customdhx.applyCssVars = applyCssVars;
})();
