class Reconciliation {
  constructor(container, data) {
    this.container = document.querySelector(container);
    this.data = data;
    this.events = {};
    this.render();
  }

  on(event, callback) {
    this.events[event] = callback;
  }

  emit(event, detail) {
    if (this.events[event]) {
      this.events[event](detail);
    }
  }

  render() {
    this.container.innerHTML = '';
    this.renderHeader();
    this.renderPanels();
    this.renderCloseUI();
    this.updateTotals();
  }

  renderHeader() {
    const header = document.createElement('div');
    header.innerHTML = `
      <h2>${this.data.description}</h2>
      <div id="netTotal" class="net_total">Net Total: $0</div>
    `;
    this.container.appendChild(header);
  }

  renderPanels() {
    const panels = document.createElement('div');
    panels.style.display = 'flex';
    panels.style.gap = '20px';
    
    const incomePanel = this.createPanel('income', this.data.income_categories);
    const expensePanel = this.createPanel('expense', this.data.expense_categories);
    
    panels.appendChild(incomePanel);
    panels.appendChild(expensePanel);
    this.container.appendChild(panels);
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
    this.container.appendChild(closeSection);
  }

  updateTotals() {
    let totalIncome = 0;
    let totalExpense = 0;
    this.container.querySelectorAll('.income_panel .txn_checkbox:checked').forEach(el => totalIncome += parseFloat(el.dataset.amount));
    this.container.querySelectorAll('.expense_panel .txn_checkbox:checked').forEach(el => totalExpense += parseFloat(el.dataset.amount));
    const netTotal = totalIncome - totalExpense;
    const netTotalEl = document.getElementById('netTotal');
    netTotalEl.innerText = `Net Total: $${netTotal}`;
    netTotalEl.className = netTotal === 0 ? 'net_total net_positive' : 'net_total net_negative';
    document.getElementById('overrideSection').style.display = netTotal === 0 ? 'none' : 'block';
    document.getElementById('closeBooksBtn').disabled = netTotal !== 0 && !document.getElementById('overrideCheckbox').checked;
    this.emit('update', { totalIncome, totalExpense, netTotal });
  }
}


// Example usage
document.addEventListener('DOMContentLoaded', () => {
    fetch('proto.json')
        .then(response => response.json())
        .then(data => {
            const reconciliation = new Reconciliation('#reconciliationContainer', data);

            reconciliation.on('update', ({ totalIncome, totalExpense, netTotal }) => {
                console.log(`Updated: Income - $${totalIncome}, Expense - $${totalExpense}, Net - $${netTotal}`);
            });

            reconciliation.on('close', () => {
                alert('Books closed successfully!');
            });
        })
        .catch(error => console.error('Error loading data:', error));
});