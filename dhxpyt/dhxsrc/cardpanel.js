function createUniqueId(prefix) {
    return `${prefix}_${Math.random().toString(16).slice(2)}`;
}

(function () {
    globalThis.customdhx = globalThis.customdhx || {};

    class CardPanel {
        constructor(target, options = {}) {
            this._events = {};
            this.cards = [];
            this._pendingActions = [];
            this._ready = false;
            this._eventsBound = false;
            this._mountId = null;
            this._domReadyPromise = null;

            this._ids = this._generateIds();

            if (!this._initializeLayout(target)) {
                throw new Error("Unable to initialize CardPanel: target container not found.");
            }

            this._bootstrap(options);
        }

        _generateIds() {
            const uid = Math.random().toString(16).slice(2);
            return {
                layoutCss: "cardpanel-layout",
                headerRow: `cardpanel_header_row_${uid}`,
                subheaderRow: `cardpanel_subheader_row_${uid}`,
                cardsRow: `cardpanel_cards_row_${uid}`,
                title: `cardpanel_title_${uid}`,
                description: `cardpanel_desc_${uid}`,
                searchWrap: `cardpanel_search_${uid}`,
                searchInput: `cardpanel_search_input_${uid}`,
                searchButton: `cardpanel_search_btn_${uid}`,
                addButton: `cardpanel_add_${uid}`,
                addButtonLabel: `cardpanel_add_label_${uid}`,
                grid: `cardpanel_grid_${uid}`
            };
        }

        _buildLayoutConfig() {
            return {
                css: this._ids.layoutCss,
                type: "none",
                rows: [
                    { id: this._ids.headerRow, height: "auto" },
                    { id: this._ids.subheaderRow, height: "auto" },
                    { id: this._ids.cardsRow, gravity: 1 }
                ]
            };
        }

        _initializeLayout(target) {
            if (!globalThis.dhx || typeof globalThis.dhx.Layout !== "function") {
                throw new Error("dhx.Layout is required for CardPanel.");
            }

            const config = this._buildLayoutConfig();

            if (target && typeof target.attach === "function") {
                this.layout = new dhx.Layout(null, config);
                target.attach(this.layout);
            } else if (target && typeof target.attachHTML === "function") {
                const mountId = createUniqueId("cardpanel_mount");
                target.attachHTML(`<div id="${mountId}" style="width:100%;height:100%;"></div>`);
                const mountEl = document.getElementById(mountId);
                if (!mountEl) {
                    return false;
                }
                this._mountId = mountId;
                this.layout = new dhx.Layout(mountEl, config);
            } else {
                const host = this._resolveDomTarget(target);
                if (!host) {
                    return false;
                }
                this.layout = new dhx.Layout(host, config);
            }

            this._attachShell();
            this._ensureDomReady();
            return true;
        }

        _resolveDomTarget(target) {
            if (typeof target === "string") {
                return document.querySelector(target);
            }

            if (target && (target.nodeType === 1 || target === document)) {
                return target;
            }

            return null;
        }

        _attachShell() {
            const headerCell = this.layout.getCell(this._ids.headerRow);
            const subheaderCell = this.layout.getCell(this._ids.subheaderRow);
            const cardsCell = this.layout.getCell(this._ids.cardsRow);

            if (!headerCell || !subheaderCell || !cardsCell) {
                throw new Error("CardPanel layout cells are not available.");
            }

            headerCell.attachHTML(this._headerTemplate());
            subheaderCell.attachHTML(this._subheaderTemplate());
            cardsCell.attachHTML(this._cardsTemplate());
        }

        _headerTemplate() {
            return `
                <div class="cardpanel-header">
                    <div class="cardpanel-header-left">
                        <div class="cardpanel-title" id="${this._ids.title}"></div>
                    </div>
                    <div class="cardpanel-actions">
                        <div class="cardpanel-search" id="${this._ids.searchWrap}">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                <path d="M21 21l-4.2-4.2" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"></path>
                                <circle cx="11" cy="11" r="7" stroke="#94a3b8" stroke-width="2"></circle>
                            </svg>
                            <input type="text" id="${this._ids.searchInput}" placeholder="Search data sources..." />
                            <button class="cardpanel-search-btn" id="${this._ids.searchButton}">Search</button>
                        </div>
                        <button class="cardpanel-add" id="${this._ids.addButton}">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="margin-right:6px;">
                                <path d="M12 5v14M5 12h14" stroke="white" stroke-width="2" stroke-linecap="round"></path>
                            </svg>
                            <span class="cardpanel-add-label" id="${this._ids.addButtonLabel}">Add Data Source</span>
                        </button>
                    </div>
                </div>
            `;
        }

        _subheaderTemplate() {
            return `
                <div class="cardpanel-subheader">
                    <div class="cardpanel-desc" id="${this._ids.description}"></div>
                </div>
            `;
        }

        _cardsTemplate() {
            return `
                <div class="cardpanel-grid" id="${this._ids.grid}"></div>
            `;
        }

        _cacheDomRefs() {
            this._titleEl = this._titleEl || document.getElementById(this._ids.title);
            this._descEl = this._descEl || document.getElementById(this._ids.description);
            this._searchWrapEl = this._searchWrapEl || document.getElementById(this._ids.searchWrap);
            this._input = this._input || document.getElementById(this._ids.searchInput);
            this._searchBtn = this._searchBtn || document.getElementById(this._ids.searchButton);
            this._addBtn = this._addBtn || document.getElementById(this._ids.addButton);
            this._addBtnLabel = this._addBtnLabel || document.getElementById(this._ids.addButtonLabel);
            this._grid = this._grid || document.getElementById(this._ids.grid);

            if (this._grid && !this._eventsBound) {
                this._wireEvents();
            }

            return Boolean(this._grid);
        }

        _ensureDomReady() {
            if (this._domReadyPromise) {
                return this._domReadyPromise;
            }

            this._domReadyPromise = new Promise((resolve) => {
                const attempt = () => {
                    if (this._cacheDomRefs()) {
                        resolve();
                        return;
                    }
                    window.requestAnimationFrame(attempt);
                };
                attempt();
            });

            return this._domReadyPromise;
        }

        _bootstrap(options) {
            this.options = Object.assign({
                title: "Data Sources",
                description: "Manage and connect to various data sources with intelligent profiling and lineage tracking.",
                searchable: true,
                searchPlaceholder: "Search data sources...",
                searchButtonText: "Search",
                addButtonText: "Add Data Source",
                viewButtonText: "View Details",
                autoFilter: true,
                cardMinWidth: 260,
                cardMinHeight: 160,
                cardGap: 16,
                cardIconSize: 44,
                cardTemplate: "default",
                cards: []
            }, options);

            this._injectStyles();
            this._ensureDomReady().then(() => {
                this._applyOptions();
                this._ready = true;

                if (Array.isArray(this.options.cards) && this.options.cards.length) {
                    this.load(this.options.cards);
                }

                this._flushPendingActions();
            });
        }

        _applyOptions() {
            if (this._titleEl) {
                this._titleEl.textContent = this.options.title || "";
            }

            if (this._descEl) {
                this._descEl.textContent = this.options.description || "";
                const wrapper = this._descEl.parentElement;
                if (wrapper) {
                    wrapper.style.display = this.options.description ? "" : "none";
                }
            }

            const showSearch = !(this.options.searchable === false || this.options.showSearch === false);
            if (this._searchWrapEl) {
                this._searchWrapEl.style.display = showSearch ? "flex" : "none";
            }

            if (this._input) {
                this._input.value = "";
                if (this.options.searchPlaceholder !== undefined && this.options.searchPlaceholder !== null) {
                    this._input.setAttribute("placeholder", this.options.searchPlaceholder);
                }
                if (this.options.searchAriaLabel) {
                    this._input.setAttribute("aria-label", this.options.searchAriaLabel);
                }
            }

            if (this._searchBtn && this.options.searchButtonText !== undefined && this.options.searchButtonText !== null) {
                this._searchBtn.textContent = this.options.searchButtonText;
            }

            if (this._addBtnLabel && this.options.addButtonText !== undefined && this.options.addButtonText !== null) {
                this._addBtnLabel.textContent = this.options.addButtonText;
            }

            if (this._addBtn) {
                this._addBtn.style.marginLeft = showSearch ? "" : "auto";
            }

            if (this._grid) {
                const minWidth = this._normalizeCssSize(this.options.cardMinWidth);
                const minHeight = this._normalizeCssSize(this.options.cardMinHeight);
                const gap = this._normalizeCssSize(this.options.cardGap);
                const iconSize = this._normalizeCssSize(this.options.cardIconSize);

                if (minWidth) {
                    this._grid.style.setProperty("--card-min-width", minWidth);
                } else {
                    this._grid.style.removeProperty("--card-min-width");
                }

                if (minHeight) {
                    this._grid.style.setProperty("--card-min-height", minHeight);
                } else {
                    this._grid.style.removeProperty("--card-min-height");
                }

                if (gap) {
                    this._grid.style.setProperty("--card-gap", gap);
                } else {
                    this._grid.style.removeProperty("--card-gap");
                }

                if (iconSize) {
                    this._grid.style.setProperty("--card-icon-size", iconSize);
                } else {
                    this._grid.style.removeProperty("--card-icon-size");
                }

                if (this.options.cardColumns && Number.isFinite(this.options.cardColumns)) {
                    const cols = Math.max(1, Math.floor(this.options.cardColumns));
                    this._grid.style.setProperty("--card-grid-template", `repeat(${cols}, minmax(0, 1fr))`);
                } else {
                    this._grid.style.removeProperty("--card-grid-template");
                }
            }

            if (!this._eventsBound) {
                this._wireEvents();
            }
        }

        _normalizeCssSize(value, defaultUnit = "px") {
            if (value === undefined || value === null) {
                return null;
            }

            if (typeof value === "number" && !Number.isNaN(value)) {
                return `${value}${defaultUnit}`;
            }

            if (typeof value === "string") {
                return value.trim() ? value : null;
            }

            return null;
        }

        _createTemplateContext(index, card) {
            const panel = this;
            return {
                panel,
                card,
                index,
                emit(name, ...args) {
                    panel.emit(name, ...args);
                }
            };
        }

        _enqueueAction(action) {
            if (this._ready) {
                action();
            } else {
                this._pendingActions.push(action);
            }
        }

        _flushPendingActions() {
            if (!this._pendingActions.length) {
                return;
            }

            const pending = this._pendingActions.slice();
            this._pendingActions.length = 0;

            pending.forEach((fn) => {
                try {
                    fn();
                } catch (err) {
                    console.error(err);
                }
            });
        }

        _wireEvents() {
            if (this._eventsBound) {
                return;
            }

            if (this._searchBtn) {
                this._searchBtn.addEventListener("click", () => {
                    const query = (this._input?.value || "").trim();
                    this.emit("search", query);
                    if (this.options.autoFilter) {
                        this._filter(query);
                    }
                });
            }

            if (this._input) {
                this._input.addEventListener("keyup", (event) => {
                    const query = (this._input?.value || "").trim();

                    if (event.key === "Enter") {
                        this.emit("search", query);
                    }

                    if (this.options.autoFilter) {
                        this._filter(query);
                    }
                });
            }

            if (this._addBtn) {
                this._addBtn.addEventListener("click", () => {
                    this.emit("add");
                });
            }

            this._eventsBound = true;
        }

        on(name, handler) {
            if (typeof handler !== "function") {
                return;
            }
            this._events[name] = this._events[name] || [];
            this._events[name].push(handler);
        }

        off(name, handler) {
            if (!this._events[name]) {
                return;
            }
            this._events[name] = this._events[name].filter((h) => h !== handler);
        }

        emit(name, ...args) {
            (this._events[name] || []).forEach((handler) => {
                try {
                    handler(...args);
                } catch (err) {
                    console.error(err);
                }
            });
        }

        _injectStyles() {
            if (document.querySelector("style[data-cardpanel-style='true']")) {
                return;
            }

const css = `
.cardpanel-layout {
    --bg: #f4f6fb;
    --panel: #ffffff;
    --panel-2: #eff3fb;
    --text: #172033;
    --muted: #5d6a7e;
    --brand: #2563eb;
    --accent: #2b9cdb;
    --btn: #2563eb;
    --btn-hover: #1d4ed8;
    --chip: #e8eefc;
    --surface-border: #d6deea;
    --card-border: #d0d8e6;
    --pill-text: #1f2a44;
    --shadow: 0 12px 30px rgba(15, 23, 42, 0.12);
    --card-min-width: 260px;
    --card-min-height: 160px;
    --card-gap: 16px;
    --card-icon-size: 44px;
    --card-border-hover: #334155;
    --card-grid-template: repeat(auto-fit, minmax(var(--card-min-width), 1fr));

    background: var(--bg);
    height: 100%;
    color: var(--text);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    box-sizing: border-box;
}
.cardpanel-layout .dhx_layout-cell {
    background: transparent;
    border: none;
    padding: 0;
}

html[data-dhx-theme="dark"] .cardpanel-layout {
    --bg: #0f1217;
    --panel: #151a22;
    --panel-2: #1b222d;
    --text: #e9eef6;
    --muted: #9aa6b2;
    --brand: #3b82f6;
    --accent: #2dd4bf;
    --btn: #2563eb;
    --btn-hover: #1d4ed8;
    --chip: #0b1220;
    --surface-border: #2a384c;
    --card-border: #364760;
    --card-border-hover: #4e6384;
    --pill-text: #cbd5e1;
    --shadow: 0 8px 24px rgba(0,0,0,.35);
    --card-min-width: 260px;
    --card-min-height: 160px;
    --card-gap: 16px;
    --card-icon-size: 44px;
    --card-grid-template: repeat(auto-fit, minmax(var(--card-min-width), 1fr));
}
.cardpanel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 14px 18px;
    background: var(--panel);
    border-bottom: 1px solid var(--surface-border);
}
.cardpanel-title {
    font-size: 20px;
    font-weight: 600;
    letter-spacing: .2px;
}
.cardpanel-actions { display:flex; gap:12px; align-items:center; width:100%; justify-content:flex-end; }
.cardpanel-search {
    flex: 1;
    display: flex; align-items: center; gap: 10px;
    background: var(--panel-2);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 10px 12px;
}
.cardpanel-search input {
    flex: 1; background: transparent; border: none; outline: none;
    color: var(--text); font-size: 14px;
}
.cardpanel-search-btn {
    background: var(--brand);
    color: #fff;
    border: none;
    border-radius: 9999px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;
    box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
}
.cardpanel-search-btn:hover { background: var(--btn-hover); }

.cardpanel-add {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--btn); color: #fff;
    border: none; border-radius: 10px; padding: 10px 14px;
    font-weight: 600; cursor: pointer;
    box-shadow: var(--shadow);
}
.cardpanel-add:hover { background: var(--btn-hover); }
.cardpanel-add svg { flex-shrink: 0; }
.cardpanel-add-label { display: inline-block; }

.cardpanel-subheader {
    padding: 20px 24px 10px 24px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    border-bottom: 1px solid var(--surface-border);
}
.cardpanel-desc { color: var(--muted); font-size: 14px; max-width: 900px; }

.cardpanel-grid {
    padding: 24px;
    display: grid;
    grid-template-columns: var(--card-grid-template);
    gap: var(--card-gap);
    background: transparent;
    overflow: auto;
}

.card-card {
    background: var(--panel);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 18px;
    box-shadow: var(--shadow);
    display: flex; flex-direction: column; gap: 14px;
    min-height: var(--card-min-height);
    transition: transform .15s ease, border-color .15s ease;
    cursor: pointer;
}
.card-card:hover { transform: translateY(-4px); border-color: var(--card-border-hover); }
.card-head { display:flex; align-items:center; gap:14px; }
.card-icon {
    width:var(--card-icon-size); height:var(--card-icon-size); display:grid; place-items:center;
    border-radius:12px; background: var(--chip);
    border:1px solid var(--surface-border);
}
.card-title { margin:0; font-size:16px; font-weight:700; letter-spacing:.2px; color:var(--text); }
.card-sub { color: var(--muted); font-size:13px; line-height:1.4; }
.card-foot { margin-top:auto; display:flex; justify-content:flex-end; }
.card-content { color: var(--text); font-size:14px; line-height:1.45; }

.card-view {
    background: var(--brand); border: none; color: #fff; font-weight:600;
    padding: 8px 12px; border-radius: 10px; cursor: pointer;
}
.card-view:hover { background: var(--btn-hover); }

.card-pill {
    display:inline-block; padding:3px 8px; border-radius:999px;
    background:var(--chip); color:var(--pill-text); border:1px solid var(--surface-border); font-size:12px;
}
`;

            const style = document.createElement("style");
            style.textContent = css;
            style.setAttribute("data-cardpanel-style", "true");
            document.head.appendChild(style);
        }

        load(cards) {
            this._enqueueAction(() => {
                this.cards = Array.isArray(cards) ? cards.map((card) => Object.assign({}, card)) : [];
                this._renderCards();
            });
        }

        add(card) {
            this._enqueueAction(() => {
                const copy = Object.assign({}, card);
                this.cards.push(copy);
                this._renderCards();
            });
        }

        _resolveTemplateRenderer() {
            const ctor = this.constructor;
            const templateRef = this.options.cardTemplate ?? "default";

            if (typeof templateRef === "function") {
                return (card, context) => templateRef.call(this, card, context);
            }

            const factory = typeof ctor.getTemplate === "function" ? ctor.getTemplate(templateRef) : null;
            const fallback = typeof ctor.getTemplate === "function" ? ctor.getTemplate("default") : null;
            const effectiveFactory = typeof factory === "function" ? factory : fallback;

            if (typeof effectiveFactory !== "function") {
                throw new Error(`CardPanel template '${templateRef}' is not registered.`);
            }

            const renderer = effectiveFactory(this);
            if (typeof renderer !== "function") {
                throw new Error("CardPanel template factory must return a renderer function.");
            }
            return renderer;
        }

        _renderCards() {
            if (!this._grid) {
                return;
            }

            this._grid.innerHTML = "";

            const renderer = this._resolveTemplateRenderer();

            this.cards.forEach((card, index) => {
                let rendered;
                try {
                    rendered = renderer(card, this._createTemplateContext(index, card));
                } catch (err) {
                    console.error("CardPanel template render failed:", err);
                    return;
                }

                if (typeof rendered === "string") {
                    const temp = document.createElement("div");
                    temp.innerHTML = rendered.trim();
                    rendered = temp.firstElementChild;
                }

                if (!(rendered instanceof HTMLElement)) {
                    console.warn("CardPanel template must return a DOM element or HTML string.");
                    return;
                }

                if (!rendered.dataset.cardId && card.id) {
                    rendered.dataset.cardId = card.id;
                }

                this._grid.appendChild(rendered);
            });
        }

        _filter(query) {
            if (!this._grid) {
                return;
            }

            const term = (query || "").toLowerCase();
            const children = Array.from(this._grid.children);

            children.forEach((child) => {
                const id = child.dataset.cardId || "";
                const card = this.cards.find((c) => (c.id || "") === id);

                if (!card) {
                    return;
                }

                const haystack = [
                    card.title || "",
                    card.subtitle || "",
                    card.pill || ""
                ].join(" ").toLowerCase();

                child.style.display = !term || haystack.indexOf(term) !== -1 ? "" : "none";
            });
        }

        destroy() {
            this.destructor();
        }

        destructor() {
            if (this.layout && typeof this.layout.destructor === "function") {
                this.layout.destructor();
            }

            this._events = {};
            this.cards = [];
            this._grid = null;

            if (this._mountId) {
                const element = document.getElementById(this._mountId);
                if (element && element.parentElement) {
                    element.parentElement.removeChild(element);
                }
                this._mountId = null;
            }
        }
    }

    CardPanel._templateFactories = CardPanel._templateFactories || new Map();

    CardPanel.registerTemplate = function (name, factory) {
        if (typeof name !== "string" || !name.trim()) {
            throw new Error("CardPanel.registerTemplate requires a non-empty string name.");
        }
        if (typeof factory !== "function") {
            throw new Error("CardPanel.registerTemplate requires a factory function.");
        }
        CardPanel._templateFactories.set(name, factory);
    };

    CardPanel.getTemplate = function (name) {
        if (typeof name !== "string") {
            return null;
        }
        return CardPanel._templateFactories.get(name) || null;
    };

    if (!CardPanel.getTemplate("default")) {
        CardPanel.registerTemplate("default", (panel) => (card) => {
            const cardDiv = document.createElement("div");
            cardDiv.className = "card-card";
            cardDiv.dataset.cardId = card.id || "";

            const head = document.createElement("div");
            head.className = "card-head";

            if (card.icon) {
                const icon = document.createElement("div");
                icon.className = "card-icon";
                icon.innerHTML = card.icon;
                head.appendChild(icon);
            }

            const titles = document.createElement("div");
            titles.style.display = "flex";
            titles.style.flexDirection = "column";
            titles.style.gap = "4px";

            const title = document.createElement("h3");
            title.className = "card-title";
            title.textContent = card.title || "Untitled";
            titles.appendChild(title);

            if (card.subtitle) {
                const subtitle = document.createElement("p");
                subtitle.className = "card-sub";
                subtitle.textContent = card.subtitle;
                titles.appendChild(subtitle);
            }

            if (card.pill) {
                const pill = document.createElement("span");
                pill.className = "card-pill";
                pill.textContent = card.pill;
                titles.appendChild(pill);
            }

            head.appendChild(titles);
            cardDiv.appendChild(head);

            if (card.contentHtml) {
                const content = document.createElement("div");
                content.className = "card-content";
                content.innerHTML = card.contentHtml;
                cardDiv.appendChild(content);
            }

            if (card.summary) {
                const summary = document.createElement("p");
                summary.className = "card-sub";
                summary.textContent = card.summary;
                cardDiv.appendChild(summary);
            }

            const viewEnabled = card.viewButton !== false && card.hideViewButton !== true;
            if (viewEnabled) {
                const foot = document.createElement("div");
                foot.className = "card-foot";

                const viewBtn = document.createElement("button");
                viewBtn.className = "card-view";
                viewBtn.textContent = card.viewButtonText || panel.options.viewButtonText || "View Details";
                viewBtn.addEventListener("click", (event) => {
                    event.stopPropagation();
                    panel.emit("view", card);
                });
                foot.appendChild(viewBtn);

                cardDiv.appendChild(foot);
            }

            cardDiv.addEventListener("click", () => {
                panel.emit("cardClick", card);
            });

            return cardDiv;
        });
    }

    globalThis.customdhx.CardPanel = CardPanel;
})();
