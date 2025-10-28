(function () {
    globalThis.customdhx = globalThis.customdhx || {};
    
    const css = `
        .rag-sidebar {
            width: 250px;
            min-width: 200px;
            max-width: 500px;
            background: #f5f5f5;
            border-right: 1px solid #e0e0e0;
            display: flex;
            flex-direction: column;
            transition: width 0.2s ease;
        }

        .rag-sidebar.hidden {
            display: none;
        }

        .rag-sidebar-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px;
            font-weight: 600;
        }

        .rag-chat-list {
            flex: 1;
            overflow-y: auto;
        }

        .rag-chat-item {
            padding: 10px 12px;
            cursor: pointer;
        }

        .rag-chat-item.active {
            background: #dfe9ff;
            font-weight: 600;
        }

        .rag-main-content {
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .rag-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }

        .rag-status {
            padding: 6px 12px;
            background: #eef3ff;
            border-bottom: 1px solid #d0d7ff;
            font-size: 13px;
            color: #3b4a8a;
        }

        .rag-chat-container {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .rag-input-container {
            border-top: 1px solid #e0e0e0;
            padding: 12px;
        }

        .rag-input-form {
            display: flex;
            gap: 8px;
        }

        .rag-input-form textarea {
            flex: 1;
            resize: none;
            padding: 10px;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
        }

        .rag-input-form button {
            padding: 10px 16px;
            border: none;
            border-radius: 6px;
            background: #2563eb;
            color: #fff;
            cursor: pointer;
        }

        .rag-message {
            padding: 12px;
            border-radius: 8px;
            line-height: 1.5;
            white-space: pre-wrap;
        }

        .rag-user-message {
            align-self: flex-end;
            background: #2563eb;
            color: #fff;
        }

        .rag-assistant-message {
            align-self: flex-start;
            background: #f1f5f9;
            color: #111827;
        }

        .rag-dark .rag-main-content {
            background: #0f172a;
            color: #e2e8f0;
        }

        .rag-dark .rag-sidebar {
            background: #1e293b;
            border-right-color: #334155;
        }

        .rag-dark .rag-chat-item.active {
            background: #334155;
        }

        .rag-dark .rag-input-form textarea {
            background: #1f2937;
            color: #e5e7eb;
            border-color: #374151;
        }

        .rag-dark .rag-assistant-message {
            background: #1f2937;
            color: #e2e8f0;
        }
    `;
    
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
            this.agentName = this.config.agentName || 'Conversation Summarizer';
            this.defaultChatTitle = this.config.defaultChatTitle || 'New Chat';
            this.showConfigPrompt = this.config.showConfigPrompt !== false && !this.backendUrl;
            this.sidebarWidth = localStorage.getItem('sidebarWidth') || '250px';
            this.sidebarHidden = localStorage.getItem('sidebarHidden') === 'true';
            this.isDarkMode = localStorage.getItem('isDarkMode') === 'true';
            this.markdownEnabled = localStorage.getItem('markdownEnabled') !== 'false';
            this.uid = 'rag-' + Math.random().toString(36).substr(2, 9);
            this.isResizing = false;
            this.statusElement = null;
            
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
                    <div class="rag-status" id="status-${this.uid}" style="display: none;"></div>
                    <div class="rag-chat-container" id="chat-container-${this.uid}"></div>
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
            this.statusElement = document.getElementById(`status-${this.uid}`);
            
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

        showConfigWindow() {
            const modal = document.createElement('div');
            modal.className = 'rag-config-modal';
            modal.innerHTML = `
                <div class="rag-config-content">
                    <h3>Configure Summarization API</h3>
                    <label>Backend URL</label>
                    <input id="backendUrl-${this.uid}" placeholder="http://localhost:8000" value="${this.backendUrl}">
                    <label>API Key (optional)</label>
                    <input id="apiKey-${this.uid}" placeholder="API Key" value="${this.apiKey}">
                    <label>Model Provider</label>
                    <select id="provider-${this.uid}">
                        <option value="ollama">Ollama</option>
                        <option value="bedrock">Bedrock</option>
                    </select>
                    <label>Model Name</label>
                    <input id="modelName-${this.uid}" placeholder="qwen2.5-coder:latest" value="qwen2.5-coder:latest">
                    <label>Stream Mode</label>
                    <select id="streamMode-${this.uid}">
                        <option value="incremental">Incremental</option>
                        <option value="batch">Batch</option>
                        <option value="realtime">Real-time</option>
                    </select>
                    <button id="submit-config-${this.uid}">Submit</button>
                </div>`;
            document.body.appendChild(modal);
            
            document.getElementById(`submit-config-${this.uid}`).addEventListener('click', () => {
                this.backendUrl = document.getElementById(`backendUrl-${this.uid}`).value.trim();
                this.apiKey = document.getElementById(`apiKey-${this.uid}`).value.trim();
                this.config.provider = document.getElementById(`provider-${this.uid}`).value;
                this.config.modelName = document.getElementById(`modelName-${this.uid}`).value;
                this.config.streamMode = document.getElementById(`streamMode-${this.uid}`).value;
                document.body.removeChild(modal);
            });
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

    // NEW: Add copy buttons to code blocks
    addCopyButtonsToCodeBlocks(element) {
        const codeBlocks = element.querySelectorAll('pre code');
        codeBlocks.forEach((codeBlock, index) => {
            const pre = codeBlock.parentElement;
            if (pre.querySelector('.copy-btn')) return; // Already has copy button
            
            // Add terminal styling classes
            pre.classList.add('terminal-block');
            codeBlock.classList.add('terminal-code');
            
            // Create copy button
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.innerHTML = '📋';
            copyBtn.title = 'Copy code';
            
            // Add copy functionality
            copyBtn.addEventListener('click', () => {
                const code = codeBlock.textContent;
                navigator.clipboard.writeText(code).then(() => {
                    copyBtn.innerHTML = '✅';
                    copyBtn.title = 'Copied!';
                    setTimeout(() => {
                        copyBtn.innerHTML = '📋';
                        copyBtn.title = 'Copy code';
                    }, 2000);
                }).catch(() => {
                    // Fallback for older browsers
                    const textarea = document.createElement('textarea');
                    textarea.value = code;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    copyBtn.innerHTML = '✅';
                    setTimeout(() => copyBtn.innerHTML = '📋', 2000);
                });
            });
            
            // Position button in top-right of code block
            pre.style.position = 'relative';
            pre.appendChild(copyBtn);
        });
    }

    addMessage(text, type, save = true) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('rag-message', type === 'user' ? 'rag-user-message' : 'rag-assistant-message');
        
        // Handle markdown rendering
        if (this.markdownEnabled && typeof marked !== 'undefined' && text.trim()) {
            try {
                messageDiv.innerHTML = marked.parse(text);
                // Add copy buttons to code blocks
                this.addCopyButtonsToCodeBlocks(messageDiv);
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

        // Build conversation context from chat history
        buildConversationContext(newQuery) {
            const activeChat = this.chats.find(c => c.id === this.activeChatId);
            const messages = activeChat ? [...activeChat.messages] : [];
            
            // Add the new query as a message
            messages.push({
                messageId: `msg_${Date.now()}`,
                text: newQuery,
                role: 'user',
                timestamp: new Date().toISOString()
            });
            
            return {
                conversationId: this.activeChatId || 'temp',
                title: activeChat?.title || 'New Conversation',
                messages: messages.map((msg, index) => ({
                    messageId: msg.messageId || `msg_${index}`,
                    text: msg.content || msg.text,
                    role: msg.role,
                    timestamp: msg.timestamp || new Date().toISOString()
                }))
            };
        }

        async streamFromBackend(query) {
            this.currentStreamId = Date.now().toString();
            const streamId = this.currentStreamId;
            
            this.emit('stream-start', { query, streamId, source: 'backend' });
            
            let targetElement = this.streamTarget || this.addMessage('', 'assistant');
            
            try {
                const headers = { 'Content-Type': 'application/json' };
                if (this.apiKey) headers['Authorization'] = `Bearer ${this.apiKey}`;
                
                // Prepare conversation context for the summarization API
                const conversationContext = this.buildConversationContext(query);
                
                // Validate context first
                const validation = await this.validateConversationContext(conversationContext);
                if (!validation.valid) {
                    throw new Error(`Invalid conversation context: ${validation.error}`);
                }
                
                const requestBody = {
                    conversation_context: conversationContext,
                    summarizer_config: {
                        provider: this.config.provider || "ollama",
                        model_name: this.config.modelName || "qwen2.5-coder:latest",
                        ollama_host: "https://devollama01.mdlxpoc.org/v1",
                        aws_region: "us-east-1"
                    },
                    stream_mode: this.config.streamMode || "incremental",
                    max_message_length: 1000,
                    include_diffs: true,
                    preserve_code_blocks: true
                };
                
                const response = await fetch(`${this.backendUrl}/stream/conversation`, {
                    method: 'POST',
                    headers,
                    body: JSON.stringify(requestBody)
                });
                
                if (!response.ok) throw new Error(`Backend request failed: ${response.status}`);
                
                const sessionId = response.headers.get('X-Session-ID');
                if (sessionId) {
                    this.emit('session-created', { sessionId, streamId });
                }
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';
                
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    
                    // Decode chunk and add to buffer
                    buffer += decoder.decode(value, { stream: true });
                    
                    // Process complete lines
                    const lines = buffer.split('\n');
                    buffer = lines.pop(); // Keep incomplete line in buffer
                    
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const jsonData = line.slice(6);
                                if (jsonData.trim()) {
                                    const chunk = JSON.parse(jsonData);
                                    
                                    this.emit('stream-chunk', { 
                                        chunk: chunk, 
                                        streamId,
                                        chunkType: chunk.chunk_type 
                                    });
                                    
                                    // Handle different chunk types
                                    await this.handleStreamChunk(chunk, targetElement);
                                }
                            } catch (e) {
                                console.warn('Failed to parse chunk:', line, e);
                            }
                        }
                    }
                }
                
                this.emit('stream-end', { 
                    streamId, 
                    source: 'backend', 
                    success: true 
                });
                
            } catch (error) {
                this.emit('stream-error', { 
                    error: error.message, 
                    streamId, 
                    source: 'backend' 
                });
                
                if (this.streamTarget) {
                    this.streamTarget.textContent = `Error: ${error.message}. Using mock response.`;
                } else {
                    targetElement.textContent = `Error: ${error.message}. Using mock response.`;
                }
                
                // Fallback to mock
                setTimeout(() => this.streamMockRAG(targetElement), 1000);
            } finally {
                this.currentStreamId = null;
                this.hideProcessingStatus();
            }
        }

        // Handle different chunk types from the streaming API
        async handleStreamChunk(chunk, targetElement) {
            switch (chunk.chunk_type) {
                case 'session_start':
                    this.showProcessingStatus('Starting summarization session...', chunk.metadata);
                    break;
                    
                case 'message_start':
                    this.showProcessingStatus(`Processing message ${chunk.message_id}...`, chunk.metadata);
                    break;
                    
                case 'content':
                case 'content_chunk':
                    // Append content to the target element
                    this.appendContent(chunk.content || '', targetElement);
                    break;
                    
                case 'realtime_content':
                    // Replace content for real-time streaming
                    this.replaceContent(chunk.content || '', targetElement);
                    break;
                    
                case 'batch_result':
                    // Handle batch processing results
                    const batchHeader = chunk.metadata?.position ? 
                        `\n\n**Message ${chunk.metadata.position}/${chunk.metadata.total}:**\n` : 
                        '\n\n**Processed Message:**\n';
                    this.appendContent(batchHeader + (chunk.content || ''), targetElement);
                    break;
                    
                case 'batch_processing':
                    this.showProcessingStatus(chunk.content || 'Processing batch...', chunk.metadata);
                    break;
                    
                case 'message_complete':
                    const stats = chunk.metadata;
                    const statusMsg = stats ? 
                        `Message completed (${stats.compression_ratio?.toFixed(1)}% compression, ${stats.tokens_saved} tokens saved)` :
                        'Message completed';
                    this.showProcessingStatus(statusMsg, chunk.metadata);
                    break;
                    
                case 'session_complete':
                    const sessionStats = chunk.metadata;
                    const completionMsg = sessionStats ? 
                        `Summarization complete! Processed ${sessionStats.total_processed} messages in ${sessionStats.processing_time?.toFixed(1)}s. Total tokens saved: ${sessionStats.tokens_saved}` :
                        'Summarization complete!';
                    this.showProcessingStatus(completionMsg, chunk.metadata);
                    this.finalizeContent(targetElement);
                    setTimeout(() => this.hideProcessingStatus(), 3000);
                    break;
                    
                case 'typing':
                    this.showTypingIndicator(chunk.message_id);
                    break;
                    
                case 'error':
                    throw new Error(chunk.content || 'Unknown streaming error');
                    
                default:
                    console.warn('Unknown chunk type:', chunk.chunk_type, chunk);
            }
        }
    }

        // Helper method to append content
        appendContent(content, targetElement) {
            if (!content) return;
            
            const currentContent = this.getElementText(targetElement);
            const newContent = currentContent + content;
            
            this.updateElementContent(newContent, targetElement);
            this.saveCurrentMessage(newContent);
        }

        // Helper method to replace content (for real-time streaming)
        replaceContent(content, targetElement) {
            this.updateElementContent(content, targetElement);
            this.saveCurrentMessage(content);
        }

        // Helper method to get current text content
        getElementText(element) {
            return element.textContent || '';
        }

        // Helper method to update element content with markdown support
        updateElementContent(content, targetElement) {
            if (this.markdownEnabled && typeof marked !== 'undefined' && content.trim()) {
                try {
                    targetElement.innerHTML = marked.parse(content);
                } catch (e) {
                    targetElement.textContent = content;
                }
            } else {
                targetElement.textContent = content;
            }
            
            if (!this.streamTarget) {
                this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
            }
        }

        // Helper method to save current message to chat
        saveCurrentMessage(content) {
            if (!this.streamTarget) {
                const activeChat = this.chats.find(c => c.id === this.activeChatId);
                if (activeChat && activeChat.messages.length > 0) {
                    activeChat.messages[activeChat.messages.length - 1].content = content;
                    this.saveChats();
                }
            }
        }

        // Helper method to show processing status
        showProcessingStatus(message, metadata) {
            if (this.statusElement) {
                this.statusElement.textContent = message;
                this.statusElement.style.display = 'block';
            }
            
            this.emit('processing-status', { message, metadata });
            console.log(`Status: ${message}`, metadata);
        }

        // Helper method to hide processing status
        hideProcessingStatus() {
            if (this.statusElement) {
                this.statusElement.style.display = 'none';
            }
        }

        // Helper method to show typing indicator
        showTypingIndicator(messageId) {
            this.showProcessingStatus(`Typing response for ${messageId}...`);
            this.emit('typing-indicator', { messageId });
        }

        // Helper method to finalize content
        finalizeContent(targetElement) {
            // Remove any temporary indicators, finalize formatting
            this.emit('content-finalized', { element: targetElement });
        }

        // Method to validate conversation context before sending
        async validateConversationContext(context) {
            try {
                const response = await fetch(`${this.backendUrl}/process/validate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(context)
                });
                
                if (response.ok) {
                    const validation = await response.json();
                    this.emit('context-validated', validation);
                    return validation;
                }
            } catch (error) {
                console.warn('Context validation failed:', error);
            }
            return { valid: false, error: 'Validation failed' };
        }

        // Method to monitor session status
        async monitorSessionStatus(sessionId) {
            try {
                const response = await fetch(`${this.backendUrl}/session/${sessionId}/status`);
                if (response.ok) {
                    const status = await response.json();
                    this.emit('session-status', status);
                    return status;
                }
            } catch (error) {
                console.warn('Failed to get session status:', error);
            }
            return null;
        }

        async streamMockRAG(existingDiv = null) {
            this.currentStreamId = this.currentStreamId || Date.now().toString();
            const streamId = this.currentStreamId;
            
            this.emit('stream-start', { streamId, source: 'mock' });
            
            let targetElement = this.streamTarget || existingDiv || this.addMessage('', 'assistant');
            
            const mockTexts = [
                `# Conversation Summary\n\n**Technical Discussion Analysis**\n\n## Key Points:\n- Thread safety implementation\n- Performance optimization strategies\n- **Code improvements** identified\n\n\`\`\`python\n# Example improvement\nqueue = collections.deque(maxlen=1000)\nwith threading.RLock():\n    queue.append(item)\n\`\`\`\n\n> Summary preserves semantic equivalence with 65% compression`,
                `## Summarization Results\n\n**Processing complete!**\n\n### Improvements Made:\n1. **Memory efficiency**: Reduced object allocation\n2. **Thread safety**: Implemented proper locking\n3. **Error handling**: Enhanced exception management\n\n| Metric | Value |\n|--------|-------|\n| Compression | 65% |\n| Time saved | 2.3s |\n| Tokens saved | 1,847 |\n\n**Ready for next conversation!**`,
                `### Mock Summarization Stream\n\n**Streaming response simulation:**\n\n- ✅ **Context analysis** complete\n- ✅ **Code extraction** finished\n- ✅ **Semantic preservation** verified\n\n\`\`\`javascript\n// Streaming chunk processed\nconst result = await processor.summarize(content);\nconsole.log("Compression:", result.ratio);\n\`\`\`\n\n> Real backend would provide actual conversation summarization`
            ];
            
            const reader = response.body.getReader();
            let fullText = '';
            
            this.showProcessingStatus('Mock processing conversation...');
            
            for (let word of words) {
                await new Promise(r => setTimeout(r, 100));
                fullText += word + ' ';
                
                const chunkText = new TextDecoder().decode(value);
                fullText += chunkText;
                
                this.emit('stream-chunk', { chunk: chunkText, fullText, streamId });
                
                // Update content
                if (this.markdownEnabled && typeof marked !== 'undefined') {
                    try {
                        if (this.streamTarget) {
                            this.streamTarget.innerHTML = marked.parse(fullText);
                            this.addCopyButtonsToCodeBlocks(this.streamTarget);
                        } else {
                            targetElement.innerHTML = marked.parse(fullText);
                            this.addCopyButtonsToCodeBlocks(targetElement);
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
                if (activeChat) {
                    activeChat.messages[activeChat.messages.length - 1].content = fullText;
                    this.saveChats();
                }
            }
            
            this.showProcessingStatus('Mock processing complete!');
            setTimeout(() => this.hideProcessingStatus(), 2000);
            
            this.emit('stream-end', { fullText, streamId, source: 'mock', success: true });
            this.currentStreamId = null;
        }
    }

    async streamMockRAG(existingDiv = null) {
        this.currentStreamId = this.currentStreamId || Date.now().toString();
        const streamId = this.currentStreamId;
        
        this.emit('stream-start', { streamId, source: 'mock' });
        
        let targetElement = this.streamTarget || existingDiv || this.addMessage('', 'assistant');
        
        const mockTexts = [
            `# RAG Response\n\n**Markdown** is fully supported!\n\n## Features:\n- Lists work\n- **Bold** and *italic*\n- \`inline code\`\n\n\`\`\`javascript\nconsole.log("Hello World!");\nconst data = { name: "RAG", version: "1.0" };\n\`\`\`\n\n\`\`\`python\ndef greet(name):\n    return f"Hello, {name}!"\n    \nprint(greet("User"))\n\`\`\``,
            `## Assistant Reply\n\nI can help with:\n1. Document analysis\n2. Code generation\n3. Q&A responses\n\n> This is a blockquote\n\n\`\`\`bash\nnpm install rag-widget\nnode server.js\n\`\`\`\n\n**Ready to assist!**`,
            `### Mock Data\n\nStreaming **markdown** response:\n\n| Feature | Status |\n|---------|--------|\n| Markdown | ✅ |\n| Dark Mode | ✅ |\n| Copy Code | ✅ |\n\n\`\`\`json\n{\n  "widget": "RAG",\n  "features": ["copy", "terminal", "streaming"],\n  "status": "active"\n}\n\`\`\``
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
                        this.addCopyButtonsToCodeBlocks(this.streamTarget);
                    } else {
                        targetElement.innerHTML = marked.parse(fullText);
                        this.addCopyButtonsToCodeBlocks(targetElement);
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

        // Configuration methods
        updateConfig(newConfig) {
            this.config = { ...this.config, ...newConfig };
            if (newConfig.backendUrl) this.backendUrl = newConfig.backendUrl;
            if (newConfig.apiKey) this.apiKey = newConfig.apiKey;
            if (newConfig.agentName) this.agentName = newConfig.agentName;
            this.emit('config-updated', { config: this.config });
            return this;
        }

        getConfig() {
            return { ...this.config };
        }

        // Chat management methods
        deleteChat(chatId) {
            const chatIndex = this.chats.findIndex(c => c.id === chatId);
            if (chatIndex === -1) return false;
            
            this.chats.splice(chatIndex, 1);
            
            if (this.activeChatId === chatId) {
                this.activeChatId = this.chats.length > 0 ? this.chats[0].id : null;
                if (!this.activeChatId) {
                    this.startNewChat();
                }
            }
            
            this.saveChats();
            this.renderChatList();
            this.renderMessages();
            this.emit('chat-deleted', { chatId });
            return true;
        }

        exportChat(chatId = null) {
            const targetId = chatId || this.activeChatId;
            const chat = this.chats.find(c => c.id === targetId);
            if (!chat) return null;
            
            return {
                id: chat.id,
                title: chat.title,
                messages: [...chat.messages],
                exportedAt: new Date().toISOString()
            };
        }

        exportAllChats() {
            return {
                chats: this.chats.map(chat => this.exportChat(chat.id)),
                exportedAt: new Date().toISOString(),
                version: '1.0'
            };
        }

        importChat(chatData) {
            if (!chatData || !chatData.messages) return false;
            
            const newId = chatData.id || Date.now().toString();
            const importedChat = {
                id: newId,
                title: chatData.title || 'Imported Chat',
                messages: chatData.messages
            };
            
            this.chats.push(importedChat);
            this.activeChatId = newId;
            this.saveChats();
            this.renderChatList();
            this.renderMessages();
            this.emit('chat-imported', { chatId: newId });
            return true;
        }

        // Utility methods
        clearAllChats() {
            this.chats = [];
            this.activeChatId = null;
            this.saveChats();
            this.startNewChat();
            this.emit('chats-cleared');
        }

        searchMessages(query) {
            const results = [];
            this.chats.forEach(chat => {
                chat.messages.forEach((msg, index) => {
                    if (msg.content.toLowerCase().includes(query.toLowerCase())) {
                        results.push({
                            chatId: chat.id,
                            chatTitle: chat.title,
                            messageIndex: index,
                            message: msg,
                            snippet: this.createSnippet(msg.content, query)
                        });
                    }
                });
            });
            return results;
        }

        createSnippet(text, query, maxLength = 100) {
            const index = text.toLowerCase().indexOf(query.toLowerCase());
            if (index === -1) return text.substring(0, maxLength) + '...';
            
            const start = Math.max(0, index - 30);
            const end = Math.min(text.length, index + query.length + 30);
            const snippet = text.substring(start, end);
            
            return (start > 0 ? '...' : '') + snippet + (end < text.length ? '...' : '');
        }

        // Event handler helpers
        addEventListeners() {
            // Listen to our own events for logging/debugging
            this.on('stream-chunk', (event) => {
                console.debug('Stream chunk:', event.chunkType, event.chunk);
            });
            
            this.on('stream-error', (event) => {
                console.error('Stream error:', event.error);
            });
            
            this.on('processing-status', (event) => {
                console.info('Processing:', event.message);
            });
        }

        // Cleanup method
        destroy() {
            // Remove event listeners
            this.eventListeners = {};
            
            // Stop any active streams
            this.stopStream();
            
            // Clean up DOM elements
            if (this.chatContainer) this.chatContainer.innerHTML = '';
            
            this.emit('widget-destroyed', { widget: this });
        }
    }
    
    // Inject CSS if not already present
    if (!document.getElementById('rag-widget-styles')) {
        const style = document.createElement('style');
        style.id = 'rag-widget-styles';
        style.textContent = css;
        document.head.appendChild(style);
    }
}

    // Export the widget class
    globalThis.customdhx.RagWidget = RagWidget;
})();
