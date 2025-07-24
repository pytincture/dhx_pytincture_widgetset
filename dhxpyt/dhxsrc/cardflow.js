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
            this.config = config || {};
            this.events = {};
            this.onNetDivClick = function () {};
            this.toolbar = [];
            this.sortOrder = "asc";
            this.optionItems = this.config.optionItems || [];
            this.rowMapping = {};
            this.showHeader = this.config.showHeader !== false;
            this.showSort = this.config.sortDisabled ? false : (this.config.showSort !== false);
            this.sortDisabled = this.config.sortDisabled || false;
            this.showDataHeaders = this.config.showDataHeaders !== false;
            this.fontSize = this.config.fontSize || "12px";
            this.showOptions = this.config.showOptions !== false; // NEW: Default to true
  
            if (this.config.columns && this.config.columns.length > 0) {
                this.sortColumnId = "";
            } else {
                this.sortColumnId = null;
            }
  
            const rows = this.config.data ? this.config.data.length : 0;
  
            const layoutRows = [];
            if (this.showHeader || (!this.sortDisabled && this.showSort)) {
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
  
            if (this.showHeader || (!this.sortDisabled && this.showSort)) {
                this.createSortToolbar();
                this.updateSortRowVisibility();
            }
  
            this.makeHeaderSection("C", rows);
            this.toolbarEventSetup();
        }
  
        toolbarEventSetup() {
            this.toolbar.forEach(toolbar => {
                const uid = toolbar._uid;
                const selector = `[data-dhx-widget-id="${uid}"]`;
                const currentLayout = this.layout;
  
                this.waitForElement(selector, 4000)
                    .then(widgetUl => {
                        const navElement = widgetUl.parentElement;
                        if (navElement && navElement.tagName.toLowerCase() === "nav") {
                            navElement.addEventListener("click", event => {
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
  
        setRowColor(rowId, color) {
            const toolbar = this.toolbar.find(tb => tb.id === rowId);
            if (!toolbar) {
                console.error(`Toolbar with id ${rowId} not found.`);
                return;
            }
            const toolbarSelector = `[data-dhx-widget-id="${toolbar._uid}"]`;
            this.waitForElement(toolbarSelector, 4000)
                .then(toolbarElem => {
                    toolbarElem.style.backgroundColor = color;
                    const rowData = this.config.data.find(row => row.id === rowId);
                    if (rowData) {
                        rowData._color = color;
                    }
                })
                .catch(error => {
                    console.error(`Toolbar element for ${toolbar._uid} not found:`, error);
                });
        }
  
        setRowFontSize(rowId, fontSize) {
            const toolbar = this.toolbar.find(tb => tb.id === rowId);
            if (!toolbar) {
                console.error(`Toolbar with id ${rowId} not found.`);
                return;
            }
            const toolbarSelector = `[data-dhx-widget-id="${toolbar._uid}"]`;
            this.waitForElement(toolbarSelector, 4000)
                .then(toolbarElem => {
                    const dataCells = toolbarElem.querySelectorAll(".toolbar-cell:not(.hideable)");
                    dataCells.forEach(cell => {
                        cell.style.fontSize = fontSize;
                    });
                    const rowData = this.config.data.find(row => row.id === rowId);
                    if (rowData) {
                        rowData._fontSize = fontSize;
                    }
                })
                .catch(error => {
                    console.error(`Toolbar element for ${toolbar._uid} not found:`, error);
                });
        }
  
        setRowDataValue(rowId, columnId, value) {
            const toolbar = this.toolbar.find(tb => tb.id === rowId);
            if (!toolbar) {
                console.error(`Toolbar with id ${rowId} not found.`);
                return;
            }
            const rowData = this.config.data.find(row => row.id === rowId);
            if (!rowData) {
                console.error(`Row data with id ${rowId} not found.`);
                return;
            }
            const column = this.config.columns.find(col => col.id === columnId);
            if (!column) {
                console.error(`Column with id ${columnId} not found.`);
                return;
            }
            const toolbarSelector = `[data-dhx-widget-id="${toolbar._uid}"]`;
            this.waitForElement(toolbarSelector, 4000)
                .then(toolbarElem => {
                    const dataCells = toolbarElem.querySelectorAll(".toolbar-cell:not(.hideable)");
                    const columnIndex = this.config.columns.findIndex(col => col.id === columnId);
                    if (columnIndex >= 0 && columnIndex < dataCells.length) {
                        let displayValue = value;
                        if (column.dataType === "time" && column.applyFormat && column.dataFormat) {
                            displayValue = formatTimeValue(value, column.dataFormat);
                        }
                        dataCells[columnIndex].textContent = displayValue;
                        rowData[columnId] = value;
                    } else {
                        console.error(`Column index for ${columnId} out of bounds or not found.`);
                    }
                })
                .catch(error => {
                    console.error(`Toolbar element for ${toolbar._uid} not found:`, error);
                });
        }
  
        // NEW: Method to show or hide the options button for a specific row
        setRowOptionsVisibility(rowId, show) {
            const toolbar = this.toolbar.find(tb => tb.id === rowId);
            if (!toolbar) {
                console.error(`Toolbar with id ${rowId} not found.`);
                return;
            }
            const rowData = this.config.data.find(row => row.id === rowId);
            if (!rowData) {
                console.error(`Row data with id ${rowId} not found.`);
                return;
            }
            toolbar.data.update("options", { hidden: !show });
            rowData._showOptions = show;
        }
  
        toggleDataHeaders(show) {
            this.showDataHeaders = show !== undefined ? show : !this.showDataHeaders;
            this.reDrawCards();
            this.toolbarEventSetup();
        }
  
        updateSortRowVisibility() {
            const sortRow = this.layout.getCell("sortRow");
            if (sortRow) {
                if (this.showHeader || (!this.sortDisabled && this.showSort)) {
                    sortRow.show();
                } else {
                    sortRow.hide();
                }
                if (this.sortToolbar) {
                    if (this.showHeader) {
                        this.sortToolbar.show("sortHeader");
                    } else {
                        this.sortToolbar.hide("sortHeader");
                    }
                    if (!this.sortDisabled && this.showSort) {
                        this.sortToolbar.show("sortLabel");
                        this.sortToolbar.show("combo");
                        this.sortToolbar.show("sortOrder");
                    } else {
                        this.sortToolbar.hide("sortLabel");
                        this.sortToolbar.hide("combo");
                        this.sortToolbar.hide("sortOrder");
                    }
                }
            }
        }
  
        toggleHeader(show) {
            this.showHeader = show !== undefined ? show : !this.showHeader;
            this.updateSortRowVisibility();
        }
  
        toggleSort(show) {
            if (this.sortDisabled) {
                console.warn("Sort controls are disabled (sortDisabled: true). Cannot toggle sort visibility.");
                return;
            }
            this.showSort = show !== undefined ? show : !this.showSort;
            this.updateSortRowVisibility();
        }
  
        createSortToolbar() {
            const sortCell = this.layout.getCell("sortCell");
            this.sortToolbar = new dhx.Toolbar(null, {
                id: "sortToolbar",
                css: "dhx_widget--bordered height55"
            });
            sortCell.attach(this.sortToolbar);
  
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
                    html: `<div style="font-family: 'Arial', sans-serif; margin-left:10px; font-weight: bold; font-size: 20px; line-height:40px; padding-right:5px;">${sortHeaderText}</div>`,
                    hidden: !this.showHeader
                });
                items.push({ type: "spacer" });
            } else {
                items.push({ type: "spacer" });
            }
            items.push({ 
                type: "customHTML", 
                id: "sortLabel", 
                html: "<div style='line-height:40px; padding-right:5px;'>Sort:</div>",
                hidden: this.sortDisabled || !this.showSort 
            });
            items.push({ 
                type: "customHTML", 
                id: "combo", 
                html: comboHTML,
                hidden: this.sortDisabled || !this.showSort 
            });
            items.push({ 
                type: "nav", 
                id: "sortOrder", 
                icon: "mdi mdi-sort-ascending", 
                tooltip: "Ascending",
                hidden: this.sortDisabled || !this.showSort 
            });
  
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
  
        sortCards() {
            if (!this.sortColumnId || this.sortDisabled) return;
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
                this.rowMapping[currentToolbar.id] = currentContent;
  
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
  
                if (rowData && rowData._fontSize) {
                    const toolbarSelector = `[data-dhx-widget-id="${currentToolbar._uid}"]`;
                    this.waitForElement(toolbarSelector, 4000)
                        .then(toolbarElem => {
                            const dataCells = toolbarElem.querySelectorAll(".toolbar-cell:not(.hideable)");
                            dataCells.forEach(cell => {
                                cell.style.fontSize = rowData._fontSize;
                            });
                        })
                        .catch(error => {
                            console.error(`Toolbar element for ${currentToolbar._uid} not found:`, error);
                        });
                }
  
                if (rowData && rowData._showOptions !== undefined) {
                    currentToolbar.data.update("options", { hidden: !rowData._showOptions });
                }
  
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
  
        deepQuerySelector(selector, root = document) {
            let element = root.querySelector(selector);
            if (element) return element;
            
            const children = root.querySelectorAll('*');
            for (const child of children) {
                if (child.shadowRoot) {
                    element = this.deepQuerySelector(selector, child.shadowRoot);
                    if (element) return element;
                }
            }
            return null;
        }
        
        waitForElement(selector, timeout = 2000, intervalTime = 50) {
            return new Promise((resolve, reject) => {
                let element = this.deepQuerySelector(selector);
                if (element) {
                    return resolve(element);
                }
                
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
                if (this.showDataHeaders) {
                    headerCells += `<div class="toolbar-cell${hideableClass}" style="font-weight: bold; padding-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: ${col.width || "100px"};">
                                      ${col.header}
                                    </div>`;
                }
                let value = rowData[col.id] !== undefined ? rowData[col.id] : "";
                if (col.dataType === "time" && col.applyFormat && col.dataFormat) {
                    value = formatTimeValue(value, col.dataFormat);
                }
                dataCells += `<div class="toolbar-cell${hideableClass}" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: ${col.width || "100px"}; font-size: ${rowData._fontSize || this.fontSize};">
                                ${value}
                              </div>`;
            }
  
            const toolbarItems = [
                { type: "nav", size: "small", id: "up", icon: "mdi mdi-chevron-right" },
                { type: "nav", size: "small", id: "down", icon: "mdi mdi-chevron-down", visible: false },
                { type: "customHTML", html: `
                  <div style="overflow:auto;width: 100%; background-color: inherit; padding: 10px 20px; font-family: Arial, sans-serif; box-sizing: border-box;">
                    <style>
                      @media (max-width: 600px) {
                        .hideable {
                          display: none;
                        }
                      }
                    </style>
                    ${this.showDataHeaders ? `<div style="display: grid; grid-template-columns: ${gridTemplateColumns}; gap: 10px;">
                      ${headerCells}
                    </div>` : ''}
                    <div style="display: grid; grid-template-columns: ${gridTemplateColumns}; gap: 10px; padding-top: ${this.showDataHeaders ? '2px' : '0'};">
                      ${dataCells}
                    </div>
                  </div>`
                },
                { type: "spacer" }
            ];
  
            // Conditionally add the options button based on showOptions and rowData._showOptions
            if (this.showOptions && (rowData._showOptions === undefined || rowData._showOptions)) {
                toolbarItems.push({
                    type: "customHTML",
                    id: "options",
                    html: '<i style="margin-right: 10px;font-size: 20px;" class="mdi mdi-dots-vertical-circle"></i>',
                    size: "medium",
                    icon: "mdi mdi-dots-vertical-circle",
                    items: this.optionItems.map(item => ({ id: item.id || item.value, ...item }))
                });
            }
  
            return toolbarItems;
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