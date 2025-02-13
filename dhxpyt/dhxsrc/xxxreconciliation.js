// (function () {
//   // Ensure we have a "customdhx" object in the global scope
//   globalThis.customdhx = globalThis.customdhx || {};

//   class xxxReconciliation {
//     constructor(container, data) {
//       // The data passed in (e.g. categories, description, etc.)
//       this.data = data.data || {};
//       this.events = {};
//       this.onNetDivClick = function () { };
//       this.toolbar = [];

//       var left_rows = this.data.expense_categories;
//       var right_rows = this.data.income_categories;
      
//       this.layout = new dhx.Layout(null, {
//         type: "none",
//         rows: [
//           {
//             id: "H1",
//             height: "auto"
//           },
//           {
//             cols: [
//               {
//                 type: "none",
//                 rows: [
//                   {
//                     type: "none",
//                     padding: 10,
//                     rows: this.scaffoldCategories(left_rows)
//                   }
//                 ]
//               },
//               {
//                 type: "none",
//                 rows: [
//                   {
//                     type: "none",
//                     padding: 10,
//                     rows: this.scaffoldCategories(right_rows)
//                   }
//                 ]
//               }
//             ]
//           }
//         ]
//       });
//       container.attach(this.layout);

//       // var toolbar_h1 = new dhx.Toolbar(null, { css: "dhx_widget--bordered" }); toolbar_h1.data.parse([{}]); this.layout.getCell("H1").attach(toolbar_h1);

//       this.populateCategories(left_rows);
//       this.populateCategories(right_rows);
      
//       this.makeHeaderSection(left_rows);
//       this.makeHeaderSection(right_rows);
//     }


//     populateCategories(rows) {
//       for (let i = 0; i < rows.length; i++) {
//         const row = rows[i];
//         const item_details_grid = this.buildItemsGrid(row);
//         console.log(`Attaching grid ${item_details_grid.data} to ${row.category_id}_items`);
//         this.layout.getCell(`${row.category_id}_items`).attach(item_details_grid);
//       }
//     }

//     makeHeaderSection(rows) {
//       Array.from({ length: rows.length }).forEach((_, index) => {
//         const row = rows[index];
//         const cell_name = row.category_id
//         // const category_and_transactions = this.renderCategory(cell_name, row);
//         // console.log(category_and_transactions)
//         var ndx = index + 1;
//         const toolbar_id = `toolbar${cell_name}`;
//         const header_cell_id = `${cell_name}_header`;
//         const items_cell_id = `${cell_name}_items`;
//         const down_id = `${cell_name}_headerdown`;
//         console.log(`makeHeaderSection ${toolbar_id} ${header_cell_id} ${items_cell_id} ${down_id}`);
//         this.toolbar[toolbar_id] = new dhx.Toolbar(null, { css: "dhx_widget--bordered" });
//         this.toolbar[toolbar_id].data.parse(this.getToolbarData(header_cell_id, row));
//         this.layout.getCell(header_cell_id).attach(this.toolbar[toolbar_id]);
//         // this.layout.getCell(items_cell_id).hide();
//         const currentLayout = this.layout;
//         const currentToolbar = this.toolbar[toolbar_id];
//         currentToolbar.hide([down_id]);
//         this.toolbar[toolbar_id].events.on("click", function (id, e) {
//           console.log(`click ${id}`);
//           console.log(e)
//           if (id.endsWith("up")) {
//             // -2 because of up
//             const down_id = `${id.slice(0, -2)}down`;
//             const items_id = `${id.slice(0, -9)}_items`;
//             console.log(`showing ${down_id} and ${items_id} and hiding ${id}`);
//             currentToolbar.hide([id])
//             currentToolbar.show([down_id])
//             currentLayout.cell(items_id).toggle();
//           } else {
//             // -4 is becuase of down
//             const up_id = `${id.slice(0, -4)}up`;
//             const items_id = `${id.slice(0, -11)}_items`;
//             console.log(`showing ${up_id} and hiding ${id} and ${items_id}`);
//             currentToolbar.show([up_id])
//             currentToolbar.hide([id])
//             populateCategories(this.data.expense_categories);
//             populateCategories(this.data.income_categories);
//             currentLayout.cell(items_id).toggle();
//           }
//         });
//       });
//     }

//     getToolbarData(name, row) {
//       const up_id = `${name}up`;
//       const down_id = `${name}down`;
//       console.log(`getToolbarData ${up_id} ${down_id}`);
//       return [{value: `${row.name}`},{ id: up_id, icon: "mdi mdi-chevron-right" }, { id: down_id, icon: "mdi mdi-chevron-down", visible: false }]
//     }

//     scaffoldCategories(rows) {
//       // Initialize an empty array
//       const list = [];
//       console.log(rows)
//       for (let i = 0; i < rows.length; i++) {
//         const row = rows[i];
//         const header_id = `${row.category_id}_header`;
//         const items_id = `${row.category_id}_items`;
//         console.log(`creating header id ${header_id}`);
//         console.log(`creating items id ${items_id}`);
//         // Create an object with an id and a value
//         var ndx = i + 1;
//         var category_header = {
//           id: header_id,
//           height: "auto",
//           padding: 5,
//         };
//         var category_items = {
//           id: items_id,
//           height: "auto",
//           hidden: true,
//           // html: `<div id="${row.category_id}_grid"></div>`,
//         };
        
//         // Add the object to the list
//         list.push(category_header);
//         list.push(category_items);
//       }

//       return list;
//     };


//     buildItemsGrid(category) {
//       console.log(JSON.stringify(category));
//       console.log(JSON.stringify(category.transactions));
//       const dataset = category.transactions.map(({memo, amount}) => {
//         return {
//           "selected": "true",
//           "info": `${memo}`,
//           "total": `${amount}`
//         };
//       });

//       console.log(`building grid for ${category.category_id}_grid using ${dataset}`);
//       const grid = new dhx.Grid(`${category.category_id}_grid`, {
//         columns: [
//           { id: "selected", header: [{ text: "" }] },
//           { id: "info", header: [{ text: "Info" }] },
//           { id: "total", header: [{ text: "Amount" }] },
//         ],
//         headerRowHeight: 0,
//         data: dataset,
//         align: "left",
//       });

//       return grid;
//     }

//     // -----------------------------------------------------------------------
//     // Below here is your original logic for building the UI and handling events
//     // -----------------------------------------------------------------------

//     on(event, callback) {
//       this.events[event] = callback;
//     }

//     emit(event, detail) {
//       if (this.events[event]) {
//         this.events[event](detail);
//       }
//     }

//     render() {
//       // Optionally return our box if you like
//       console.log("render");
//       return this.box;
//     }

//     renderHeader() {
//       console.log("renderHeader");
//       this.header = document.createElement('div');

//       // Create the h2 element and set its text content
//       const h2 = document.createElement('h2');
//       h2.textContent = this.data.description || "No Description";

//       // Create the div for netTotal and set its class and text content
//       this.netTotalDiv = document.createElement('div');
//       this.netTotalDiv.id = 'netTotal';
//       this.netTotalDiv.classList.add('net_total');
//       this.netTotalDiv.textContent = 'Net Total: $0';

//       this.netTotalDiv.onclick = (click_event) => {
//         const newEvent = {
//           type: "anytype",
//           target: this.netTotalDiv.id,
//           value: this.netTotalDiv.textContent,
//           event_callback: "onNetDivClick"
//         };
//         this.onNetDivClick(newEvent);
//       };

//       // Append the h2 and netTotal div to the header
//       this.header.appendChild(h2);
//       this.header.appendChild(this.netTotalDiv);

//       // Append the header to the box
//       this.box.appendChild(this.header);
//     }

//     onNetDivClickEvent(proxy) {
//       this.onNetDivClick = proxy;
//       this.netTotalDiv.addEventListener("click", this.onNetDivClick);
//     }

//     updateHeader() {
//       // If you want to dynamically update the netTotalDiv text
//       this.netTotalDiv.textContent = 'Net Total: $updateHeader value';
//       // If you want to repaint, just call .paint() or do direct DOM updates
//     }

//     renderPanels() {
//       const panels = document.createElement('div');
//       panels.style.display = 'flex';
//       panels.style.gap = '20px';

//       const incomePanel = this.createPanel('income', this.data.income_categories || []);
//       const expensePanel = this.createPanel('expense', this.data.expense_categories || []);

//       panels.appendChild(incomePanel);
//       panels.appendChild(expensePanel);
//       this.box.appendChild(panels);
//     }

//     createPanel(type, categories) {
//       const panel = document.createElement('div');
//       panel.className = `${type}_panel`;
//       panel.innerHTML = `<h3>${type.charAt(0).toUpperCase() + type.slice(1)}</h3>`;
//       categories.forEach(category => {
//         const categoryEl = this.createCategory(category);
//         panel.appendChild(categoryEl);
//       });
//       return panel;
//     }

//     createCategory(category) {
//       const wrapper = document.createElement('details');
//       wrapper.innerHTML = `
//               <summary>${category.name} (<span class="transaction-count">${category.transactions.length}</span>)</summary>
//               <div class="transaction-list"></div>
//           `;
//       const list = wrapper.querySelector('.transaction-list');
//       if (category.transactions.length === 0) {
//         list.innerHTML = '<p class="no-transactions">No transactions.</p>';
//       } else {
//         category.transactions.forEach(txn => list.appendChild(this.createTransaction(txn)));
//       }
//       return wrapper;
//     }

//     createTransaction(txn) {
//       const txnEl = document.createElement('div');
//       txnEl.className = 'txn_card';
//       txnEl.innerHTML = `
//               <input type="checkbox" class="txn_checkbox" data-amount="${txn.amount}" ${txn.checked ? 'checked' : ''}>
//               <div class="txn_details">
//                   <div>${txn.txn_date} - ${txn.memo}</div>
//                   <div>${txn.counterparty} (${txn.counterparty_desc || ''})</div>
//                   ${txn.source_url ? `<a href="${txn.source_url}" target="_blank">View Source</a>` : ''}
//               </div>
//               <div class="txn_amount">$${txn.amount}</div>
//           `;
//       txnEl.querySelector('.txn_checkbox').addEventListener('change', () => this.updateTotals());
//       return txnEl.outerHTML;
//     }

//     renderCloseUI() {
//       const closeSection = document.createElement('div');
//       closeSection.innerHTML = `
//               <div id="overrideSection" style="display:none;">
//                   <input type="checkbox" id="overrideCheckbox"> I understand the imbalance.
//               </div>
//               <button id="closeBooksBtn" disabled>Close Books</button>
//           `;
//       closeSection.querySelector('#overrideCheckbox').addEventListener('change', () => this.updateTotals());
//       closeSection.querySelector('#closeBooksBtn').addEventListener('click', () => this.emit('close', {}));
//       this.box.appendChild(closeSection);
//     }

//     updateTotals() {
//       console.log("updateTotals");
//       let totalIncome = 0;
//       let totalExpense = 0;
//       this.box.querySelectorAll('.income_panel .txn_checkbox:checked')
//         .forEach(el => totalIncome += parseFloat(el.dataset.amount));
//       this.box.querySelectorAll('.expense_panel .txn_checkbox:checked')
//         .forEach(el => totalExpense += parseFloat(el.dataset.amount));

//       const netTotal = totalIncome - totalExpense;
//       const netTotalEl = this.netTotalDiv;
//       netTotalEl.innerText = `Net Total: $${netTotal}`;
//       netTotalEl.className = netTotal === 0 ? 'net_total net_positive' : 'net_total net_negative';

//       const overrideSection = this.box.querySelector('#overrideSection');
//       const closeBooksBtn = this.box.querySelector('#closeBooksBtn');
//       if (overrideSection && closeBooksBtn) {
//         overrideSection.style.display = netTotal === 0 ? 'none' : 'block';
//         closeBooksBtn.disabled = netTotal !== 0 && !this.box.querySelector('#overrideCheckbox').checked;
//       }

//       this.emit('update', { totalIncome, totalExpense, netTotal });
//     }
//   }

//   // Make Reconciliation class available globally:
//   globalThis.customdhx.Reconciliation = Reconciliation;
// })();
