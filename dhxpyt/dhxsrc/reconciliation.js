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
                    rows: this.initCategoryLayout(left_rows)
                  }
                ]
              },
              {
                type: "none",
                rows: [
                  {
                    type: "none",
                    padding: 10,
                    rows: this.initCategoryLayout(right_rows)
                  }
                ]
              }
            ]
          }
        ]
      });
      container.attach(this.layout);

      // var toolbar_h1 = new dhx.Toolbar(null, { css: "dhx_widget--bordered" }); toolbar_h1.data.parse([{}]); this.layout.getCell("H1").attach(toolbar_h1);

      // this.populateCategories(left_rows);
      // this.populateCategories(right_rows);
      
      // this.makeHeaderSection(left_rows);
      // this.makeHeaderSection(right_rows);

      this.renderCategoryHeaders(left_rows);
      this.renderCategoryHeaders(right_rows);
    }

    _getToolbarId(category_id) {
      return `${category_id}_toolbar`;
    }

    _getCategoryHeaderId(category_id) {
      return `${category_id}_header`;
    }

    _computeCategoryTotal(category) {
      return category.transactions.reduce((acc, item) => acc + item.amount, 0);
    }

    initCategoryLayout(rows) {
      // Initialize an empty array
      const list = [];
      console.log(rows)
      for (const row of rows) {
        const header_id = this._getCategoryHeaderId(row.category_id);
        const items_id = `${row.category_id}_items`;
        console.log(`creating header id ${header_id}`);
        console.log(`creating items id ${items_id}`);

        var category_header = {
          id: header_id,
          height: "auto",
          padding: 5,
        };

        var category_items = {
          id: items_id,
          height: "auto",
          hidden: true,
          // html: `<div id="${row.category_id}_grid"></div>`,
        };

        // Add the object to the list
        list.push(category_header);
        list.push(category_items);
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
        this.layout.getCell(header_cell_id).attach(categoryToolbar);
        this.toolbars[toolbar_id] = categoryToolbar;
      }
    }

    
    populateCategories(rows) {
      for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const item_details_grid = this.buildItemsGrid(row);
        console.log(`Attaching grid ${item_details_grid.data} to ${row.category_id}_items`);
        this.layout.getCell(`${row.category_id}_items`).attach(item_details_grid);
      }
    }
  
  }

  // Make Reconciliation class available globally:
  globalThis.customdhx.Reconciliation = Reconciliation;
})();
