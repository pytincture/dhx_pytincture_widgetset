(function () {
    globalThis.customdhx = globalThis.customdhx || {};
    
    class RagWidget {
        constructor(container, config) {
            this.config = config || {};
            this.eventListeners = {};
            this.streamTarget = null;
            this.currentStreamId = null;
            
            // Core properties
            this.chats = JSON.parse(localStorage.getItem('chats')) || [];
            this.activeChatId = localStorage.getItem('activeChatId') || null;
            this.backendUrl = this.config.backendUrl || '';
            this.apiKey = this.config.apiKey || '';
            this.agentName = this.config.agentName || 'RAG Agent';
            this.defaultChatTitle = this.config.defaultChatTitle || 'New Chat';
            this.showConfigPrompt = this.config.showConfigPrompt !== false && !this.backendUrl;
            this.sidebarWidth = localStorage.getItem('sidebarWidth') || '250px';
            this.sidebarHidden = localStorage.getItem('sidebarHidden') === 'true';
            this.isDarkMode = localStorage.getItem('isDarkMode') === 'true';
            this.markdownEnabled = localStorage.getItem('markdownEnabled') !== 'false';
            this.uid = 'rag-' + Math.random().toString(36).substr(2, 9);
            this.isResizing = false;
            
            // Configure marked.js if available
            if (typeof marked !== 'undefined') {
                marked.setOptions({
                    breaks: true,
                    gfm: true,
                    headerIds: false,
                    mangle: false
                });
            }
            
            this.createUI(container);
            this.applySavedSettings();
            
            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'd') this.toggleDarkMode();
            });
            
            if (this.showConfigPrompt) this.showConfigWindow();
            this.initChats();
            
            // Emit widget created event
            this.emit('widget-created', { widget: this });
        }

        // Event System
        on(eventType, callback) {
            if (!this.eventListeners[eventType]) this.eventListeners[eventType] = [];
            this.eventListeners[eventType].push(callback);
            return this;
        }

        off(eventType, callback) {
            if (!this.eventListeners[eventType]) return this;
            this.eventListeners[eventType] = this.eventListeners[eventType].filter(cb => cb !== callback);
            return this;
        }

        emit(eventType, data = {}) {
            const event = { type: eventType, timestamp: Date.now(), ...data };
            if (this.eventListeners[eventType]) {
                this.eventListeners[eventType].forEach(callback => {
                    try { callback(event); } catch (e) { console.error('Event listener error:', e); }
                });
            }
            return event;
        }

        // Stream redirection for artifacts
        setStreamTarget(target) {
            this.streamTarget = target;
            return this;
        }

        clearStreamTarget() {
            this.streamTarget = null;
            return this;
        }

        createUI(container) {
            container.style.display = 'flex';
            container.style.width = '100%';
            container.style.height = '100%';
            container.innerHTML = `
                <div class="rag-sidebar" id="sidebar-${this.uid}">
                    <div class="resize-handle" id="resize-handle-${this.uid}"></div>
                    <div class="rag-sidebar-header">
                        <span>Chats</span>
                        <button id="new-chat-btn-${this.uid}">New Chat</button>
                    </div>
                    <div class="rag-chat-list" id="chat-list-${this.uid}"></div>
                </div>
                <div class="rag-main-content" style="flex: 1; display: flex; flex-direction: column; min-width: 0;">
                    <div class="rag-header">
                        <div class="rag-header-left">
                            <button class="sidebar-toggle" id="sidebar-toggle-${this.uid}">
                                ${this.sidebarHidden ? '☰' : '←'}
                            </button>
                            <div class="rag-agent-name">${this.agentName}</div>
                        </div>
                        <div class="rag-header-right">
                            <div class="toggle-group">
                                <label class="theme-switch">
                                    <input type="checkbox" id="theme-toggle-${this.uid}" ${this.isDarkMode ? 'checked' : ''}>
                                    <span class="theme-slider"></span>
                                </label>
                                <span class="theme-label">${this.isDarkMode ? 'Dark' : 'Light'}</span>
                            </div>
                            <div class="toggle-group">
                                <label class="markdown-switch">
                                    <input type="checkbox" id="markdown-toggle-${this.uid}" ${this.markdownEnabled ? 'checked' : ''}>
                                    <span class="markdown-slider"></span>
                                </label>
                                <span class="markdown-label">${this.markdownEnabled ? 'MD' : 'Text'}</span>
                            </div>
                        </div>
                    </div>
                    <div class="rag-chat-container" id="chat-container-${this.uid}" style="flex: 1; overflow-y: auto;"></div>
                    <div class="rag-input-container">
                        <form class="rag-input-form">
                            <textarea id="query-${this.uid}" placeholder="${this.getPlaceholderText()}" rows="1"></textarea>
                            <button type="button" id="send-btn-${this.uid}">Send</button>
                        </form>
                    </div>
                </div>`;
            
            // Get DOM elements
            this.chatContainer = document.getElementById(`chat-container-${this.uid}`);
            this.chatList = document.getElementById(`chat-list-${this.uid}`);
            this.queryInput = document.getElementById(`query-${this.uid}`);
            this.sendBtn = document.getElementById(`send-btn-${this.uid}`);
            this.newChatBtn = document.getElementById(`new-chat-btn-${this.uid}`);
            this.sidebar = document.getElementById(`sidebar-${this.uid}`);
            this.sidebarToggle = document.getElementById(`sidebar-toggle-${this.uid}`);
            this.resizeHandle = document.getElementById(`resize-handle-${this.uid}`);
            this.themeToggle = document.getElementById(`theme-toggle-${this.uid}`);
            this.markdownToggle = document.getElementById(`markdown-toggle-${this.uid}`);
            this.themeLabel = document.querySelector('.theme-label');
            this.markdownLabel = document.querySelector('.markdown-label');
            
            // Event listeners
            this.sendBtn.addEventListener('click', () => this.handleSubmit());
            this.queryInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSubmit();
                }
            });
            this.newChatBtn.addEventListener('click', () => this.startNewChat());
            this.sidebarToggle.addEventListener('click', () => this.toggleSidebar());
            this.themeToggle.addEventListener('change', () => this.toggleDarkMode());
            this.markdownToggle.addEventListener('change', () => this.toggleMarkdown());
            
            this.setupResize();
            
            // Auto-resize textarea
            this.queryInput.addEventListener('input', () => {
                this.queryInput.style.height = 'auto';
                this.queryInput.style.height = this.queryInput.scrollHeight + 'px';
            });
        }

        getPlaceholderText() {
            return this.markdownEnabled ? "Type your message (markdown supported)..." : "Type your message...";
        }

        setupResize() {
            this.resizeHandle.addEventListener('mousedown', (e) => {
                this.isResizing = true;
                document.addEventListener('mousemove', this.handleResize.bind(this));
                document.addEventListener('mouseup', this.stopResize.bind(this));
                e.preventDefault();
            });
        }

        handleResize(e) {
            if (!this.isResizing) return;
            const newWidth = e.clientX;
            if (newWidth >= 200 && newWidth <= 500) {
                this.sidebar.style.width = newWidth + 'px';
                this.sidebarWidth = newWidth + 'px';
            }
        }

        stopResize() {
            this.isResizing = false;
            localStorage.setItem('sidebarWidth', this.sidebarWidth);
            document.removeEventListener('mousemove', this.handleResize);
            document.removeEventListener('mouseup', this.stopResize);
        }

        toggleSidebar() {
            const beforeState = this.sidebarHidden;
            this.emit('sidebar-toggle', { before: beforeState, after: !beforeState });
            
            this.sidebarHidden = !this.sidebarHidden;
            if (this.sidebarHidden) {
                this.sidebar.classList.add('hidden');
                this.sidebarToggle.textContent = '☰';
            } else {
                this.sidebar.classList.remove('hidden');
                this.sidebarToggle.textContent = '←';
            }
            localStorage.setItem('sidebarHidden', this.sidebarHidden);
        }

        toggleDarkMode() {
            const beforeState = this.isDarkMode;
            this.emit('theme-toggle', { before: beforeState, after: !beforeState });
            
            this.isDarkMode = !this.isDarkMode;
            const container = document.getElementById('container') || document.body;
            if (this.isDarkMode) {
                container.classList.add('rag-dark');
                this.themeLabel.textContent = 'Dark';
            } else {
                container.classList.remove('rag-dark');
                this.themeLabel.textContent = 'Light';
            }
            localStorage.setItem('isDarkMode', this.isDarkMode);
        }

        toggleMarkdown() {
            const beforeState = this.markdownEnabled;
            this.emit('markdown-toggle', { before: beforeState, after: !beforeState });
            
            this.markdownEnabled = !this.markdownEnabled;
            this.markdownLabel.textContent = this.markdownEnabled ? 'MD' : 'Text';
            this.queryInput.placeholder = this.getPlaceholderText();
            localStorage.setItem('markdownEnabled', this.markdownEnabled);
            this.renderMessages();
        }

        applySavedSettings() {
            if (!this.sidebarHidden) this.sidebar.style.width = this.sidebarWidth;
            if (this.sidebarHidden) {
                this.sidebar.classList.add('hidden');
                this.sidebarToggle.textContent = '☰';
            }
            if (this.isDarkMode) {
                const container = document.getElementById('container') || document.body;
                container.classList.add('rag-dark');
                this.themeLabel.textContent = 'Dark';
            }
            this.markdownLabel.textContent = this.markdownEnabled ? 'MD' : 'Text';
        }

        showConfigWindow() {
            const modal = document.createElement('div');
            modal.className = 'rag-config-modal';
            modal.innerHTML = `
                <div class="rag-config-content">
                    <h3>Configure Backend</h3>
                    <label>Backend URL</label>
                    <input id="backendUrl-${this.uid}" placeholder="https://your-backend.com/rag">
                    <label>API Key</label>
                    <input id="apiKey-${this.uid}" placeholder="API Key (optional)">
                    <button id="submit-config-${this.uid}">Submit</button>
                </div>`;
            document.body.appendChild(modal);
            
            document.getElementById(`submit-config-${this.uid}`).addEventListener('click', () => {
                this.backendUrl = document.getElementById(`backendUrl-${this.uid}`).value.trim();
                this.apiKey = document.getElementById(`apiKey-${this.uid}`).value.trim();
                document.body.removeChild(modal);
            });
        }

        initChats() {
            if (this.chats.length === 0) this.startNewChat();
            else if (!this.activeChatId || !this.chats.find(c => c.id === this.activeChatId)) {
                this.activeChatId = this.chats[0].id;
            }
            this.renderChatList();
            this.renderMessages();
        }

        saveChats() {
            localStorage.setItem('chats', JSON.stringify(this.chats));
            localStorage.setItem('activeChatId', this.activeChatId);
        }

        renderChatList() {
            this.chatList.innerHTML = '';
            this.chats.forEach(chat => {
                const item = document.createElement('div');
                item.className = `rag-chat-item ${chat.id === this.activeChatId ? 'active' : ''}`;
                item.textContent = chat.title;
                item.addEventListener('click', () => this.switchChat(chat.id));
                this.chatList.appendChild(item);
            });
        }

        renderMessages() {
            this.chatContainer.innerHTML = '';
            const activeChat = this.chats.find(c => c.id === this.activeChatId);
            if (activeChat) {
                activeChat.messages.forEach(msg => this.addMessage(msg.content, msg.role, false));
            }
            this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        }

        switchChat(id) {
            this.emit('chat-switch', { from: this.activeChatId, to: id });
            this.activeChatId = id;
            this.saveChats();
            this.renderChatList();
            this.renderMessages();
        }

        startNewChat() {
            const newId = Date.now().toString();
            const newTitle = `${this.defaultChatTitle} ${new Date().toLocaleTimeString()}`;
            this.emit('chat-create', { chatId: newId, title: newTitle });
            
            this.chats.push({ id: newId, title: newTitle, messages: [] });
            this.activeChatId = newId;
            this.saveChats();
            this.renderChatList();
            this.renderMessages();
        }

        handleSubmit() {
            const query = this.queryInput.value.trim();
            if (!query || !this.activeChatId) return;
            
            const event = this.emit('message-send', { message: query, chatId: this.activeChatId });
            if (event.preventDefault) return;
            
            this.addMessage(query, 'user');
            this.updateChatTitle(query);
            this.queryInput.value = '';
            this.queryInput.style.height = 'auto';
            
            if (this.backendUrl) this.streamFromBackend(query);
            else this.streamMockRAG();
        }

        addMessage(text, type, save = true) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('rag-message', type === 'user' ? 'rag-user-message' : 'rag-assistant-message');
            
            // Handle markdown rendering
            if (this.markdownEnabled && typeof marked !== 'undefined' && text.trim()) {
                try {
                    messageDiv.innerHTML = marked.parse(text);
                } catch (e) {
                    messageDiv.textContent = text;
                }
            } else {
                messageDiv.textContent = text;
            }
            
            this.chatContainer.appendChild(messageDiv);
            this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
            
            if (save) {
                const activeChat = this.chats.find(c => c.id === this.activeChatId);
                activeChat.messages.push({ role: type, content: text });
                this.saveChats();
            }
            
            return messageDiv;
        }

        updateChatTitle(query) {
            const activeChat = this.chats.find(c => c.id === this.activeChatId);
            if (activeChat.messages.length === 1) {
                const plainText = query.replace(/[#*`_~\[\]()]/g, '');
                activeChat.title = plainText.substring(0, 30) + (plainText.length > 30 ? '...' : '');
                this.saveChats();
                this.renderChatList();
            }
        }

        async streamFromBackend(query) {
            this.currentStreamId = Date.now().toString();
            const streamId = this.currentStreamId;
            
            this.emit('stream-start', { query, streamId, source: 'backend' });
            
            let targetElement = this.streamTarget || this.addMessage('', 'assistant');
            
            try {
                const headers = { 'Content-Type': 'application/json' };
                if (this.apiKey) headers['Authorization'] = `Bearer ${this.apiKey}`;
                
                const response = await fetch(this.backendUrl, {
                    method: 'POST',
                    headers,
                    body: JSON.stringify({ query })
                });
                
                if (!response.ok) throw new Error('Backend request failed');
                
                const reader = response.body.getReader();
                let fullText = '';
                
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    
                    const chunkText = new TextDecoder().decode(value);
                    fullText += chunkText;
                    
                    this.emit('stream-chunk', { chunk: chunkText, fullText, streamId });
                    
                    // Update content
                    if (this.markdownEnabled && typeof marked !== 'undefined') {
                        try {
                            if (this.streamTarget) {
                                this.streamTarget.innerHTML = marked.parse(fullText);
                            } else {
                                targetElement.innerHTML = marked.parse(fullText);
                            }
                        } catch (e) {
                            if (this.streamTarget) {
                                this.streamTarget.textContent = fullText;
                            } else {
                                targetElement.textContent = fullText;
                            }
                        }
                    } else {
                        if (this.streamTarget) {
                            this.streamTarget.textContent = fullText;
                        } else {
                            targetElement.textContent = fullText;
                        }
                    }
                    
                    if (!this.streamTarget) {
                        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
                    }
                }
                
                // Save to chat if not redirected
                if (!this.streamTarget) {
                    const activeChat = this.chats.find(c => c.id === this.activeChatId);
                    activeChat.messages[activeChat.messages.length - 1].content = fullText;
                    this.saveChats();
                }
                
                this.emit('stream-end', { fullText, streamId, source: 'backend', success: true });
                
            } catch (error) {
                this.emit('stream-error', { error: error.message, streamId, source: 'backend' });
                
                if (this.streamTarget) {
                    this.streamTarget.textContent = `Error: ${error.message}. Using mock response.`;
                } else {
                    targetElement.textContent = `Error: ${error.message}. Using mock response.`;
                }
                this.streamMockRAG(targetElement);
            } finally {
                this.currentStreamId = null;
            }
        }

        async streamMockRAG(existingDiv = null) {
            this.currentStreamId = this.currentStreamId || Date.now().toString();
            const streamId = this.currentStreamId;
            
            this.emit('stream-start', { streamId, source: 'mock' });
            
            let targetElement = this.streamTarget || existingDiv || this.addMessage('', 'assistant');
            
            const mockTexts = [
                `# RAG Response\n\n**Markdown** is fully supported!\n\n## Features:\n- Lists work\n- **Bold** and *italic*\n- \`code blocks\`\n\n\`\`\`js\nconsole.log("Hello!");\n\`\`\``,
                `## Assistant Reply\n\nI can help with:\n1. Document analysis\n2. Code generation\n3. Q&A responses\n\n> This is a blockquote\n\n**Ready to assist!**`,
                `### Mock Data\n\nStreaming **markdown** response:\n\n| Feature | Status |\n|---------|--------|\n| Markdown | ✅ |\n| Dark Mode | ✅ |\n| Resize | ✅ |`
            ];
            
            const text = mockTexts[Math.floor(Math.random() * mockTexts.length)];
            const words = text.split(' ');
            let fullText = '';
            
            for (let word of words) {
                await new Promise(r => setTimeout(r, 100));
                fullText += word + ' ';
                
                this.emit('stream-chunk', { chunk: word + ' ', fullText, streamId });
                
                if (this.markdownEnabled && typeof marked !== 'undefined') {
                    try {
                        if (this.streamTarget) {
                            this.streamTarget.innerHTML = marked.parse(fullText);
                        } else {
                            targetElement.innerHTML = marked.parse(fullText);
                        }
                    } catch (e) {
                        if (this.streamTarget) {
                            this.streamTarget.textContent = fullText;
                        } else {
                            targetElement.textContent = fullText;
                        }
                    }
                } else {
                    if (this.streamTarget) {
                        this.streamTarget.textContent = fullText;
                    } else {
                        targetElement.textContent = fullText;
                    }
                }
                
                if (!this.streamTarget) {
                    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
                }
            }
            
            // Save to chat if not redirected
            if (!this.streamTarget) {
                const activeChat = this.chats.find(c => c.id === this.activeChatId);
                activeChat.messages[activeChat.messages.length - 1].content = fullText;
                this.saveChats();
            }
            
            this.emit('stream-end', { fullText, streamId, source: 'mock', success: true });
            this.currentStreamId = null;
        }

        // Public API methods
        sendMessage(message) {
            this.queryInput.value = message;
            this.handleSubmit();
            return this;
        }

        getCurrentChat() {
            return this.chats.find(c => c.id === this.activeChatId);
        }

        getAllChats() {
            return [...this.chats];
        }

        addCustomMessage(content, type = 'assistant') {
            return this.addMessage(content, type);
        }

        stopStream() {
            if (this.currentStreamId) {
                this.emit('stream-stop', { streamId: this.currentStreamId });
                this.currentStreamId = null;
            }
            return this;
        }
    }

    globalThis.customdhx.RagWidget = RagWidget;
})();
