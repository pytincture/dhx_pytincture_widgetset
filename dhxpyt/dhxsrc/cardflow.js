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
            this.defaultExpandedHeight = this.config.defaultExpandedHeight || "300px";
            this.showHeader = this.config.showHeader !== false;
            this.showSort = this.config.sortDisabled ? false : (this.config.showSort !== false);
            this.sortDisabled = this.config.sortDisabled || false;
            this.showDataHeaders = this.config.showDataHeaders !== false;
            this.fontSize = this.config.fontSize || "12px";
            this.toolbarFontFamily = this.config.toolbarFontFamily || "Arial, sans-serif";
            this.showOptions = this.config.showOptions !== false;

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
                            html: "<div id='sortToolbarContainer' style='width: 100%;'></div>"
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

        // Method to set expanded height for a specific card (can be called dynamically)
        setCardExpandedHeight(cardId, height) {
            const rowData = this.config.data.find(row => row.id === cardId);
            if (rowData) {
                rowData._expanded_height = height;
            }
            
            // If the card is currently expanded, update its height immediately
            const toolbar = this.toolbar.find(tb => tb.id === cardId);
            if (toolbar && toolbar.stat === "down") {
                const cellId = this.rowMapping[cardId];
                if (cellId) {
                    this.updateCellHeight(cellId, height);
                }
            }
        }

        // Helper method to update cell height dynamically
        updateCellHeight(cellId, height) {
            const cellElement = document.querySelector(`[data-dhx-id="${cellId}"]`);
            if (cellElement) {
                cellElement.style.height = height;
                cellElement.style.minHeight = height;
            }
        }

        // Helper method to get the expanded height for a card
        getCardExpandedHeight(cardId) {
            const rowData = this.config.data.find(row => row.id === cardId);
            return (rowData && rowData._expanded_height) ? rowData._expanded_height : this.defaultExpandedHeight;
        }

        toolbarEventSetup() {
            this.toolbar.forEach(toolbar => {
                if (toolbar.stat !== "down" && toolbar.stat !== "up") {
                    toolbar.stat = "up";
                }

                const uid = toolbar._uid;
                const selector = `[data-dhx-widget-id="${uid}"]`;
                const currentLayout = this.layout;

                this.waitForElement(selector, 4000)
                    .then(widgetUl => {
                const navElement = widgetUl.closest("nav") || widgetUl;
                if (!navElement.__cardflowClickHandler) {
                    const handler = (event) => {
                        if (event.target.className.indexOf("dhx_toolbar-button__icon") !== -1) {
                        } else if (event.target.className.indexOf("dhx_toolbar-button--icon") !== -1) {
                        } else if (event.target.className.indexOf("dhx_button") !== -1) {
                        } else if (event.target.className.indexOf("mdi-dots") !== -1) {
                        } else if (event.target.className.indexOf("dhx_toolbar__item") !== -1) {
                        } else {
                            if (toolbar.stat !== "down" && toolbar.stat !== "up") {
                                toolbar.stat = "up";
                            }
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
                                        const contentCell = currentLayout.getCell(toolbar.contentCell);
                                        contentCell.show();
                                        // Apply the specific height for this card from _expanded_height or default
                                const expandedHeight = this.getCardExpandedHeight(toolbar.id);
                                this.updateCellHeight(toolbar.contentCell, expandedHeight);
                                this.onExpand(toolbar.id, event);
                            }
                        }
                    };
                    navElement.addEventListener("click", handler);
                    navElement.__cardflowClickHandler = handler;
                }
                if (!navElement) {
                    console.error("Toolbar container not found for nav click handling.");
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
                    this._applyFontFamilyToElement(toolbarElem);
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
                    let cellIndex = 0;
                    for (let i = 0; i < this.config.columns.length; i++) {
                        if (this.config.columns[i].type === "stretch") continue;
                        if (this.config.columns[i].id === columnId) {
                            break;
                        }
                        cellIndex++;
                    }
                    if (cellIndex < dataCells.length) {
                        let displayValue = value;
                        if (column.dataType === "time" && column.applyFormat && column.dataFormat) {
                            displayValue = formatTimeValue(value, column.dataFormat);
                        }
                        dataCells[cellIndex].textContent = displayValue;
                        rowData[columnId] = value;
                    } else {
                        console.error(`Column index for ${columnId} out of bounds or not found.`);
                    }
                })
                .catch(error => {
                    console.error(`Toolbar element for ${toolbar._uid} not found:`, error);
                });
        }

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
                css: "dhx_widget--bordered height55",
                width: "100%"
            });
            sortCell.attach(this.sortToolbar);

            let optionsHTML = `<option value="" selected>Select</option>`;
            if (this.config.columns && this.config.columns.length > 0) {
                this.config.columns.forEach(col => {
                    if (col.type === "stretch" || !col.id) return;
                    const headerText = (typeof col.header === "string") ? col.header.replace(/:/g, "") : col.header;
                    optionsHTML += `<option value="$${col.id}">$${headerText}</option>`;
                });
            }

            const comboHTML = `<select id="sortColumnSelect" style="height:25px; font-size:12px; width:80px;">${optionsHTML}</select>`;
            const sortHeaderText = this.config.sortHeader || "";
            const items = [];
            if (sortHeaderText) {
                items.push({
                    type: "customHTML",
                    id: "sortHeader",
                    html: sortHeaderText,
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
            if (this.events["onCardExpand"]) {
                this.events["onCardExpand"](id, event);
            }
        }

        onCollapse(id, event) {
            if (this.events["onCardCollapse"]) {
                this.events["onCardCollapse"](id, event);
            }
        }

        onOptions(id, event, optionValue) {
            if (this.events["onOptions"]) {
                this.events["onOptions"](id, event, optionValue);
            }
        }

        makeHeaderSection(cell_start, rows) {
            const dataSet = this.config.data || [];
            const columns = this.config.columns || [];

            for (let index = 0; index < rows; index++) {
                const ndx = index + 1;
                const currentToolbar = new dhx.Toolbar(null, {
                    id: `toolbar$${cell_start}$${ndx}`,
                    css: "dhx_widget--bordered height55",
                    width: "100%"
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
                this._applyToolbarFontFamily(currentToolbar);

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
                    } else {
                        if (currentToolbar.stat !== "down" && currentToolbar.stat !== "up") {
                            currentToolbar.stat = "up";
                        }

                        if (id.endsWith("up")) {
                        currentToolbar.hide(id);
                        currentToolbar.show("down");
                        currentToolbar.stat = "down";
                        this.layout.getCell(currentContent).show();
                        // Apply the specific height for this card from _expanded_height or default
                        const expandedHeight = this.getCardExpandedHeight(currentToolbar.id);
                        this.updateCellHeight(currentContent, expandedHeight);
                        this.onExpand(currentToolbar.id, e);
                        } else if (id.endsWith("down")) {
                        currentToolbar.show("up");
                        currentToolbar.hide("down");
                        currentToolbar.stat = "up";
                        this.layout.getCell(currentContent).hide();
                        this.onCollapse(currentToolbar.id, e);
                    }
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

        _applyFontFamilyToElement(element) {
            if (!element || !this.toolbarFontFamily) {
                return;
            }
            element.style.fontFamily = this.toolbarFontFamily;
            const cells = element.querySelectorAll(".toolbar-cell");
            cells.forEach(cell => {
                cell.style.fontFamily = this.toolbarFontFamily;
            });
        }

        _applyToolbarFontFamily(toolbarInstance) {
            if (!toolbarInstance) {
                return;
            }
            const selector = `[data-dhx-widget-id="${toolbarInstance._uid}"]`;
            this.waitForElement(selector, 4000)
                .then(toolbarElem => {
                    this._applyFontFamilyToElement(toolbarElem);
                })
                .catch(error => {
                    console.error(`Toolbar element for ${toolbarInstance._uid} not found:`, error);
                });
        }

        getToolbarData(columns, rowData) {
            let headerCells = "";
            let dataCells = "";
            let leftColumns = "";
            let rightColumns = "";
            let stretchIndex = -1;
            let cellIndex = 0; // For hideable class and cell indexing

            // Detect stretch column and build column widths
            for (let i = 0; i < columns.length; i++) {
                const col = columns[i];
                if (col.type === "stretch") {
                    stretchIndex = i;
                    continue;
                }
                const colWidth = col.width || "100px";
                if (i < stretchIndex || stretchIndex === -1) {
                    leftColumns += colWidth + " ";
                } else {
                    rightColumns += colWidth + " ";
                }
            }

            // Build cells
            for (let i = 0; i < columns.length; i++) {
                const col = columns[i];
                if (col.type === "stretch") continue;
                const hideableClass = cellIndex >= 2 ? " hideable" : "";
                const colWidth = col.width || "100px";
                if (this.showDataHeaders) {
                    headerCells += `<div class="toolbar-cell${hideableClass}" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: ${colWidth}; font-weight: bold; padding-bottom: 2px; font-family: ${this.toolbarFontFamily};">
                                      ${col.header}
                                    </div>`;
                }
                let value = rowData[col.id] !== undefined ? rowData[col.id] : "";
                if (col.dataType === "time" && col.applyFormat && col.dataFormat) {
                    value = formatTimeValue(value, col.dataFormat);
                }
                dataCells += `<div class="toolbar-cell${hideableClass}" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: ${colWidth}; font-size: ${rowData._fontSize || this.fontSize}; font-family: ${this.toolbarFontFamily};">
                                ${value}
                              </div>`;
                cellIndex++;
            }

            let htmlContent = `
              <div style="width: 100%; background-color: inherit; padding: 10px 20px; font-family: ${this.toolbarFontFamily}; box-sizing: border-box;">
                <style>
                  @media (max-width: 600px) {
                    .hideable {
                      display: none;
                    }
                  }
                  .toolbar-cell:not(.hideable) {
                    min-width: 0;
                  }
                </style>
            `;

            if (stretchIndex !== -1) {
                // Use flexbox layout for stretch
                const leftHeaderCells = stretchIndex > 0 ? headerCells.split('</div>').slice(0, stretchIndex).join('</div>') + '</div>' : '';
                const rightHeaderCells = headerCells.split('</div>').slice(stretchIndex).join('</div>') + (headerCells ? '</div>' : '');
                const leftDataCells = stretchIndex > 0 ? dataCells.split('</div>').slice(0, stretchIndex).join('</div>') + '</div>' : '';
                const rightDataCells = dataCells.split('</div>').slice(stretchIndex).join('</div>') + (dataCells ? '</div>' : '');

                if (this.showDataHeaders) {
                    htmlContent += `
                      <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                        <div style="display: grid; grid-template-columns: ${leftColumns}; gap: 10px;">
                          ${leftHeaderCells}
                        </div>
                        <div style="display: grid; grid-template-columns: ${rightColumns}; gap: 10px;">
                          ${rightHeaderCells}
                        </div>
                      </div>
                    `;
                }

                htmlContent += `
                  <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; padding-top: ${this.showDataHeaders ? '2px' : '0'};">
                    <div style="display: grid; grid-template-columns: ${leftColumns}; gap: 10px;">
                      ${leftDataCells}
                    </div>
                    <div style="display: grid; grid-template-columns: ${rightColumns}; gap: 10px;">
                      ${rightDataCells}
                    </div>
                  </div>
                `;
            } else {
                // Use grid layout for no stretch
                const gridTemplateColumns = columns.map(col => col.width || "100px").join(" ");
                if (this.showDataHeaders) {
                    htmlContent += `
                      <div style="display: grid; grid-template-columns: ${gridTemplateColumns}; gap: 10px; width: 100%;">
                        ${headerCells}
                      </div>
                    `;
                }
                htmlContent += `
                  <div style="display: grid; grid-template-columns: ${gridTemplateColumns}; gap: 10px; padding-top: ${this.showDataHeaders ? '2px' : '0'}; width: 100%;">
                    ${dataCells}
                  </div>
                `;
            }

            htmlContent += `</div>`;

            const toolbarItems = [
                { type: "nav", size: "small", id: "up", icon: "mdi mdi-chevron-right" },
                { type: "nav", size: "small", id: "down", icon: "mdi mdi-chevron-down", visible: false },
                { type: "customHTML", html: htmlContent },
                { type: "spacer" }
            ];

            if (this.showOptions && (rowData._showOptions === undefined || rowData._showOptions)) {
                toolbarItems.push({
                    type: "customHTML",
                    id: "options",
                    html: '<i style="margin-right: 10px; font-size: 20px;" class="mdi mdi-dots-vertical-circle"></i>',
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
                const itemA = { id: `${name}${ndx}A`, height: "auto", padding: 5, width: "100%" };
                const itemB = { id: `${name}${ndx}B`, height: "auto", html: "", padding: 5, width: "100%" };
                list.push(itemA);
                list.push(itemB);
            }
            return {
                type: "none",
                rows: [{ type: "none", padding: 10, rows: list, css: "layout-scroll", width: "100%" }]
            };
        }

        collapseAll() {
            this.toolbar.forEach(toolbar => {
                if (toolbar.stat === "down") {
                    const currentContent = toolbar.contentCell;
                    this.layout.getCell(currentContent).hide();
                    toolbar.show("up");
                    toolbar.hide("down");
                    toolbar.stat = "up";
                    this.onCollapse(toolbar.id, {});
                } else if (toolbar.stat !== "up") {
                    const currentContent = toolbar.contentCell;
                    this.layout.getCell(currentContent).hide();
                    toolbar.show("up");
                    toolbar.hide("down");
                    toolbar.stat = "up";
                    this.onCollapse(toolbar.id, {});
                }
            });
        }
    
        expandAll() {
            this.toolbar.forEach(toolbar => {
                if (toolbar.stat === "up" || toolbar.stat === undefined || toolbar.stat === null) {
                    const currentContent = toolbar.contentCell;
                    this.layout.getCell(currentContent).show();
                    // Apply the specific height for this card from _expanded_height or default
                    const expandedHeight = this.getCardExpandedHeight(toolbar.id);
                    this.updateCellHeight(currentContent, expandedHeight);
                    toolbar.hide("up");
                    toolbar.show("down");
                    toolbar.stat = "down";
                    this.onExpand(toolbar.id, {});
                } else if (toolbar.stat !== "down") {
                    const currentContent = toolbar.contentCell;
                    this.layout.getCell(currentContent).show();
                    const expandedHeight = this.getCardExpandedHeight(toolbar.id);
                    this.updateCellHeight(currentContent, expandedHeight);
                    toolbar.hide("up");
                    toolbar.show("down");
                    toolbar.stat = "down";
                    this.onExpand(toolbar.id, {});
                }
            });
        }
    }

    globalThis.customdhx.CardFlow = CardFlow;
})();
