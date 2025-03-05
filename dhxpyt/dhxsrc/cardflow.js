(function () {
    // Helper function to parse time strings (e.g. "09:30 AM") into minutes from midnight
    function parseTime(str) {
        var match = str.match(/(\d{1,2}):(\d{2})\s*(AM|PM)/i);
        if (match) {
            let hour = parseInt(match[1], 10);
            const minute = parseInt(match[2], 10);
            const period = match[3].toUpperCase();
            if (period === "PM" && hour < 12) hour += 12;
            if (period === "AM" && hour === 12) hour = 0;
            return hour * 60 + minute;
        }
        return NaN;
    }
  
    // Helper function to format time values according to a format string.
    // Expected tokens: "HH" for hour, "MM" for minutes, and "AM/PM" for period.
    function formatTimeValue(value, format) {
        let totalMinutes = parseTime(value);
        if (isNaN(totalMinutes)) return value;
        let hours24 = Math.floor(totalMinutes / 60);
        let minutes = totalMinutes % 60;
        let period = hours24 >= 12 ? "PM" : "AM";
        let hours12 = hours24 % 12;
        if (hours12 === 0) hours12 = 12;
        let hourStr = hours12.toString().padStart(2, "0");
        let minuteStr = minutes.toString().padStart(2, "0");
        return format.replace("HH", hourStr).replace("MM", minuteStr).replace("AM/PM", period);
    }
  
    // Ensure we have a "customdhx" namespace
    globalThis.customdhx = globalThis.customdhx || {};
  
    class CardFlow {
        constructor(container, config) {
            // Save the config (should include: columns, data, editable, group, groupable, etc.)
            this.config = config || {};
            this.events = {};
            this.onNetDivClick = function () {};
            this.toolbar = [];
            this.sortOrder = "asc";
            this.optionItems = this.config.optionItems || [];
            // NEW: Create a mapping to store layout cell id by toolbar id
            this.rowMapping = {};
  
            // Instead of defaulting to the first column, default to nothing.
            if (this.config.columns && this.config.columns.length > 0) {
                this.sortColumnId = "";
            } else {
                this.sortColumnId = null;
            }
  
            const rows = this.config.data ? this.config.data.length : 0;
  
            const layoutRows = [];
            if (!this.config.sortDisabled) {
                layoutRows.push({
                    id: "sortRow",
                    height: "75px",
                    padding: 10,
                    cols: [
                        {
                            id: "sortCell",
                            html: "<div id='sortToolbarContainer'></div>"
                        }
                    ],
                });
            }
            layoutRows.push({
                id: "cardsRow",
                cols: [this.getLayoutCount("C", rows)],
            });
  
            this.layout = new dhx.Layout(null, {
                id: "youknowme",
                type: "none",
                rows: layoutRows,
            });
            container.attach(this.layout);
  
            if (!this.config.sortDisabled) {
                this.createSortToolbar();
            }
  
            this.makeHeaderSection("C", rows);
            this.toolbarEventSetup();
        }
  
  
        toolbarEventSetup(){
            this.toolbar.forEach(toolbar => {
                const uid = toolbar._uid;
                const selector = `[data-dhx-widget-id="${uid}"]`;
                const currentLayout = this.layout;
  
                this.waitForElement(selector, 4000)
                    .then(widgetUl => {
                        const navElement = widgetUl.parentElement;
                        if (navElement && navElement.tagName.toLowerCase() === "nav") {
                            navElement.addEventListener("click", event => {
                                // the reason for not handing these items is that all others need to cause collapse / expand
                                if (event.target.className.indexOf("dhx_toolbar-button__icon") !== -1) {
                                } else if (event.target.className.indexOf("dhx_toolbar-button--icon") !== -1) {
                                } else if (event.target.className.indexOf("dhx_button") !== -1) {
                                } else if (event.target.className.indexOf("mdi-dots") !== -1) {
                                } else if (event.target.className.indexOf("dhx_toolbar__item") !== -1) {
                                } else {
                                    if (toolbar.stat === "down") {
                                        toolbar.show("up");
                                        toolbar.hide("down");
                                        toolbar.stat = "up";
                                        currentLayout.getCell(toolbar.contentCell).hide();
                                        this.onCollapse(toolbar.id, event);
                                    } else if (toolbar.stat === "up") {
                                        toolbar.show("down");
                                        toolbar.hide("up");
                                        toolbar.stat = "down";
                                        currentLayout.getCell(toolbar.contentCell).show();
                                        this.onExpand(toolbar.id, event);
                                    }
                                }
                            });
                        } else {
                            console.error("The parent element is not a <nav>.");
                        }
                    })
                    .catch(error => {
                        console.error(`Widget element for toolbar uid ${uid} not found within 4 seconds.`, error);
                    });
            });
        }
  
        // NEW: Updated attachToCardContent to use the mapping
        attachToCardContent(id, widget) {
            const cellId = this.rowMapping[id];
            if (!cellId) {
                console.error(`Mapping for card with id ${id} not found.`);
                return;
            }
            const cardContentCell = this.layout.getCell(cellId);
            if (cardContentCell) {
                cardContentCell.attach(widget);
            } else {
                console.error(`Card with id ${id} not found.`);
            }
        }
  
        // NEW: Updated detachCardFromContent to use the mapping
        detachCardFromContent(id) {
            const cellId = this.rowMapping[id];
            if (!cellId) {
                console.error(`Mapping for card with id ${id} not found.`);
                return;
            }
            const cardContentCell = this.layout.getCell(cellId);
            if (cardContentCell) {
                cardContentCell.detach();
            } else {
                console.error(`Card with id ${id} not found.`);
            }
        }
  
        createSortToolbar() {
            const sortCell = this.layout.getCell("sortCell");
            this.sortToolbar = new dhx.Toolbar(null, {
                id: "sortToolbar",
                css: "dhx_widget--bordered height55"
            });
            sortCell.attach(this.sortToolbar);
  
            // Add an initial placeholder option so nothing is selected by default.
            let optionsHTML = `<option value="" selected>Select</option>`;
            if (this.config.columns && this.config.columns.length > 0) {
                this.config.columns.forEach(col => {
                    const headerText = (typeof col.header === "string") ? col.header.replace(/:/g, "") : col.header;
                    optionsHTML += `<option value="${col.id}">${headerText}</option>`;
                });
            }
  
            const comboHTML = `<select id="sortColumnSelect" style="height:25px; font-size:12px; width:80px;">${optionsHTML}</select>`;
            const sortHeaderText = this.config.sortHeader || "";
            const items = [];
            if (sortHeaderText) {
                items.push({
                    type: "customHTML",
                    id: "sortHeader",
                    html: `<div style="font-family: 'Arial', sans-serif; margin-left:10px; font-weight: bold; font-size: 16px; line-height:40px; padding-right:5px;">${sortHeaderText}</div>`
                });
                items.push({ type: "spacer" });
            } else {
                items.push({ type: "spacer" });
            }
            items.push({ type: "customHTML", id: "sortLabel", html: "<div style='line-height:40px; padding-right:5px;'>Sort:</div>" });
            items.push({ type: "customHTML", id: "combo", html: comboHTML });
            items.push({ type: "nav", id: "sortOrder", icon: "mdi mdi-sort-ascending", tooltip: "Ascending" });
  
            this.sortToolbar.data.parse(items);
  
            setTimeout(() => {
                const selectEl = document.getElementById("sortColumnSelect");
                if (selectEl) {
                    selectEl.addEventListener("change", (e) => {
                        this.sortColumnId = e.target.value;
                        this.sortCards();
                    });
                }
            }, 100);
  
            this.sortToolbar.events.on("click", (id, e) => {
                if (id === "sortOrder") {
                    this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc";
                    const newIcon = this.sortOrder === "asc" ? "mdi mdi-sort-ascending" : "mdi mdi-sort-descending";
                    const newTooltip = this.sortOrder === "asc" ? "Ascending" : "Descending";
                    this.sortToolbar.data.update("sortOrder", { icon: newIcon, tooltip: newTooltip });
                    this.sortCards();
                }
            });
        }
  
        // UPDATED: sortCards now uses column definitions (dataType, dataFormat, and applyFormat) for conversion.
        sortCards() {
            if (!this.sortColumnId) return;
            // Find the column definition for the sort column
            const colDef = (this.config.columns || []).find(col => col.id === this.sortColumnId);
  
            this.config.data.sort((a, b) => {
                let aVal = a[this.sortColumnId];
                let bVal = b[this.sortColumnId];
  
                if (colDef && colDef.dataType) {
                    switch(colDef.dataType) {
                        case "float":
                        case "int":
                            aVal = parseFloat(aVal);
                            bVal = parseFloat(bVal);
                            break;
                        case "time":
                            aVal = parseTime(aVal);
                            bVal = parseTime(bVal);
                            break;
                        default:
                            aVal = aVal.toString();
                            bVal = bVal.toString();
                    }
                } else {
                    // No explicit dataType provided.
                    const aNum = parseFloat(aVal);
                    const bNum = parseFloat(bVal);
                    if (!isNaN(aNum) && !isNaN(bNum)) {
                        aVal = aNum;
                        bVal = bNum;
                    } else {
                        const aDate = new Date(aVal);
                        const bDate = new Date(bVal);
                        if (!isNaN(aDate.getTime()) && !isNaN(bDate.getTime())) {
                            aVal = aDate.getTime();
                            bVal = bDate.getTime();
                        } else {
                            aVal = aVal.toString();
                            bVal = bVal.toString();
                        }
                    }
                }
  
                if (aVal < bVal) return this.sortOrder === "asc" ? -1 : 1;
                if (aVal > bVal) return this.sortOrder === "asc" ? 1 : -1;
                return 0;
            });
            this.reDrawCards();
            this.toolbarEventSetup();
        }
  
        reDrawCards() {
            const rows = this.config.data ? this.config.data.length : 0;
            this.toolbar.forEach(toolbar => {
                if (toolbar.destructor) {
                    toolbar.destructor();
                }
            });
            this.toolbar = [];
            for (let i = 0; i < rows; i++) {
                const cellA = this.layout.getCell(`C${i + 1}A`);
                const cellB = this.layout.getCell(`C${i + 1}B`);
                if (cellA && cellA.clear) cellA.clear();
                if (cellB && cellB.clear) cellB.clear();
            }
            this.makeHeaderSection("C", rows);
        }
  
        onExpand(id, event) {
            //console.log("expand", id, event);
        }
  
        onCollapse(id, event) {
            //console.log("collapse", id, event);
        }
  
        onOptions(id, event, optionValue) {
            //console.log("options", id, event, optionValue);
        }
  
        makeHeaderSection(cell_start, rows) {
            const dataSet = this.config.data || [];
            const columns = this.config.columns || [];
  
            for (let index = 0; index < rows; index++) {
                const ndx = index + 1;
                const currentToolbar = new dhx.Toolbar(null, {
                    id: `toolbar${cell_start}${ndx}`,
                    css: "dhx_widget--bordered height55"
                });
                const currentContent = cell_start + ndx.toString() + "B";
  
                const rowData = dataSet[index];
                if (rowData) {
                    if (rowData.id) {
                        currentToolbar.id = rowData.id;
                    } else {
                        currentToolbar.id = (index + 1).toString();
                    }
                }
  
                currentToolbar.data.parse(this.getToolbarData(columns, rowData));
                this.layout.getCell(`${cell_start}${ndx}A`).attach(currentToolbar);
                this.layout.getCell(currentContent).hide();
                currentToolbar.hide("down");
                this.toolbar.push(currentToolbar);
                currentToolbar.stat = "up";
                currentToolbar.contentCell = currentContent;
                // Save mapping between toolbar id and its corresponding content cell id.
                this.rowMapping[currentToolbar.id] = currentContent;
  
                // If the row contains _color, apply it to the toolbar container.
                if (rowData && rowData._color) {
                    const toolbarSelector = `[data-dhx-widget-id="${currentToolbar._uid}"]`;
                    this.waitForElement(toolbarSelector, 4000)
                        .then(toolbarElem => {
                            toolbarElem.style.backgroundColor = rowData._color;
                        })
                        .catch(error => {
                            console.error(`Toolbar element for ${currentToolbar._uid} not found:`, error);
                        });
                }
  
                // Update click handling for options items
                currentToolbar.events.on("click", function (id, e) {
                    const optionsItem = currentToolbar.data.getItem("options");
                    if (
                        optionsItem &&
                        optionsItem.items &&
                        optionsItem.items.find(item => item.id === id)
                    ) {
                        this.onOptions(currentToolbar.id, e, id);
                    } else if (id.endsWith("up")) {
                        currentToolbar.hide(id);
                        currentToolbar.show("down");
                        currentToolbar.stat = "down";
                        this.layout.getCell(currentContent).show();
                        this.onExpand(currentToolbar.id, e);
                    } else if (id.endsWith("down")) {
                        currentToolbar.show("up");
                        currentToolbar.hide("down");
                        currentToolbar.stat = "up";
                        this.layout.getCell(currentContent).hide();
                        this.onCollapse(currentToolbar.id, e);
                    }
                }.bind(this));
            }
        }

        // Recursively search the DOM and any shadow DOMs for the selector.
        deepQuerySelector(selector, root = document) {
            // Try finding it in the current root.
            let element = root.querySelector(selector);
            if (element) return element;
            
            // If not found, search through all elements that might host a shadow root.
            const children = root.querySelectorAll('*');
            for (const child of children) {
            if (child.shadowRoot) {
                element = deepQuerySelector(selector, child.shadowRoot);
                if (element) return element;
            }
            }
            return null;
        }
        
        waitForElement(selector, timeout = 2000, intervalTime = 50) {
            return new Promise((resolve, reject) => {
            // First check using the deep search
            let element = this.deepQuerySelector(selector);
            if (element) {
                return resolve(element);
            }
            
            // Polling method with setInterval.
            const interval = setInterval(() => {
                element = this.deepQuerySelector(selector);
                if (element) {
                clearInterval(interval);
                clearTimeout(timer);
                resolve(element);
                }
            }, intervalTime);
            
            const timer = setTimeout(() => {
                clearInterval(interval);
                reject(new Error("Timeout reached: element not found."));
            }, timeout);
            });
        }
          
  
        getToolbarData(columns, rowData) {
            const len = columns.length;
            const gridTemplateColumns = columns.map(col => col.width ? col.width : "100px").join(" ");
            let headerCells = "";
            let dataCells = "";
  
            for (let i = 0; i < len; i++) {
                const col = columns[i];
                const hideableClass = i >= 2 ? " hideable" : "";
                headerCells += `<div class="toolbar-cell${hideableClass}" style="font-weight: bold; padding-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: ${col.width || "100px"};">
                                  ${col.header}
                                </div>`;
                let value = rowData[col.id] !== undefined ? rowData[col.id] : "";
                // If the column is a time and applyFormat is true, reformat the value.
                if (col.dataType === "time" && col.applyFormat && col.dataFormat) {
                    value = formatTimeValue(value, col.dataFormat);
                }
                dataCells += `<div class="toolbar-cell${hideableClass}" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: ${col.width || "100px"};">
                                ${value}
                              </div>`;
            }
  
            const customhtml = `
              <div style="overflow:auto;width: 100%; background-color: inherit; padding: 10px 20px; font-family: Arial, sans-serif; box-sizing: border-box;">
                <style>
                  @media (max-width: 600px) {
                    .hideable {
                      display: none;
                    }
                  }
                </style>
                <div style="display: grid; grid-template-columns: ${gridTemplateColumns}; gap: 10px;">
                  ${headerCells}
                </div>
                <div style="display: grid; grid-template-columns: ${gridTemplateColumns}; gap: 10px; padding-top: 2px;">
                  ${dataCells}
                </div>
              </div>`;
  
            return [
                { type: "nav", size: "small", id: "up", icon: "mdi mdi-chevron-right" },
                { type: "nav", size: "small", id: "down", icon: "mdi mdi-chevron-down", visible: false },
                { type: "customHTML", html: customhtml },
                { type: "spacer" },
                { 
                    type: "customHTML", 
                    id: "options", 
                    html: '<i style="margin-right: 10px;font-size: 20px;" class="mdi mdi-dots-vertical-circle"></i>', 
                    size: "medium", 
                    icon: "mdi mdi-dots-vertical-circle", 
                    items: this.optionItems.map(item => ({ id: item.id || item.value, ...item })) 
                }
            ];
        }
  
        getLayoutCount(name, rows) {
            const list = [];
            for (let i = 0; i < rows; i++) {
                const ndx = i + 1;
                const itemA = { id: `${name}${ndx}A`, height: "auto", padding: 5 };
                const itemB = { id: `${name}${ndx}B`, height: "auto", html: "", padding: 5 };
                list.push(itemA);
                list.push(itemB);
            }
            return {
                type: "none",
                rows: [{ type: "none", padding: 10, rows: list, css:"layout-scroll"}]
            };
        }
  
        collapseAll() {
            this.toolbar.forEach(toolbar => {
                if (toolbar.stat === "up") {
                    const currentContent = toolbar.contentCell;
                    this.layout.getCell(currentContent).hide();
                    toolbar.show("down");
                    toolbar.stat = "down";
                    this.onCollapse(toolbar.id, {});
                }
            });
        }
    
        expandAll() {
            this.toolbar.forEach(toolbar => {
                if (toolbar.stat === "down") {
                    const currentContent = toolbar.contentCell;
                    this.layout.getCell(currentContent).show();
                    toolbar.show("up");
                    toolbar.stat = "up";
                    this.onExpand(toolbar.id, {});
                }
            });
        }
    }
  
    globalThis.customdhx.CardFlow = CardFlow;
})();
