(function () {
    "use strict";

    const DEFAULT_OPTIONS = {
        title: null,
        description: null,
        enableLanes: false,
        laneField: "lane",
        allowCardDrag: true,
        allowColumnReorder: false,
        addColumnText: null,
        addCardText: "Add card",
        emptyBoardText: "No cards yet",
        theme: "auto",
        cardTemplate: null,
        columnTemplate: null,
        boardId: null,
    };

    const CARD_TEMPLATES = new Map();
    const COLUMN_TEMPLATES = new Map();

    function createUniqueId(prefix) {
        const idPrefix = prefix || "kanban";
        return `${idPrefix}-${Math.random().toString(16).slice(2)}-${Date.now().toString(16)}`;
    }

    function deepClone(value) {
        if (typeof structuredClone === "function") {
            try {
                return structuredClone(value);
            } catch (err) {
                console.warn("[KanbanBoard] structuredClone failed", err);
            }
        }
        return JSON.parse(JSON.stringify(value));
    }

    function ensureStyles() {
        if (document.querySelector("style[data-kanban-style='true']")) {
            return;
        }

        const css = `
.kanban-wrapper {
    --kanban-bg: #f8fafc;
    --kanban-border: rgba(15, 23, 42, 0.08);
    --kanban-header-bg: #ffffff;
    --kanban-text: #0f172a;
    --kanban-muted: #64748b;
    --kanban-column-bg: #ffffff;
    --kanban-column-border: rgba(15, 23, 42, 0.08);
    --kanban-card-bg: #ffffff;
    --kanban-card-border: rgba(15, 23, 42, 0.08);
    --kanban-card-shadow: 0 8px 16px -8px rgba(15, 23, 42, 0.15);
    --kanban-tag-bg: rgba(79, 70, 229, 0.12);
    --kanban-tag-fg: #4338ca;
    --kanban-badge-bg: rgba(14, 165, 233, 0.12);
    --kanban-badge-fg: #0369a1;
    --kanban-add-bg: #0f172a;
    --kanban-add-bg-hover: #1e293b;
    --kanban-add-fg: #f8fafc;
    --kanban-scroll-track: rgba(148, 163, 184, 0.25);
    --kanban-scroll-thumb: rgba(100, 116, 139, 0.6);
    --kanban-progress-bg: rgba(148, 163, 184, 0.3);
    --kanban-progress-fg: #14b8a6;
    --kanban-lane-label-width: 220px;
    background: var(--kanban-bg);
    color: var(--kanban-text);
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    font-family: var(--dhx-font-family, "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif);
}

.kanban-wrapper[data-kanban-theme="dark"] {
    --kanban-bg: #111827;
    --kanban-border: rgba(148, 163, 184, 0.12);
    --kanban-header-bg: #0f172a;
    --kanban-text: #e2e8f0;
    --kanban-muted: #94a3b8;
    --kanban-column-bg: #1e293b;
    --kanban-column-border: rgba(15, 23, 42, 0.6);
    --kanban-card-bg: #1f2937;
    --kanban-card-border: rgba(148, 163, 184, 0.08);
    --kanban-card-shadow: 0 16px 24px -12px rgba(15, 23, 42, 0.45);
    --kanban-tag-bg: rgba(129, 140, 248, 0.18);
    --kanban-tag-fg: #c7d2fe;
    --kanban-badge-bg: rgba(56, 189, 248, 0.18);
    --kanban-badge-fg: #bae6fd;
    --kanban-add-bg: rgba(148, 163, 184, 0.18);
    --kanban-add-bg-hover: rgba(148, 163, 184, 0.28);
    --kanban-add-fg: #e2e8f0;
    --kanban-scroll-track: rgba(100, 116, 139, 0.12);
    --kanban-scroll-thumb: rgba(148, 163, 184, 0.45);
    --kanban-progress-bg: rgba(148, 163, 184, 0.18);
    --kanban-progress-fg: #34d399;
}

.kanban-wrapper * {
    box-sizing: border-box;
}

.kanban-header {
    padding: 18px 24px;
    border-bottom: 1px solid var(--kanban-border);
    background: var(--kanban-header-bg);
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.kanban-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--kanban-text);
    margin: 0;
}

.kanban-description {
    font-size: 14px;
    color: var(--kanban-muted);
    margin: 0;
}

.kanban-scroll {
    flex: 1;
    overflow: auto;
    padding: 24px;
}

.kanban-scroll::-webkit-scrollbar {
    height: 12px;
    width: 12px;
}

.kanban-scroll::-webkit-scrollbar-track {
    background: var(--kanban-scroll-track);
    border-radius: 999px;
}

.kanban-scroll::-webkit-scrollbar-thumb {
    background: var(--kanban-scroll-thumb);
    border-radius: 999px;
}

.kanban-board {
    display: flex;
    flex-direction: column;
    gap: 16px;
    min-height: 100%;
}

.kanban-board-header {
    display: flex;
    gap: 20px;
    align-items: flex-end;
    padding: 0 0 8px;
}

.kanban-board-header-columns {
    display: flex;
    gap: 20px;
    flex: 1;
}

.kanban-board-lanes {
    display: flex;
    flex-direction: column;
    gap: 24px;
    min-height: 100%;
}

.kanban-lane {
    display: flex;
    gap: 20px;
    align-items: stretch;
}

.kanban-lane-label {
    width: var(--kanban-lane-label-width);
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 6px 0 0;
}

.kanban-lane-label.is-empty {
    visibility: hidden;
}

.kanban-lane-label-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--kanban-text);
}

.kanban-lane-label-caption {
    font-size: 12px;
    color: var(--kanban-muted);
}

.kanban-board-header .kanban-lane-label {
    visibility: hidden;
}

.kanban-columns {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    flex: 1;
}

.kanban-column {
    width: 280px;
    min-width: 260px;
    background: var(--kanban-column-bg);
    border: 1px solid var(--kanban-column-border);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 20px 40px -24px rgba(15, 23, 42, 0.4);
    transition: transform 120ms ease;
}

.kanban-column.is-collapsed .kanban-column-body,
.kanban-column.is-collapsed .kanban-column-footer {
    display: none;
}

.kanban-column.drag-over {
    border-color: rgba(59, 130, 246, 0.6);
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
}

.kanban-column-header {
    padding: 14px 16px;
    border-bottom: 1px solid var(--kanban-column-border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.kanban-column-headeronly {
    width: 280px;
    min-width: 260px;
}

.kanban-column-headeronly .kanban-column-header {
    border: none;
    padding: 0;
}

.kanban-column-header-main {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
}

.kanban-column-title {
    font-weight: 600;
    font-size: 15px;
    color: var(--kanban-text);
    margin: 0;
}

.kanban-column-meta {
    font-size: 12px;
    color: var(--kanban-muted);
}

.kanban-column-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--kanban-badge-bg);
    color: var(--kanban-badge-fg);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
    white-space: nowrap;
}

.kanban-column-body {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    min-height: 80px;
}

.kanban-empty-column {
    font-size: 13px;
    color: var(--kanban-muted);
    text-align: center;
    border: 1px dashed var(--kanban-border);
    border-radius: 12px;
    padding: 18px 12px;
}

.kanban-column-footer {
    padding: 12px 16px 16px;
    border-top: 1px solid var(--kanban-column-border);
}

.kanban-column-add {
    appearance: none;
    border: none;
    border-radius: 10px;
    background: var(--kanban-add-bg);
    color: var(--kanban-add-fg);
    font-weight: 600;
    font-size: 13px;
    padding: 10px 12px;
    width: 100%;
    cursor: pointer;
    transition: background 120ms ease, transform 120ms ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.kanban-column-add:hover {
    background: var(--kanban-add-bg-hover);
    transform: translateY(-1px);
}

.kanban-card {
    background: var(--kanban-card-bg);
    border-radius: 12px;
    padding: 14px 16px;
    box-shadow: var(--kanban-card-shadow);
    border: 1px solid var(--kanban-card-border);
    cursor: grab;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: transform 120ms ease, box-shadow 120ms ease;
}

.kanban-card:active {
    cursor: grabbing;
}

.kanban-card.is-dragging {
    opacity: 0.55;
    box-shadow: 0 24px 40px -24px rgba(59, 130, 246, 0.45);
}

.kanban-card-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--kanban-text);
    margin: 0;
}

.kanban-card-description {
    font-size: 13px;
    color: var(--kanban-muted);
    margin: 0;
    line-height: 1.5;
}

.kanban-card-meta {
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
    font-size: 12px;
    color: var(--kanban-muted);
}

.kanban-card-assignee {
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.kanban-card-avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
}

.kanban-card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.kanban-tag {
    background: var(--kanban-tag-bg);
    color: var(--kanban-tag-fg);
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.kanban-progress {
    height: 6px;
    border-radius: 999px;
    background: var(--kanban-progress-bg);
    overflow: hidden;
}

.kanban-progress-bar {
    height: 100%;
    background: var(--kanban-progress-fg);
    transition: width 160ms ease;
}

.kanban-board-empty {
    border: 1px dashed var(--kanban-border);
    border-radius: 18px;
    padding: 32px;
    text-align: center;
    font-size: 14px;
    color: var(--kanban-muted);
}

.kanban-add-column {
    appearance: none;
    border: 1px dashed var(--kanban-border);
    background: transparent;
    border-radius: 14px;
    padding: 16px;
    min-width: 260px;
    height: 72px;
    color: var(--kanban-muted);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: border 120ms ease, color 120ms ease, background 120ms ease;
}

.kanban-add-column:hover {
    border-color: rgba(59, 130, 246, 0.6);
    color: rgba(59, 130, 246, 0.9);
    background: rgba(59, 130, 246, 0.08);
}
        `;

        const style = document.createElement("style");
        style.type = "text/css";
        style.setAttribute("data-kanban-style", "true");
        style.appendChild(document.createTextNode(css));
        document.head.appendChild(style);
    }

    function resolveDomTarget(target) {
        if (!target) {
            return null;
        }

        if (typeof target === "string") {
            return document.querySelector(target);
        }

        if (target && (target.nodeType === 1 || target === document)) {
            return target;
        }

        return null;
    }

    class KanbanBoard {
        constructor(target, options = {}) {
            ensureStyles();
            this._host = this._initializeHost(target);
            if (!this._host) {
                throw new Error("Unable to resolve host for KanbanBoard.");
            }

            this._options = Object.assign({}, DEFAULT_OPTIONS);
            this._cards = new Map();
            this._columns = [];
            this._lanes = [];
            this._events = new Map();
            this._suspendRender = false;
            this._dragState = null;
            this._theme = "auto";

            this._buildShell();
            this.load(options);
        }

        // ------------------------------------------------------------------
        // Static API (templates)
        // ------------------------------------------------------------------

        static registerCardTemplate(name, factory) {
            if (!name || typeof name !== "string") {
                throw new Error("Card template name must be a non-empty string.");
            }
            let ref = factory;
            if (typeof factory === "string") {
                ref = (0, eval)(factory); // eslint-disable-line no-eval
            }
            if (typeof ref !== "function") {
                throw new Error("Card template factory must be a function.");
            }
            CARD_TEMPLATES.set(name, ref);
        }

        static registerColumnTemplate(name, factory) {
            if (!name || typeof name !== "string") {
                throw new Error("Column template name must be a non-empty string.");
            }
            let ref = factory;
            if (typeof factory === "string") {
                ref = (0, eval)(factory); // eslint-disable-line no-eval
            }
            if (typeof ref !== "function") {
                throw new Error("Column template factory must be a function.");
            }
            COLUMN_TEMPLATES.set(name, ref);
        }

        static getCardTemplate(name) {
            return CARD_TEMPLATES.get(name);
        }

        static getColumnTemplate(name) {
            return COLUMN_TEMPLATES.get(name);
        }

        // ------------------------------------------------------------------
        // Event emitter helpers
        // ------------------------------------------------------------------

        on(eventName, handler) {
            if (!eventName || typeof handler !== "function") {
                return;
            }
            const bucket = this._events.get(eventName) || [];
            bucket.push(handler);
            this._events.set(eventName, bucket);
        }

        off(eventName, handler) {
            const bucket = this._events.get(eventName);
            if (!bucket) {
                return;
            }
            if (!handler) {
                this._events.delete(eventName);
                return;
            }
            const next = bucket.filter((fn) => fn !== handler);
            if (next.length) {
                this._events.set(eventName, next);
            } else {
                this._events.delete(eventName);
            }
        }

        _emit(eventName, payload) {
            const bucket = this._events.get(eventName);
            if (!bucket || !bucket.length) {
                return;
            }
            const data = payload === undefined ? undefined : deepClone(payload);
            bucket.forEach((handler) => {
                try {
                    handler(data);
                } catch (err) {
                    console.error("[KanbanBoard] event handler failed", err);
                }
            });
        }

        // ------------------------------------------------------------------
        // Public API: data + configuration
        // ------------------------------------------------------------------

        load(options = {}) {
            const incoming = options || {};
            const {
                columns,
                cards,
                lanes,
                theme,
                ...rest
            } = incoming;

            this._applyOptions(rest);

            if (theme) {
                this.setTheme(theme);
            }

            this._withSuspendedRender(() => {
                if (Array.isArray(columns)) {
                    this._applyColumns(columns);
                }
                if (Array.isArray(cards)) {
                    this._applyCards(cards);
                }
                if (Array.isArray(lanes) || lanes === null) {
                    this._applyLanes(lanes);
                }
            });

            this._render();
        }

        setColumns(columns) {
            this._applyColumns(columns);
            this._render();
        }

        setCards(cards) {
            this._applyCards(cards);
            this._render();
        }

        setLanes(lanes) {
            this._applyLanes(lanes);
            this._render();
        }

        addCard(card, index) {
            const normalized = this._normalizeCard(card);
            const column = this._getColumn(normalized.status);
            if (!column) {
                throw new Error(`Unknown column: ${normalized.status}`);
            }
            this._cards.set(normalized.id, normalized);

            const targetIndex = typeof index === "number" && index >= 0
                ? Math.min(index, column.cards.length)
                : column.cards.length;
            column.cards.splice(targetIndex, 0, normalized.id);

            this._render();
            this._emit("cardMove", {
                action: "add",
                card: normalized,
                toColumn: column.id,
                toLane: normalized.lane || null,
            });
            return normalized.id;
        }

        updateCard(cardId, updates) {
            const existing = this._cards.get(cardId);
            if (!existing) {
                return;
            }

            const clone = Object.assign({}, existing, updates || {});
            const hasStatus = updates && Object.prototype.hasOwnProperty.call(updates, "status");
            const hasLane = updates && Object.prototype.hasOwnProperty.call(updates, "lane");
            const currentColumn = this._getColumn(existing.status);
            let currentIndex = null;
            if (currentColumn) {
                const idx = currentColumn.cards.indexOf(cardId);
                if (idx >= 0) {
                    currentIndex = idx;
                }
            }

            if (hasStatus && updates.status !== existing.status) {
                const moveOptions = { column: updates.status };
                if (hasLane) {
                    moveOptions.lane = updates.lane;
                }
                this.moveCard(cardId, moveOptions);
                return;
            }

            if (hasLane && updates.lane !== existing.lane) {
                this.moveCard(cardId, {
                    column: existing.status,
                    lane: updates.lane,
                    index: currentIndex !== null ? currentIndex : undefined,
                });
                return;
            }

            this._cards.set(cardId, clone);
            this._render();
        }

        removeCard(cardId) {
            const existing = this._cards.get(cardId);
            if (!existing) {
                return;
            }

            this._cards.delete(cardId);
            this._columns.forEach((column) => {
                column.cards = column.cards.filter((id) => id !== cardId);
            });

            this._render();
            this._emit("cardMove", {
                action: "remove",
                card: existing,
                fromColumn: existing.status,
                fromLane: existing.lane || null,
            });
        }

        moveCard(cardId, options = {}) {
            const card = this._cards.get(cardId);
            if (!card) {
                return;
            }

            const fromColumnId = card.status;
            const fromLaneId = card.lane || null;

            const targetColumnId = options.column || fromColumnId;
            const targetLaneId = options.hasOwnProperty("lane")
                ? options.lane
                : fromLaneId;
            const targetColumn = this._getColumn(targetColumnId);
            if (!targetColumn) {
                console.warn("[KanbanBoard] moveCard: unknown target column", targetColumnId);
                return;
            }

            this._columns.forEach((column) => {
                const idx = column.cards.indexOf(cardId);
                if (idx >= 0) {
                    column.cards.splice(idx, 1);
                }
            });

            const insertIndex = typeof options.index === "number" && options.index >= 0
                ? Math.min(options.index, targetColumn.cards.length)
                : targetColumn.cards.length;
            targetColumn.cards.splice(insertIndex, 0, cardId);

            card.status = targetColumnId;
            card.lane = targetLaneId || null;
            this._cards.set(cardId, card);

            this._render();

            this._emit("cardMove", {
                action: "move",
                card: card,
                fromColumn: fromColumnId,
                toColumn: targetColumnId,
                fromLane: fromLaneId,
                toLane: card.lane || null,
                index: insertIndex,
            });
        }

        addColumn(column, index) {
            const normalized = this._normalizeColumn(column);
            const targetIndex = typeof index === "number" && index >= 0
                ? Math.min(index, this._columns.length)
                : this._columns.length;
            this._columns.splice(targetIndex, 0, normalized);
            this._render();

            this._emit("columnCreate", {
                columnId: normalized.id,
                title: normalized.title,
                index: targetIndex,
            });
            return normalized.id;
        }

        updateColumn(columnId, updates) {
            const column = this._getColumn(columnId);
            if (!column) {
                return;
            }
            Object.assign(column, updates || {});
            this._render();
        }

        removeColumn(columnId) {
            const index = this._columns.findIndex((col) => col.id === columnId);
            if (index === -1) {
                return;
            }
            const [removed] = this._columns.splice(index, 1);
            this._render();
            this._emit("columnToggle", {
                action: "remove",
                columnId: removed.id,
                title: removed.title,
            });
        }

        setTheme(theme) {
            this._theme = theme || "auto";
            const resolved = this._resolveTheme(this._theme);
            this._root.setAttribute("data-kanban-theme", resolved);
        }

        getState() {
            const columns = this._columns.map((column) => ({
                id: column.id,
                title: column.title,
                limit: column.limit,
                allowDrop: column.allowDrop,
                allowAdd: column.allowAdd,
                collapsed: column.collapsed,
                badge: column.badge,
                order: column.order,
                emptyText: column.emptyText,
                addButtonText: column.addButtonText,
                template: column.template,
                cards: column.cards.slice(),
            }));

            const cards = [];
            this._cards.forEach((card) => {
                cards.push(Object.assign({}, card));
            });

            const lanes = this._lanes.map((lane) => Object.assign({}, lane));

            return {
                columns,
                cards,
                lanes,
                options: Object.assign({}, this._options, { theme: this._theme }),
            };
        }

        destroy() {
            this._events.clear();
            this._cards.clear();
            this._columns = [];
            this._lanes = [];
            if (this._root && this._root.parentNode) {
                this._root.parentNode.removeChild(this._root);
            }
        }

        // ------------------------------------------------------------------
        // Internal helpers
        // ------------------------------------------------------------------

        _initializeHost(target) {
            if (!target) {
                return null;
            }

            if (target && typeof target.attach === "function") {
                const mount = document.createElement("div");
                mount.style.width = "100%";
                mount.style.height = "100%";
                target.attach(mount);
                return mount;
            }

            if (target && typeof target.attachHTML === "function") {
                const mountId = createUniqueId("kanban-mount");
                target.attachHTML(`<div id="${mountId}" style="width:100%;height:100%"></div>`);
                return document.getElementById(mountId);
            }

            return resolveDomTarget(target);
        }

        _buildShell() {
            this._root = document.createElement("div");
            this._root.className = "kanban-wrapper";

            this._header = document.createElement("div");
            this._header.className = "kanban-header";
            this._titleEl = document.createElement("h2");
            this._titleEl.className = "kanban-title";
            this._descriptionEl = document.createElement("p");
            this._descriptionEl.className = "kanban-description";
            this._header.appendChild(this._titleEl);
            this._header.appendChild(this._descriptionEl);

        this._scroll = document.createElement("div");
        this._scroll.className = "kanban-scroll";

        this._board = document.createElement("div");
        this._board.className = "kanban-board";
        this._boardHeader = document.createElement("div");
        this._boardHeader.className = "kanban-board-header";
        this._boardHeaderLabel = document.createElement("div");
        this._boardHeaderLabel.className = "kanban-lane-label";
        this._boardHeaderColumns = document.createElement("div");
        this._boardHeaderColumns.className = "kanban-board-header-columns";
        this._boardHeader.appendChild(this._boardHeaderLabel);
        this._boardHeader.appendChild(this._boardHeaderColumns);
        this._boardLanes = document.createElement("div");
        this._boardLanes.className = "kanban-board-lanes";
        this._board.appendChild(this._boardHeader);
        this._board.appendChild(this._boardLanes);

        this._empty = document.createElement("div");
        this._empty.className = "kanban-board-empty";
        this._empty.style.display = "none";

            this._scroll.appendChild(this._empty);
            this._scroll.appendChild(this._board);

            this._root.appendChild(this._header);
            this._root.appendChild(this._scroll);

            this._host.appendChild(this._root);
            this._updateHeader();
            this.setTheme(this._options.theme);
        }

        _withSuspendedRender(callback) {
            const previous = this._suspendRender;
            this._suspendRender = true;
            try {
                callback();
            } finally {
                this._suspendRender = previous;
            }
        }

        _render() {
            if (this._suspendRender) {
                return;
            }

            this._updateHeader();

            this._boardHeaderColumns.innerHTML = "";
            this._boardLanes.innerHTML = "";
            const hasColumns = Boolean(this._columns.length);
            const hasCards = this._columns.some((column) => column.cards.length);

            if (!hasColumns) {
                this._boardHeader.style.display = "none";
                this._empty.textContent = this._options.emptyBoardText || "No columns configured yet.";
                this._empty.style.display = "block";
                return;
            }

            this._boardHeader.style.display = "";
            this._empty.style.display = hasCards ? "none" : "block";
            if (!hasCards) {
                this._empty.textContent = this._options.emptyBoardText || "Drop cards here to get started.";
            }

            this._columns.forEach((column) => {
                const headerCell = this._renderColumnHeaderCell(column);
                this._boardHeaderColumns.appendChild(headerCell);
            });

            const lanes = this._getRenderableLanes();
            lanes.forEach((lane, index) => {
                const laneEl = this._renderLane(lane, index);
                this._boardLanes.appendChild(laneEl);
            });

            if (this._options.addColumnText) {
                const button = document.createElement("button");
                button.className = "kanban-add-column";
                button.type = "button";
                button.textContent = this._options.addColumnText;
                button.addEventListener("click", () => {
                    this._emit("columnCreate", {
                        action: "request",
                        boardId: this._options.boardId || null,
                    });
                });
                if (lanes.length) {
                    const lastLane = this._boardLanes.lastElementChild;
                    if (lastLane && lastLane.classList.contains("kanban-lane")) {
                        const columnsContainer = lastLane.querySelector(".kanban-columns");
                        if (columnsContainer) {
                            columnsContainer.appendChild(button);
                            return;
                        }
                    }
                }
                this._board.appendChild(button);
            }
        }

        _renderLane(lane, laneIndex) {
            const laneEl = document.createElement("div");
            laneEl.className = "kanban-lane";
            laneEl.dataset.laneId = lane.id || "";
            laneEl.dataset.laneIndex = String(typeof laneIndex === "number" ? laneIndex : 0);

            const labelWrapper = document.createElement("div");
            labelWrapper.className = "kanban-lane-label";
            if (!lane.title) {
                labelWrapper.classList.add("is-empty");
            }
            if (lane.title) {
                const labelTitle = document.createElement("div");
                labelTitle.className = "kanban-lane-label-title";
                labelTitle.textContent = lane.title;
                labelWrapper.appendChild(labelTitle);
            }
            if (lane.description) {
                const labelCaption = document.createElement("div");
                labelCaption.className = "kanban-lane-label-caption";
                labelCaption.textContent = lane.description;
                labelWrapper.appendChild(labelCaption);
            }
            laneEl.appendChild(labelWrapper);

            const columnsWrap = document.createElement("div");
            columnsWrap.className = "kanban-columns";

            this._columns.forEach((column) => {
                const columnEl = this._renderColumn(column, lane, laneIndex);
                columnsWrap.appendChild(columnEl);
            });

            laneEl.appendChild(columnsWrap);
            return laneEl;
        }

        _renderColumnHeaderCell(column) {
            const container = document.createElement("div");
            container.className = "kanban-column-headeronly";
            if (column.collapsed) {
                container.classList.add("is-collapsed");
            }

            const header = document.createElement("div");
            header.className = "kanban-column-header";
            header.addEventListener("click", (event) => {
                if (event.target && event.target.closest("button")) {
                    return;
                }
                if (column.toggleOnHeader) {
                    column.collapsed = !column.collapsed;
                    this._render();
                    this._emit("columnToggle", {
                        columnId: column.id,
                        collapsed: column.collapsed,
                    });
                }
            });

            const headerContent = this._renderColumnHeaderContent(column, null);
            if (headerContent instanceof Node) {
                header.appendChild(headerContent);
            } else {
                header.innerHTML = headerContent;
            }

            container.appendChild(header);
            return container;
        }

        _renderColumn(column, lane, laneIndex) {
            const columnEl = document.createElement("div");
            columnEl.className = "kanban-column";
            columnEl.dataset.columnId = column.id;
            columnEl.dataset.laneIndex = String(typeof laneIndex === "number" ? laneIndex : 0);
            if (column.collapsed) {
                columnEl.classList.add("is-collapsed");
            }

            const body = document.createElement("div");
            body.className = "kanban-column-body";
            body.addEventListener("dragenter", (event) => this._handleDragEnter(event, columnEl, column));
            body.addEventListener("dragover", (event) => this._handleDragOver(event, columnEl, column, lane));
            body.addEventListener("dragleave", (event) => this._handleDragLeave(event, columnEl));
            body.addEventListener("drop", (event) => this._handleDrop(event, columnEl, column, lane));

            const cards = this._getCardsForColumn(column, lane);
            if (!cards.length) {
                const empty = document.createElement("div");
                empty.className = "kanban-empty-column";
                empty.textContent = column.emptyText || "Nothing here yet";
                body.appendChild(empty);
            } else {
                cards.forEach((card) => {
                    const cardEl = this._renderCard(card, column, lane);
                    body.appendChild(cardEl);
                });
            }

            columnEl.appendChild(body);

            if (laneIndex === 0 && column.allowAdd !== false && this._options.addCardText) {
                const footer = document.createElement("div");
                footer.className = "kanban-column-footer";
                const addButton = document.createElement("button");
                addButton.type = "button";
                addButton.className = "kanban-column-add";
                addButton.textContent = column.addButtonText || this._options.addCardText;
                addButton.addEventListener("click", () => {
                    this._emit("cardCreate", {
                        columnId: column.id,
                        laneId: lane.id || null,
                        columnTitle: column.title,
                    });
                });
                footer.appendChild(addButton);
                columnEl.appendChild(footer);
            }

            return columnEl;
        }

        _renderColumnHeaderContent(column, lane) {
            const template = this._resolveColumnTemplate(column);
            const context = {
                column,
                lane,
                board: this,
            };

            if (typeof template === "function") {
                return template(context);
            }

            const wrapper = document.createElement("div");
            wrapper.className = "kanban-column-header-main";

            const title = document.createElement("span");
            title.className = "kanban-column-title";
            title.textContent = column.title || "Column";
            wrapper.appendChild(title);

            if (column.badge || column.limit) {
                const meta = document.createElement("span");
                meta.className = "kanban-column-meta";
                const parts = [];
                if (column.badge) {
                    parts.push(column.badge);
                }
                if (column.limit) {
                    const count = this._countColumnCards(column, lane);
                    parts.push(`${count}/${column.limit}`);
                }
                meta.textContent = parts.join(" · ");
                wrapper.appendChild(meta);
            }

            if (column.badge && !column.limit) {
                const badge = document.createElement("span");
                badge.className = "kanban-column-badge";
                badge.textContent = column.badge;
                const container = document.createElement("div");
                container.className = "kanban-column-header-main";
                container.appendChild(wrapper);
                container.appendChild(badge);
                return container;
            }

            return wrapper;
        }

        _renderCard(card, column, lane) {
            const cardEl = document.createElement("div");
            cardEl.className = "kanban-card";
            cardEl.dataset.cardId = card.id;

            const canDrag = this._options.allowCardDrag && column.allowDrop !== false;
            cardEl.setAttribute("draggable", String(canDrag));

            cardEl.addEventListener("click", () => {
                this._emit("cardClick", {
                    card,
                    columnId: column.id,
                    laneId: lane.id || null,
                });
            });

            cardEl.addEventListener("dragstart", (event) => this._handleDragStart(event, cardEl, card));
            cardEl.addEventListener("dragend", () => this._handleDragEnd(cardEl));

            const template = this._resolveCardTemplate(card);
            const context = {
                card,
                column,
                lane,
                board: this,
            };

            if (typeof template === "function") {
                const result = template(context);
                if (result instanceof Node) {
                    cardEl.appendChild(result);
                } else if (typeof result === "string") {
                    cardEl.innerHTML = result;
                }
            } else {
                const title = document.createElement("h3");
                title.className = "kanban-card-title";
                title.textContent = card.title || "Untitled task";
                cardEl.appendChild(title);

                if (card.description) {
                    const desc = document.createElement("p");
                    desc.className = "kanban-card-description";
                    desc.textContent = card.description;
                    cardEl.appendChild(desc);
                }

                if (card.tags && card.tags.length) {
                    const tags = document.createElement("div");
                    tags.className = "kanban-card-tags";
                    card.tags.forEach((tag) => {
                        const badge = document.createElement("span");
                        badge.className = "kanban-tag";
                        badge.textContent = tag;
                        tags.appendChild(badge);
                    });
                    cardEl.appendChild(tags);
                }

                const metaItems = [];
                if (card.assignee) {
                    metaItems.push({ type: "assignee" });
                }
                if (card.priority) {
                    metaItems.push({ type: "text", value: card.priority });
                }
                if (card.due) {
                    metaItems.push({ type: "text", value: card.due });
                }

                if (metaItems.length) {
                    const meta = document.createElement("div");
                    meta.className = "kanban-card-meta";
                    metaItems.forEach((item) => {
                        if (item.type === "assignee") {
                            const assignee = document.createElement("span");
                            assignee.className = "kanban-card-assignee";
                            if (card.avatar) {
                                const img = document.createElement("img");
                                img.src = card.avatar;
                                img.alt = card.assignee;
                                img.className = "kanban-card-avatar";
                                assignee.appendChild(img);
                            }
                            const name = document.createElement("span");
                            name.textContent = card.assignee;
                            assignee.appendChild(name);
                            meta.appendChild(assignee);
                        } else {
                            const text = document.createElement("span");
                            text.textContent = item.value;
                            meta.appendChild(text);
                        }
                    });
                    cardEl.appendChild(meta);
                }

                if (typeof card.progress === "number") {
                    const progress = document.createElement("div");
                    progress.className = "kanban-progress";
                    const bar = document.createElement("div");
                    bar.className = "kanban-progress-bar";
                    const clamped = Math.max(0, Math.min(100, card.progress));
                    bar.style.width = `${clamped}%`;
                    progress.appendChild(bar);
                    cardEl.appendChild(progress);
                }
            }

            return cardEl;
        }

        _handleDragStart(event, cardEl, card) {
            if (!this._options.allowCardDrag) {
                event.preventDefault();
                return;
            }
            cardEl.classList.add("is-dragging");
            this._dragState = {
                cardId: card.id,
                columnId: card.status,
                laneId: card.lane || null,
            };
            if (event.dataTransfer) {
                event.dataTransfer.effectAllowed = "move";
                event.dataTransfer.setData("text/plain", card.id);
            }
        }

        _handleDragEnd(cardEl) {
            cardEl.classList.remove("is-dragging");
            this._dragState = null;
            this._clearDragHighlights();
        }

        _handleDragEnter(event, columnEl, column) {
            if (!this._dragState || column.allowDrop === false) {
                return;
            }
            event.preventDefault();
            columnEl.classList.add("drag-over");
        }

        _handleDragOver(event, columnEl, column, lane) {
            if (!this._dragState || column.allowDrop === false) {
                return;
            }
            event.preventDefault();
            event.dataTransfer.dropEffect = "move";
        }

        _handleDragLeave(event, columnEl) {
            const related = event.relatedTarget;
            if (columnEl.contains(related)) {
                return;
            }
            columnEl.classList.remove("drag-over");
        }

        _handleDrop(event, columnEl, column, lane) {
            event.preventDefault();
            columnEl.classList.remove("drag-over");
            if (!this._dragState || column.allowDrop === false) {
                return;
            }
            const cardId = this._dragState.cardId;
            const laneId = lane.id || null;
            this.moveCard(cardId, {
                column: column.id,
                lane: laneId,
            });
            this._dragState = null;
            this._clearDragHighlights();
        }

        _clearDragHighlights() {
            this._board.querySelectorAll(".kanban-column.drag-over").forEach((el) => {
                el.classList.remove("drag-over");
            });
        }

        _applyOptions(rest) {
            const next = Object.assign({}, rest);
            const dataKeys = ["columns", "cards", "lanes"];
            dataKeys.forEach((key) => delete next[key]);

            if (next.enableLanes !== undefined) {
                this._options.enableLanes = Boolean(next.enableLanes);
            }
            if (next.laneField) {
                this._options.laneField = String(next.laneField);
            }
            if (next.allowCardDrag !== undefined) {
                this._options.allowCardDrag = Boolean(next.allowCardDrag);
            }
            if (next.allowColumnReorder !== undefined) {
                this._options.allowColumnReorder = Boolean(next.allowColumnReorder);
            }
            if (next.addColumnText !== undefined) {
                this._options.addColumnText = next.addColumnText;
            }
            if (next.addCardText !== undefined) {
                this._options.addCardText = next.addCardText;
            }
            if (next.emptyBoardText !== undefined) {
                this._options.emptyBoardText = next.emptyBoardText;
            }
            if (next.cardTemplate !== undefined) {
                this._options.cardTemplate = next.cardTemplate;
            }
            if (next.columnTemplate !== undefined) {
                this._options.columnTemplate = next.columnTemplate;
            }
            if (next.title !== undefined) {
                this._options.title = next.title;
            }
            if (next.description !== undefined) {
                this._options.description = next.description;
            }
            if (next.boardId !== undefined) {
                this._options.boardId = next.boardId;
            }
        }

        _applyColumns(columns) {
            const normalized = (columns || []).map((column) => this._normalizeColumn(column));
            this._columns = normalized.sort((a, b) => {
                const orderA = typeof a.order === "number" ? a.order : Number.MAX_SAFE_INTEGER;
                const orderB = typeof b.order === "number" ? b.order : Number.MAX_SAFE_INTEGER;
                return orderA - orderB;
            });
            this._reconcileCards();
        }

        _applyCards(cards) {
            this._cards.clear();
            (cards || []).forEach((card) => {
                const normalized = this._normalizeCard(card);
                this._cards.set(normalized.id, normalized);
            });
            this._columns.forEach((column) => { column.cards = []; });
            this._cards.forEach((card) => {
                const column = this._getColumn(card.status);
                if (column) {
                    column.cards.push(card.id);
                }
            });
        }

        _applyLanes(lanes) {
            if (!Array.isArray(lanes)) {
                this._lanes = [];
                return;
            }
            this._lanes = lanes.map((lane) => Object.assign({}, lane));
            this._lanes.sort((a, b) => {
                const orderA = typeof a.order === "number" ? a.order : Number.MAX_SAFE_INTEGER;
                const orderB = typeof b.order === "number" ? b.order : Number.MAX_SAFE_INTEGER;
                return orderA - orderB;
            });
        }

        _reconcileCards() {
            const seen = new Set();
            this._columns.forEach((column) => {
                const collected = [];
                (column.cards || []).forEach((card) => {
                    const cardId = typeof card === "string" ? card : card.id;
                    if (!cardId) {
                        return;
                    }
                    const normalized = this._normalizeCard(
                        typeof card === "string" ? { id: card, status: column.id } : card,
                        column.id,
                    );
                    this._cards.set(normalized.id, Object.assign({}, this._cards.get(normalized.id) || {}, normalized));
                    collected.push(normalized.id);
                    seen.add(normalized.id);
                });
                column.cards = collected;
            });
            this._cards.forEach((_, cardId) => {
                if (!seen.has(cardId)) {
                    const card = this._cards.get(cardId);
                    const column = this._getColumn(card.status);
                    if (column) {
                        column.cards.push(cardId);
                    }
                }
            });
        }

        _normalizeColumn(column) {
            const raw = column || {};
            const id = raw.id ? String(raw.id) : createUniqueId("column");
            const normalized = {
                id,
                title: raw.title || "Column",
                limit: raw.limit != null ? Number(raw.limit) : null,
                allowDrop: raw.allowDrop !== false,
                allowAdd: raw.allowAdd !== false,
                collapsed: Boolean(raw.collapsed),
                badge: raw.badge || null,
                order: raw.order != null ? Number(raw.order) : null,
                emptyText: raw.emptyText || null,
                addButtonText: raw.addButtonText || null,
                template: raw.template || null,
                cards: Array.isArray(raw.cards) ? raw.cards.slice() : [],
                toggleOnHeader: raw.toggleOnHeader !== undefined ? Boolean(raw.toggleOnHeader) : true,
                meta: Object.assign({}, raw.meta || {}, raw.extra || {}),
            };
            return normalized;
        }

        _normalizeCard(card, fallbackColumnId) {
            const raw = card || {};
            const id = raw.id ? String(raw.id) : createUniqueId("card");
            const status = raw.status ? String(raw.status) : fallbackColumnId || this._columns[0]?.id || "backlog";
            const laneField = (this._options && this._options.laneField) ? this._options.laneField : "lane";
            let laneValue;
            if (Object.prototype.hasOwnProperty.call(raw, laneField)) {
                laneValue = raw[laneField];
            } else if (Object.prototype.hasOwnProperty.call(raw, "lane")) {
                laneValue = raw.lane;
            } else {
                laneValue = null;
            }
            const normalizedLane = laneValue === undefined ? null : laneValue;
            const normalized = {
                id,
                title: raw.title || "Untitled",
                status,
                description: raw.description || "",
                lane: normalizedLane,
                assignee: raw.assignee || null,
                avatar: raw.avatar || null,
                priority: raw.priority || null,
                due: raw.due || null,
                tags: Array.isArray(raw.tags) ? raw.tags.slice() : [],
                progress: typeof raw.progress === "number" ? raw.progress : null,
                meta: Object.assign({}, raw.meta || {}),
                template: raw.template || null,
                extra: Object.assign({}, raw.extra || {}),
            };
            if (laneField !== "lane") {
                normalized[laneField] = normalizedLane;
            }
            return normalized;
        }

        _getColumn(columnId) {
            return this._columns.find((column) => column.id === columnId);
        }

        _getRenderableLanes() {
            if (!this._options.enableLanes) {
                return [{ id: null, title: null }];
            }

            if (this._lanes.length) {
                return this._lanes;
            }

            const extracted = new Map();
            this._cards.forEach((card) => {
                const laneId = card[this._options.laneField] || card.lane || null;
                if (!laneId) {
                    return;
                }
                if (!extracted.has(laneId)) {
                    extracted.set(laneId, {
                        id: laneId,
                        title: laneId,
                    });
                }
            });

            if (!extracted.size) {
                return [{ id: null, title: null }];
            }

            return Array.from(extracted.values());
        }

        _getCardsForColumn(column, lane) {
            const laneId = this._options.enableLanes
                ? (lane && typeof lane === "object" ? (lane.id || null) : null)
                : null;
            const cards = [];
            column.cards.forEach((cardId) => {
                const card = this._cards.get(cardId);
                if (!card) {
                    return;
                }
                const currentLane = card[this._options.laneField] || card.lane || null;
                if (!this._options.enableLanes || laneId === null || currentLane === laneId) {
                    cards.push(card);
                }
            });
            return cards;
        }

        _countColumnCards(column, lane) {
            return this._getCardsForColumn(column, lane).length;
        }

        _resolveTheme(theme) {
            if (theme === "dark") {
                return "dark";
            }
            if (theme === "light") {
                return "light";
            }
            const docTheme = document.documentElement.getAttribute("data-dhx-theme")
                || document.documentElement.getAttribute("data-theme");
            if (docTheme) {
                return docTheme === "dark" ? "dark" : "light";
            }
            if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
                return "dark";
            }
            return "light";
        }

        _resolveCardTemplate(card) {
            if (card.template) {
                if (typeof card.template === "function") {
                    return card.template;
                }
                if (typeof card.template === "string" && CARD_TEMPLATES.has(card.template)) {
                    return CARD_TEMPLATES.get(card.template);
                }
            }

            if (this._options.cardTemplate) {
                if (typeof this._options.cardTemplate === "function") {
                    return this._options.cardTemplate;
                }
                if (typeof this._options.cardTemplate === "string") {
                    return CARD_TEMPLATES.get(this._options.cardTemplate);
                }
            }

            return null;
        }

        _resolveColumnTemplate(column) {
            if (column.template) {
                if (typeof column.template === "function") {
                    return column.template;
                }
                if (typeof column.template === "string" && COLUMN_TEMPLATES.has(column.template)) {
                    return COLUMN_TEMPLATES.get(column.template);
                }
            }

            if (this._options.columnTemplate) {
                if (typeof this._options.columnTemplate === "function") {
                    return this._options.columnTemplate;
                }
                if (typeof this._options.columnTemplate === "string") {
                    return COLUMN_TEMPLATES.get(this._options.columnTemplate);
                }
            }

            return null;
        }

        _updateHeader() {
            const titleVisible = Boolean(this._options.title);
            const descVisible = Boolean(this._options.description);

            if (titleVisible) {
                this._titleEl.textContent = this._options.title;
                this._titleEl.style.display = "";
            } else {
                this._titleEl.style.display = "none";
            }

            if (descVisible) {
                this._descriptionEl.textContent = this._options.description;
                this._descriptionEl.style.display = "";
            } else {
                this._descriptionEl.style.display = "none";
            }

            this._header.style.display = (titleVisible || descVisible) ? "" : "none";
        }
    }

    globalThis.customdhx = globalThis.customdhx || {};
    globalThis.customdhx.KanbanBoard = KanbanBoard;
})();
