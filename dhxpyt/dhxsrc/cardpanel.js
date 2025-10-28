(function () {
    class CardPanel {
        constructor(rootSelector, options = {}) {
            this.root = (typeof rootSelector === "string") ? document.querySelector(rootSelector) : rootSelector;
            if (!this.root) {
                throw new Error("Root element not found for CardPanel");
            }

            this.options = Object.assign({
                title: "Data Sources",
                description: "Manage and connect to various data sources with intelligent profiling and lineage tracking.",
                searchable: true,
                autoFilter: true,
                cards: []
            }, options);

            this._events = {};
            this.cards = [];
            this._injectStyles();
            this._renderBase();

            if (Array.isArray(this.options.cards) && this.options.cards.length) {
                this.load(this.options.cards);
            }
        }

        on(name, handler) {
            if (typeof handler !== "function") return;
            this._events[name] = this._events[name] || [];
            this._events[name].push(handler);
        }

        off(name, handler) {
            if (!this._events[name]) return;
            this._events[name] = this._events[name].filter(h => h !== handler);
        }

        emit(name, ...args) {
            (this._events[name] || []).forEach(handler => {
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
:root {
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
    --surface-border: #233044;
    --card-border: #1e293b;
    --shadow: 0 8px 24px rgba(0,0,0,.35);
}
.cardpanel-wrap {
    background: var(--bg);
    height: 100%;
    color: var(--text);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    box-sizing: border-box;
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
.cardpanel-actions { display:flex; gap:12px; align-items:center; width:100%; }
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
    background: #3b82f6;
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
.cardpanel-search-btn:hover { background: #2563eb; }

.cardpanel-add {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--btn); color: #fff;
    border: none; border-radius: 10px; padding: 10px 14px;
    font-weight: 600; cursor: pointer;
    box-shadow: var(--shadow);
}
.cardpanel-add:hover { background: var(--btn-hover); }

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
    grid-template-columns: repeat(4, minmax(260px, 1fr));
    gap: 16px;
    background: transparent;
}
@media (max-width: 1300px) {
    .cardpanel-grid { grid-template-columns: repeat(3, minmax(260px, 1fr)); }
}
@media (max-width: 980px) {
    .cardpanel-grid { grid-template-columns: repeat(2, minmax(260px, 1fr)); }
}
@media (max-width: 640px) {
    .cardpanel-grid { grid-template-columns: 1fr; }
}

.card-card {
    background: var(--panel);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 18px;
    box-shadow: var(--shadow);
    display: flex; flex-direction: column; gap: 14px;
    min-height: 160px;
    transition: transform .15s ease, border-color .15s ease;
    cursor: pointer;
}
.card-card:hover { transform: translateY(-4px); border-color: #334155; }
.card-head { display:flex; align-items:center; gap:14px; }
.card-icon {
    width:44px; height:44px; display:grid; place-items:center;
    border-radius:12px; background: var(--chip);
    border:1px solid var(--surface-border);
}
.card-title { margin:0; font-size:16px; font-weight:700; letter-spacing:.2px; color:var(--text); }
.card-sub { color: var(--muted); font-size:13px; line-height:1.4; }
.card-foot { margin-top:auto; display:flex; justify-content:flex-end; }

.card-view {
    background: #0b5cf5; border: none; color: #fff; font-weight:600;
    padding: 8px 12px; border-radius: 10px; cursor: pointer;
}
.card-view:hover { background: #0a4bd1; }

.card-pill {
    display:inline-block; padding:3px 8px; border-radius:999px;
    background:#0f172a; color:#cbd5e1; border:1px solid #233044; font-size:12px;
}
`;

            const style = document.createElement("style");
            style.textContent = css;
            style.setAttribute("data-cardpanel-style", "true");
            document.head.appendChild(style);
        }

        _renderBase() {
            this.root.innerHTML = "";

            const wrap = document.createElement("div");
            wrap.className = "cardpanel-wrap";

            const header = document.createElement("div");
            header.className = "cardpanel-header";

            const left = document.createElement("div");
            left.style.display = "flex";
            left.style.alignItems = "center";
            left.style.gap = "12px";

            const title = document.createElement("div");
            title.className = "cardpanel-title";
            title.textContent = this.options.title;
            left.appendChild(title);

            const actions = document.createElement("div");
            actions.className = "cardpanel-actions";

            const searchWrap = document.createElement("div");
            searchWrap.className = "cardpanel-search";
            const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svg.setAttribute("width", "18");
            svg.setAttribute("height", "18");
            svg.setAttribute("viewBox", "0 0 24 24");
            svg.setAttribute("fill", "none");
            svg.innerHTML = `<path d="M21 21l-4.2-4.2" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"></path><circle cx="11" cy="11" r="7" stroke="#94a3b8" stroke-width="2"></circle>`;
            searchWrap.appendChild(svg);

            this._input = document.createElement("input");
            this._input.type = "text";
            this._input.placeholder = "Search data sources...";
            this._input.id = "cp_search_input";
            searchWrap.appendChild(this._input);

            this._searchBtn = document.createElement("button");
            this._searchBtn.className = "cardpanel-search-btn";
            this._searchBtn.textContent = "Search";
            searchWrap.appendChild(this._searchBtn);

            if (this.options.searchable !== false) {
                actions.appendChild(searchWrap);
            } else {
                searchWrap.style.display = "none";
            }

            this._addBtn = document.createElement("button");
            this._addBtn.className = "cardpanel-add";
            this._addBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="margin-right:6px;"><path d="M12 5v14M5 12h14" stroke="white" stroke-width="2" stroke-linecap="round"/></svg> Add Data Source`;
            actions.appendChild(this._addBtn);

            header.appendChild(left);
            header.appendChild(actions);

            const sub = document.createElement("div");
            sub.className = "cardpanel-subheader";

            const desc = document.createElement("div");
            desc.className = "cardpanel-desc";
            desc.textContent = this.options.description;
            sub.appendChild(desc);

            this._grid = document.createElement("div");
            this._grid.className = "cardpanel-grid";

            wrap.appendChild(header);
            wrap.appendChild(sub);
            wrap.appendChild(this._grid);
            this.root.appendChild(wrap);

            this._wireEvents();
        }

        _wireEvents() {
            if (this._searchBtn) {
                this._searchBtn.addEventListener("click", () => {
                    const query = this._input.value.trim();
                    this.emit("search", query);
                    if (this.options.autoFilter) {
                        this._filter(query);
                    }
                });
            }

            if (this._input) {
                this._input.addEventListener("keyup", (event) => {
                    const query = this._input.value.trim();

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
        }

        load(cards) {
            this.cards = Array.isArray(cards) ? cards.map(card => Object.assign({}, card)) : [];
            this._renderCards();
        }

        add(card) {
            this.cards.push(Object.assign({}, card));
            this._renderCards();
        }

        _renderCards() {
            this._grid.innerHTML = "";

            if (!this.cards.length) {
                const empty = document.createElement("div");
                empty.style.padding = "24px";
                empty.style.color = "var(--muted)";
                empty.textContent = "No cards to display.";
                this._grid.appendChild(empty);
                return;
            }

            this.cards.forEach(card => {
                const node = this._createCardNode(card);
                this._grid.appendChild(node);
            });
        }

        _createCardNode(card) {
            const wrap = document.createElement("div");
            wrap.className = "card-card";
            wrap.dataset.cardId = card.id || "";

            const head = document.createElement("div");
            head.className = "card-head";

            const iconWrap = document.createElement("div");
            iconWrap.className = "card-icon";
            if (card.icon) {
                if (typeof card.icon === "string") {
                    iconWrap.innerHTML = card.icon;
                } else if (card.icon instanceof Element) {
                    iconWrap.appendChild(card.icon);
                }
            }
            head.appendChild(iconWrap);

            const meta = document.createElement("div");
            const title = document.createElement("h3");
            title.className = "card-title";
            title.textContent = card.title || "";

            const sub = document.createElement("div");
            sub.className = "card-sub";
            sub.textContent = card.subtitle || "";

            meta.appendChild(title);
            meta.appendChild(sub);

            if (card.pill) {
                const pill = document.createElement("div");
                pill.className = "card-pill";
                pill.style.marginTop = "8px";
                pill.innerHTML = card.pill;
                meta.appendChild(pill);
            }

            head.appendChild(meta);

            const foot = document.createElement("div");
            foot.className = "card-foot";

            const viewBtn = document.createElement("button");
            viewBtn.className = "card-view";
            viewBtn.textContent = "View Details";
            viewBtn.addEventListener("click", (event) => {
                event.stopPropagation();
                this.emit("view", card.id);
            });

            foot.appendChild(viewBtn);

            wrap.appendChild(head);
            wrap.appendChild(foot);

            wrap.addEventListener("click", () => {
                this.emit("cardClick", card.id);
            });

            return wrap;
        }

        _filter(query) {
            const term = (query || "").toLowerCase();
            const children = Array.from(this._grid.children);

            children.forEach(child => {
                const id = child.dataset.cardId || "";
                const card = this.cards.find(c => (c.id || "") === id);

                if (!card) {
                    return;
                }

                const haystack = [
                    card.title || "",
                    card.subtitle || "",
                    card.pill || ""
                ].join(" ").toLowerCase();

                if (!term || haystack.indexOf(term) !== -1) {
                    child.style.display = "";
                } else {
                    child.style.display = "none";
                }
            });
        }
    }

    globalThis.customdhx.CardPanel = CardPanel;
})();
