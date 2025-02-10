(function () {
  // Ensure we have a "customdhx" object in the global scope
  globalThis.customdhx = globalThis.customdhx || {};

  class Reconciliation {
    constructor(container, data) {
      // The data passed in (e.g. categories, description, etc.)
      this.data = data.data || {};
      this.events = {};
      this.onNetDivClick = function () { };
      this.toolbars = [];

      var left_rows = this.data.expense_categories;
      var right_rows = this.data.income_categories;
      
      this.layout = new dhx.Layout(null, {
        type: "none",
        rows: [
          {
            id: "H1",
            height: "auto"
          },
          {
            cols: [
              {
                type: "none",
                rows: [
                  {
                    type: "none",
                    padding: 10,
                    rows: this.setupCategoryLayout(left_rows)
                  }
                ]
              },
              {
                type: "none",
                rows: [
                  {
                    type: "none",
                    padding: 10,
                    rows: this.setupCategoryLayout(right_rows)
                  }
                ]
              }
            ]
          }
        ]
      });

      this.layout.events.on("afterShow", (cellId) => {
        console.log(`layout afterShow ${cellId}`);
        console.log(left_rows);
        console.log(right_rows);
        const categoryId = cellId.replace("_items", "");
        console.log(`searching for category ${categoryId}`);
        const category = left_rows.find(cat => cat.category_id === categoryId) ||
                 right_rows.find(cat => cat.category_id === categoryId);
        
        console.log(`passing category ${category.category_id}`);
        this.layout.getCell(cellId).attach(this.buildItemsGrid(category));
      });

      container.attach(this.layout);

      this.renderCategoryHeaders(left_rows);
      this.renderCategoryHeaders(right_rows);

      dhx.cssManager.add({
        display: "none",
        padding: 0
      }, "dhx_grid-header-cell");

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
      console.log(rows)
      for (const row of rows) {
        const header_id = this._getCategoryHeaderId(row.category_id);
        const items_id = this._getCategoryItemsId(row.category_id);
        console.log(`creating header id ${header_id}`);
        console.log(`creating items id ${items_id}`);

        var category_header_cell = {
          id: header_id,
          height: "auto",
        };

        var category_items_cell = {
          id: items_id,
          hidden: true,
          height: "auto",
        };

        // Add the object to the list
        list.push(category_header_cell);
        list.push(category_items_cell);
      }

      return list;
    };

    getHeaderToolbarConfig(name, row) {
      const up_id = `${name}up`;
      const down_id = `${name}down`;
      console.log(`getToolbarData ${up_id} ${down_id}`);
      return [
        { id: up_id, icon: "mdi mdi-chevron-right" }, 
        { id: down_id, icon: "mdi mdi-chevron-down", visible: false }, 
        { value: `${row.name}` },
        { value: `${this._computeCategoryTotal(row)}` }
      ];
    }

    renderCategoryHeaders(rows) {
      for (const row of rows) {
        const category_id = row.category_id;
        const toolbar_id = this._getToolbarId(category_id);
        const header_cell_id = this._getCategoryHeaderId(category_id);
        const categoryToolbar = new dhx.Toolbar(null, { css: "dhx_widget--bordered" });
        categoryToolbar.data.parse(this.getHeaderToolbarConfig(toolbar_id, row));
        this.addCategoryHeaderEvents(categoryToolbar, this.layout);
        this.layout.getCell(header_cell_id).attach(categoryToolbar);
        this.toolbars[toolbar_id] = categoryToolbar;
      }
    }

    addCategoryHeaderEvents(categoryToolbar, currentLayout) {
      categoryToolbar.events.on("click", function (id, e) {
        if (id.endsWith("up")) {
          // -2 because of up
          const category_toolbar_id = id.slice(0, -2);
          const down_id = `${category_toolbar_id}down`;
          categoryToolbar.hide([id]);
          categoryToolbar.show([down_id]);
          const category_items_id = category_toolbar_id.replace("_toolbar", "_items");
          currentLayout.cell(`${category_items_id}`).show();
        } else {
          // -4 is becuase of down
          const category_toolbar_id = id.slice(0, -4);
          const up_id = `${category_toolbar_id}up`;
          const items_id = `${id.slice(0, -11)}_items`;
          categoryToolbar.show([up_id]);
          categoryToolbar.hide([id]);
          const category_items_id = category_toolbar_id.replace("_toolbar", "_items");
          currentLayout.cell(`${category_items_id}`).hide();
        }
      });
    }

    
    buildItemsGrid(category) {
      console.log(`building grid for ${category.category_id}`);
      console.log(`category.transactions ${JSON.stringify(category)}`);
      const dataset = category.transactions.map(({ memo, amount }) => {
        return {
          "selected": "true",
          "info": `${memo}`,
          "total": `${amount}`
        };
      });

      console.log(`building grid for ${category.category_id}_grid using ${JSON.stringify(dataset)}`);
      const grid = new dhx.Grid(`${category.category_id}_grid`, {
        columns: [
          { id: "selected", header: [{ text: "" }] },
          { id: "info", header: [{ text: "Info" }] },
          { id: "total", header: [{ text: "Amount" }], align: "right" },
        ],
        headerRowHeight: 0,
        // adjust: true,
        autoWidth: true
      });

      grid.data.parse(dataset);
      return grid;
    }  
  }

  // Make Reconciliation class available globally:
  globalThis.customdhx.Reconciliation = Reconciliation;
})();
