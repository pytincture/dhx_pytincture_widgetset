globalThis.customdhx = globalThis.customdhx || {};


class Reconciliation {
  constructor(container, data) {
    // this.container = document.querySelector(container);
    this.container = container;
    this.data = data;
    this.events = {};
    this.onNetDivClick = function () {};
    
    this.box = document.createElement('div');
    this.box.id = 'adfjkey3fnan';
    this.renderHeader();
    // this.renderPanels();
    // this.renderCloseUI();
    // this.updateTotals();
    console.log(this.box.id);
    this.container.attachHTML(this.box.innerHTML);
    console.log(this.box.id);
  }

  // dhx stuff

  getRootView() {
    console.log(this.box)
    // return this.box._view;
    return this.box;
  }

  //
  on(event, callback) {
    this.events[event] = callback;
  }

  emit(event, detail) {
    if (this.events[event]) {
      this.events[event](detail);
    }
  }

  // only render the widget when it gets attached
  // container should be another layout widget
  // expect this.container to be a layout
  // assume container is a dhx layout (cell) (not undefined)
  // build up html then dump it into container

  render() {
    // // this.container.innerHTML = '';
    // this.box = document.createElement('div');
    // this.box.id = 'adfjkey3fnan';
    // this.renderHeader();
    // // this.renderPanels();
    // // this.renderCloseUI();
    // // this.updateTotals();
    // console.log(this.box.id);
    // this.container.attachHTML(this.box.innerHTML);
    // console.log(this.box.id);

    return this.box;
  }

  // // come back and fix this html
  // renderHeader() {
  //   this.header = document.createElement('div');
  //   this.header.innerHTML = `
  //     <h2>${this.data.description}</h2>
  //     <div id="netTotal" class="net_total">Net Total: $0</div>
  //   `;
  //   this.box.appendChild(this.header);
  // }

  renderHeader() {
    this.header = document.createElement('div');

    // Create the h2 element and set its text content
    const h2 = document.createElement('h2');
    h2.textContent = this.data.description;

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
      }
      this.onNetDivClick(newEvent);
    }

    // Append the h2 and netTotal div to the header
    this.header.appendChild(h2);
    this.header.appendChild(this.netTotalDiv);

    // Append the header to the box
    this.box.appendChild(this.header);
  }

  onNetDivClickEvent(proxy) {
    this.onNetDivClick = proxy;
    this.netTotalDiv.addEventListener("click", this.onNetDivClick)
  }

  updateHeader() {
    // Create the div for netTotal and set its class and text content
    this.netTotalDiv = document.createElement('div');
    this.netTotalDiv.id = 'netTotal';
    this.netTotalDiv.classList.add('net_total');
    this.netTotalDiv.textContent = 'Net Total: $updateHeader value';

    this.container.attachHTML(this.box.innerHTML);
  }

  renderPanels() {
    const panels = document.createElement('div');
    panels.style.display = 'flex';
    panels.style.gap = '20px';
    
    const incomePanel = this.createPanel('income', this.data.income_categories);
    const expensePanel = this.createPanel('expense', this.data.expense_categories);
    
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
    closeSection.querySelector('#overrideCheckbox'). addEventListener('change', () => this.updateTotals());
    closeSection.querySelector('#closeBooksBtn').addEventListener('click', () => this.emit('close', {}));
    this.box.appendChild(closeSection);
  }

  updateTotals() {
    let totalIncome = 0;
    let totalExpense = 0;
    this.box.querySelectorAll('.income_panel .txn_checkbox:checked').forEach(el => totalIncome += parseFloat(el.dataset.amount));
    this.box.querySelectorAll('.expense_panel .txn_checkbox:checked').forEach(el => totalExpense += parseFloat(el.dataset.amount));
    const netTotal = totalIncome - totalExpense;
    const netTotalEl = document.getElementById('netTotal');
    netTotalEl.innerText = `Net Total: $${netTotal}`;
    netTotalEl.className = netTotal === 0 ? 'net_total net_positive' : 'net_total net_negative';
    document.getElementById('overrideSection').style.display = netTotal === 0 ? 'none' : 'block';
    document.getElementById('closeBooksBtn').disabled = netTotal !== 0 && !document.getElementById('overrideCheckbox').checked;
    this.emit('update', { totalIncome, totalExpense, netTotal });
  }
}


// 3. Attach the class to your global object
globalThis.customdhx.Reconciliation = Reconciliation;
