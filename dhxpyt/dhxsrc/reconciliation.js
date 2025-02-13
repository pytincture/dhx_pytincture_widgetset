(function () {
  // Ensure we have a "customdhx" object in the global scope
  globalThis.customdhx = globalThis.customdhx || {};

  class Reconciliation {
    constructor(container, data) {
      // The data passed in (e.g. categories, description, etc.)
      this.data = data.data || {};
      this.events = {};
      this.toolbars = [];

      var left_rows = this.data.expense_categories;
      var right_rows = this.data.income_categories;
      
      this.layout = new dhx.Layout(null, {
        type: "wide",
        rows: [
          {
            id: "H1",
            height: "auto"
          },
          {
            cols: [
              {
                type: "wide",
                rows: [
                  {
                    type: "wide",
                    padding: 10,
                    width: "100%",
                    rows: this.setupCategoryLayout(left_rows)
                  }
                ]
              },
              {
                type: "wide",
                rows: [
                  {
                    type: "wide",
                    padding: 10,
                    width: "100%",
                    rows: this.setupCategoryLayout(right_rows)
                  }
                ]
              }
            ]
          }
        ]
      });

      this.layout.events.on("afterShow", (cellId) => {
        const categoryId = cellId.replace("_items", "");
        const category = left_rows.find(cat => cat.category_id === categoryId) ||
                 right_rows.find(cat => cat.category_id === categoryId);        
        this.layout.getCell(cellId).attach(this.buildItemsGrid(category));
      });

      container.attach(this.layout);

      this.renderCategoryHeaders(left_rows);
      this.renderCategoryHeaders(right_rows);

      console.log(`Adding event listeners to toolbars ${this.toolbars.length}`);
      this.toolbars.forEach(toolbar => {
        const uid = toolbar._uid;
        const selector = `[data-dhx-widget-id="${uid}"]`;
        const currentToolbar = toolbar;
        const currentLayout = this.layout;

        this.waitForElement(selector, 2000)
          .then(widgetUl => {
            const navElement = widgetUl.parentElement;
            const toolbar = currentToolbar;
            const toolbarId = toolbar.config.id;
            const categoryItemsId = toolbarId.replace("_toolbar", "_items");
            const layout = currentLayout;
            if (navElement && navElement.tagName.toLowerCase() === "nav") {
              navElement.addEventListener("click", event => {
                if (toolbar.getState(toolbarId) == true) {
                  layout.cell(categoryItemsId).show();
                  toolbar.setState({[toolbarId]: false});
                } else {
                  layout.cell(categoryItemsId).hide();
                  toolbar.setState({[toolbarId]: true});
                }
              });
            } else {
              console.error("The parent element is not a <nav>.");
            }
          })
          .catch(error => {
            console.error(`Widget element for toolbar uid ${uid} not found within 2 seconds.`, error);
          });
      });

      dhx.cssManager.add({
        display: "none",
        padding: 0
      }, "dhx_grid-header-cell");

      dhx.cssManager.add({
        display: "inline",
      }, "dhx_layout-rows");

    }

    _getToolbarId(category_id) {
      return `${category_id}_toolbar`;
    }

    _getCategoryHeaderId(category_id) {
      return `${category_id}_header`;
    }

    _getCategoryItemsId(category_id) {
      return `${category_id}_items`;
    }

    _computeCategoryTotal(category) {
      return category.transactions.reduce((acc, item) => acc + item.amount, 0);
    }

    setupCategoryLayout(rows) {
      // Initialize an empty array
      const list = [];
      for (const row of rows) {
        const header_id = this._getCategoryHeaderId(row.category_id);
        const items_id = this._getCategoryItemsId(row.category_id);

        var category_header_cell = {
          id: header_id,
          type: "wide",
          width: "100%",
        };

        var category_items_cell = {
          id: items_id,
          type: "wide",
          width: "100%",
          hidden: true,
          height: "contents",
        };

        // Add the object to the list
        list.push(category_header_cell);
        list.push(category_items_cell);
      }

      return list;
    };

    getHeaderHtml(name, row) {
      return `
        <table style="width: 100%;">
          <tr>
            <td>${row.name}</td>
            <td>${this._computeCategoryTotal(row)}</td>
          </tr>
        </table>
      `;
    }

    waitForElement(selector, timeout = 2000, intervalTime = 50) {
      return new Promise((resolve, reject) => {
        const interval = setInterval(() => {
          const element = document.querySelector(selector);
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
    
    getCategoryToolbarConfig(name, row) {
      const up_id = `${name}up`;
      const down_id = `${name}down`;
      return [
        { id: name, type: "button", full: true, twoState: true, html: this.getHeaderHtml(name, row) },
      ];
    }

    renderCategoryHeaders(rows) {
      for (const row of rows) {
        const category_id = row.category_id;
        const toolbar_id = this._getToolbarId(category_id);
        const header_cell_id = this._getCategoryHeaderId(category_id);
        const categoryToolbar = new dhx.Toolbar(null, {id: toolbar_id, css: "dhx_widget--bordered" });
        categoryToolbar.data.parse(this.getCategoryToolbarConfig(toolbar_id, row));
        categoryToolbar.setState({[toolbar_id]: true});
        this.addCategoryHeaderEvents(categoryToolbar, this.layout);
        this.layout.getCell(header_cell_id).attach(categoryToolbar);
        this.toolbars.push(categoryToolbar);
      }
    }

    addCategoryHeaderEvents(categoryToolbar, currentLayout) {
      categoryToolbar.events.on("click", function (id, e) {
        const category_items_id = id.replace("_toolbar", "_items");
        if (categoryToolbar.getState(id) == true) {
          currentLayout.cell(category_items_id).show();
        } else {
          currentLayout.cell(category_items_id).hide();
        }
      });
    }

    
    buildItemsGrid(category) {
      const dataset = category.transactions.map(({ memo, amount }) => {
        return {
          "selected": "true",
          "info": `${memo}`,
          "total": `${amount}`
        };
      });

      const grid = new dhx.Grid(`${category.category_id}_grid`, {
        columns: [
          { id: "selected", header: [{ text: "" }] },
          { id: "info", header: [{ text: "Info" }] },
          { id: "total", header: [{ text: "Amount" }], align: "right" },
        ],
        headerRowHeight: 0,
        adjust: true,
        height: -1,
        width: "100%",
      });

      grid.data.parse(dataset);
      return grid;
    }  
  }

  // Make Reconciliation class available globally:
  globalThis.customdhx.Reconciliation = Reconciliation;
})();
