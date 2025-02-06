(function () {
  // Ensure we have a "customdhx" object in the global scope
  globalThis.customdhx = globalThis.customdhx || {};

  class Reconciliation {
      constructor(container, data) {
          // The data passed in (e.g. categories, description, etc.)
          this.data = data || {};
          this.events = {};
          this.onNetDivClick = function () {};
          this.toolbar = [];
          var left_rows = 4;
          var right_rows = 4;

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
                              rows: this.getLayoutCount("C", left_rows)
                            }
                          ]
                      },
                      {     
                        type: "none",
                        rows: [
                          {
                            type: "none",
                            padding: 10,
                            rows: this.getLayoutCount("R", right_rows)
                          }
                      ]
                    }
                  ]
                }
              ]
          });
          container.attach(this.layout);
          
          var toolbar_h1 = new dhx.Toolbar(null, {css: "dhx_widget--bordered"});toolbar_h1.data.parse([{}]);this.layout.getCell("H1").attach(toolbar_h1);

          this.makeHeaderSection("C", left_rows);
          this.makeHeaderSection("R", right_rows);
      }

      makeHeaderSection(cell_name, rows) {
        Array.from({ length: rows }).forEach((_, index) => {
          console.log(`Processing row ${index + 1}`);
          var ndx = index + 1;
          this.toolbar["toolbar"+cell_name+ndx.toString()] = new dhx.Toolbar(null, {css: "dhx_widget--bordered"});
          this.toolbar["toolbar"+cell_name+ndx.toString()].data.parse(this.getToolbarData(`${cell_name}${ndx}`));
          this.layout.getCell(`${cell_name}${ndx}A`).attach(this.toolbar["toolbar"+cell_name+ndx.toString()]);
          this.layout.getCell(`${cell_name}${ndx}B`).hide();
          const currentLayout = this.layout;
          const currentToolbar = this.toolbar["toolbar"+cell_name+ndx.toString()];
          currentToolbar.hide([`${cell_name}${ndx}down`]);
          this.toolbar["toolbar" + cell_name + ndx.toString()].events.on("click", function(id, e) {
              if(id.endsWith("up")) {
                // -2 because of up
                currentToolbar.hide([`${id}`])
                currentToolbar.show([`${id.slice(0, -2)}down`])
                currentLayout.getCell(`${id.slice(0, -2)}B`).show();
              } else {
                // -4 is becuase of down
                currentToolbar.show([`${id.slice(0, -4)}up`])
                currentToolbar.hide([`${id}`])
                currentLayout.getCell(`${id.slice(0, -4)}B`).hide();
              }
          });
        });
      }

      getToolbarData(name) {
        return [{ id: name+"up", icon: "mdi mdi-chevron-right" }, { id: name+"down", icon: "mdi mdi-chevron-down", visible: false}]
      }

      getLayoutCount(name, rows) {
        // Initialize an empty array
        const list = [];
        
        // Loop 'count' times to fill the list
        for (let i = 0; i < rows; i++) {
            // Create an object with an id and a value
            var ndx = i + 1;
            var itemA = {
              id: `${name}${ndx}A`,
              height: "auto",
              padding: 5,
            };
            var itemB = {
              id: `${name}${ndx}B`,
              height: "auto",
              html: "<div>HELLO WORLD<div>",
            };
            
            // Add the object to the list
            list.push(itemA);
            list.push(itemB);
        }
        
        return list;
      }

      // -----------------------------------------------------------------------
      // Below here is your original logic for building the UI and handling events
      // -----------------------------------------------------------------------

      on(event, callback) {
          this.events[event] = callback;
      }

      emit(event, detail) {
          if (this.events[event]) {
              this.events[event](detail);
          }
      }

      render() {
          // Optionally return our box if you like
          console.log("render");
          return this.box;
      }

      renderHeader() {
          console.log("renderHeader");
          this.header = document.createElement('div');

          // Create the h2 element and set its text content
          const h2 = document.createElement('h2');
          h2.textContent = this.data.description || "No Description";

          // Create the div for netTotal and set its class and text content
          this.netTotalDiv = document.createElement('div');
          this.netTotalDiv.id = 'netTotal';
          this.netTotalDiv.classList.add('net_total');
          this.netTotalDiv.textContent = 'Net Total: $0';

          this.netTotalDiv.onclick = (click_event) => {
              const newEvent = {
                  type: "anytype",
                  target: this.netTotalDiv.id,
                  value: this.netTotalDiv.textContent,
                  event_callback: "onNetDivClick"
              };
              this.onNetDivClick(newEvent);
          };

          // Append the h2 and netTotal div to the header
          this.header.appendChild(h2);
          this.header.appendChild(this.netTotalDiv);

          // Append the header to the box
          this.box.appendChild(this.header);
      }

      onNetDivClickEvent(proxy) {
          this.onNetDivClick = proxy;
          this.netTotalDiv.addEventListener("click", this.onNetDivClick);
      }

      updateHeader() {
          // If you want to dynamically update the netTotalDiv text
          this.netTotalDiv.textContent = 'Net Total: $updateHeader value';
          // If you want to repaint, just call .paint() or do direct DOM updates
      }

      renderPanels() {
          const panels = document.createElement('div');
          panels.style.display = 'flex';
          panels.style.gap = '20px';

          const incomePanel = this.createPanel('income', this.data.income_categories || []);
          const expensePanel = this.createPanel('expense', this.data.expense_categories || []);

          panels.appendChild(incomePanel);
          panels.appendChild(expensePanel);
          this.box.appendChild(panels);
      }

      createPanel(type, categories) {
          const panel = document.createElement('div');
          panel.className = `${type}_panel`;
          panel.innerHTML = `<h3>${type.charAt(0).toUpperCase() + type.slice(1)}</h3>`;
          categories.forEach(category => {
              const categoryEl = this.createCategory(category);
              panel.appendChild(categoryEl);
          });
          return panel;
      }

      createCategory(category) {
          const wrapper = document.createElement('details');
          wrapper.innerHTML = `
              <summary>${category.name} (<span class="transaction-count">${category.transactions.length}</span>)</summary>
              <div class="transaction-list"></div>
          `;
          const list = wrapper.querySelector('.transaction-list');
          if (category.transactions.length === 0) {
              list.innerHTML = '<p class="no-transactions">No transactions.</p>';
          } else {
              category.transactions.forEach(txn => list.appendChild(this.createTransaction(txn)));
          }
          return wrapper;
      }

      createTransaction(txn) {
          const txnEl = document.createElement('div');
          txnEl.className = 'txn_card';
          txnEl.innerHTML = `
              <input type="checkbox" class="txn_checkbox" data-amount="${txn.amount}" ${txn.checked ? 'checked' : ''}>
              <div class="txn_details">
                  <div>${txn.txn_date} - ${txn.memo}</div>
                  <div>${txn.counterparty} (${txn.counterparty_desc || ''})</div>
                  ${txn.source_url ? `<a href="${txn.source_url}" target="_blank">View Source</a>` : ''}
              </div>
              <div class="txn_amount">$${txn.amount}</div>
          `;
          txnEl.querySelector('.txn_checkbox').addEventListener('change', () => this.updateTotals());
          return txnEl;
      }

      renderCloseUI() {
          const closeSection = document.createElement('div');
          closeSection.innerHTML = `
              <div id="overrideSection" style="display:none;">
                  <input type="checkbox" id="overrideCheckbox"> I understand the imbalance.
              </div>
              <button id="closeBooksBtn" disabled>Close Books</button>
          `;
          closeSection.querySelector('#overrideCheckbox').addEventListener('change', () => this.updateTotals());
          closeSection.querySelector('#closeBooksBtn').addEventListener('click', () => this.emit('close', {}));
          this.box.appendChild(closeSection);
      }

      updateTotals() {
          let totalIncome = 0;
          let totalExpense = 0;
          this.box.querySelectorAll('.income_panel .txn_checkbox:checked')
              .forEach(el => totalIncome += parseFloat(el.dataset.amount));
          this.box.querySelectorAll('.expense_panel .txn_checkbox:checked')
              .forEach(el => totalExpense += parseFloat(el.dataset.amount));

          const netTotal = totalIncome - totalExpense;
          const netTotalEl = this.netTotalDiv; 
          netTotalEl.innerText = `Net Total: $${netTotal}`;
          netTotalEl.className = netTotal === 0 ? 'net_total net_positive' : 'net_total net_negative';

          const overrideSection = this.box.querySelector('#overrideSection');
          const closeBooksBtn = this.box.querySelector('#closeBooksBtn');
          if (overrideSection && closeBooksBtn) {
              overrideSection.style.display = netTotal === 0 ? 'none' : 'block';
              closeBooksBtn.disabled = netTotal !== 0 && !this.box.querySelector('#overrideCheckbox').checked;
          }

          this.emit('update', { totalIncome, totalExpense, netTotal });
      }
  }

  // Make Reconciliation class available globally:
  globalThis.customdhx.Reconciliation = Reconciliation;
})();
