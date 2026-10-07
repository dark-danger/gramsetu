// GramSetu AI - Frontend Orchestrator & UI Interface
// Features: Real-time Streaming, Safe Processing Metadata (Deep Think),
// Local SQLite Memory Sync, Local Voice STT/TTS, and Multimodal Visual Studio.

const APP_STATE = {
  activeModel: 'qwen2.5:3b',
  engineMode: 'ollama', // 'ollama' or 'offline'
  deepReasoningEnabled: true,
  isListening: false,
  speechRate: 0.95,
  sessionId: 'session_' + Date.now(),
  conversationHistory: []
};

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
  initOllamaProbe();
  initSpeechEngine();
  syncBackendMemories();
  updateReasoningToggleUI();
});

// Fetch active model list from Ollama
async function initOllamaProbe() {
  const modelLabel = document.getElementById('activeModelLabel');
  const sidebarStatus = document.getElementById('sidebarEngineStatus');
  try {
    const res = await fetch('/api/tags', { cache: 'no-store' });
    if (res && res.ok) {
      const data = await res.json();
      const models = data.models || [];
      const bestQwen = models.find(m => m.name.includes('qwen2.5:3b') || m.name.includes('qwen2.5:1.5b') || m.name.includes('llama3.2') || m.name.includes('qwen'));
      if (bestQwen) {
        APP_STATE.activeModel = bestQwen.name;
      }
      APP_STATE.engineMode = 'ollama';
      if (modelLabel) modelLabel.innerText = `GRAM Setu (${APP_STATE.activeModel})`;
      if (sidebarStatus) sidebarStatus.innerText = `${APP_STATE.activeModel} • Active`;
    }
  } catch (err) {
    if (modelLabel) modelLabel.innerText = 'GRAM Setu (Offline Engine)';
  }
}

// Toggle Deep Reasoning (Safe Pipeline Metadata) Panel
function toggleDeepReasoning() {
  APP_STATE.deepReasoningEnabled = !APP_STATE.deepReasoningEnabled;
  updateReasoningToggleUI();
}

function updateReasoningToggleUI() {
  const btn = document.getElementById('deepThinkToggleBtn');
  if (btn) {
    if (APP_STATE.deepReasoningEnabled) {
      btn.classList.add('active');
      btn.setAttribute('title', 'Pipeline Processing Metadata Active');
    } else {
      btn.classList.remove('active');
      btn.setAttribute('title', 'Fast Response Mode');
    }
  }
}

function toggleModelMenu() {
  const menu = document.getElementById('modelMenu');
  if (menu) menu.classList.toggle('show');
}

function setModel(mode) {
  APP_STATE.engineMode = mode;
  const menu = document.getElementById('modelMenu');
  if (menu) menu.classList.remove('show');
}

document.addEventListener('click', (e) => {
  if (!e.target.closest('.model-pill-wrapper')) {
    document.getElementById('modelMenu')?.classList.remove('show');
  }
});

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (window.innerWidth <= 768) {
    sidebar.classList.toggle('open');
  } else {
    sidebar.classList.toggle('collapsed');
  }
}

// ==================== MEMORY SYNC WITH SQLITE BACKEND ====================

async function syncBackendMemories() {
  try {
    const res = await fetch('/api/memories');
    if (res.ok) {
      const data = await res.json();
      renderMemoryFactsList(data.memories || []);
    }
  } catch (e) {}
}

async function openMemoryModal() {
  const modal = document.getElementById('memoryModal');
  if (!modal) return;

  try {
    const res = await fetch('/api/memories');
    if (res.ok) {
      const data = await res.json();
      const mems = data.memories || [];
      
      const loc = mems.find(m => m.key === 'location');
      const crop = mems.find(m => m.key === 'primary_crop');
      const land = mems.find(m => m.key === 'land_area');
      const lang = mems.find(m => m.key === 'preferred_language');

      document.getElementById('memoryLocationInput').value = loc ? loc.value : '';
      document.getElementById('memoryCropInput').value = crop ? crop.value : '';
      document.getElementById('memoryLandInput').value = land ? land.value : '';
      document.getElementById('memoryLangInput').value = lang ? lang.value.toLowerCase() : 'auto';

      renderMemoryFactsList(mems);
    }
  } catch (e) {}

  modal.classList.add('show');
}

function closeMemoryModal() {
  const modal = document.getElementById('memoryModal');
  if (modal) modal.classList.remove('show');
}

function renderMemoryFactsList(mems) {
  const container = document.getElementById('memoryListContainer');
  if (!container) return;

  if (!mems || mems.length === 0) {
    container.innerHTML = `<div style="color: var(--chatgpt-text-muted); font-size: 0.78rem; text-align: center; padding: 8px;">No stored memories yet. Talk to GramSetu to build profile!</div>`;
    return;
  }

  container.innerHTML = mems.map(m => `
    <div class="memory-item-row">
      <span class="memory-item-text">🧠 <strong>${escapeHTML(m.key)}:</strong> ${escapeHTML(m.value)} <em style="color:var(--chatgpt-text-muted); font-size:0.7rem;">(${escapeHTML(m.source)})</em></span>
    </div>
  `).join('');
}

async function clearAllMemories() {
  try {
    await fetch('/api/memories/clear', { method: 'POST' });
    syncBackendMemories();
    closeMemoryModal();
  } catch (e) {}
}

async function saveUserProfileMemory() {
  const loc = document.getElementById('memoryLocationInput').value.trim();
  const crop = document.getElementById('memoryCropInput').value.trim();
  const land = document.getElementById('memoryLandInput').value.trim();
  const lang = document.getElementById('memoryLangInput').value;

  if (loc) await fetch('/api/memories/save', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ key: 'location', value: loc, memory_type: 'location' }) });
  if (crop) await fetch('/api/memories/save', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ key: 'primary_crop', value: crop, memory_type: 'agriculture' }) });
  if (land) await fetch('/api/memories/save', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ key: 'land_area', value: land, memory_type: 'agriculture' }) });
  if (lang && lang !== 'auto') await fetch('/api/memories/save', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ key: 'preferred_language', value: lang, memory_type: 'preference' }) });

  syncBackendMemories();
  closeMemoryModal();
}

// ==================== CHAT ACTIONS & STREAMING ====================

function createNewChat() {
  const hero = document.getElementById('emptyHero');
  const feed = document.getElementById('messagesFeed');
  const input = document.getElementById('chatInput');

  if (hero) hero.style.display = 'flex';
  if (feed) {
    feed.innerHTML = '';
    feed.style.display = 'none';
  }
  if (input) {
    input.value = '';
    input.style.height = 'auto';
  }

  APP_STATE.sessionId = 'session_' + Date.now();
  APP_STATE.conversationHistory = [];
  if (window.innerWidth <= 768) {
    document.getElementById('sidebar')?.classList.remove('open');
  }
}

function sendSuggestion(text) {
  const input = document.getElementById('chatInput');
  if (input) {
    input.value = text;
    handleSend();
  }
}

function loadSamplePrompt(text) {
  sendSuggestion(text);
}

function loadChatSession(sessionId) {
  createNewChat();
}

function triggerImagePrompt() {
  const input = document.getElementById('chatInput');
  if (input) {
    if (!input.value.startsWith('/image')) {
      input.value = '/image ' + (input.value ? input.value : 'organic farming drip irrigation with healthy crops');
    }
    input.focus();
  }
}

async function handleSend() {
  const input = document.getElementById('chatInput');
  if (!input) return;
  const prompt = input.value.trim();
  if (!prompt) return;

  // 1. Hide Empty Hero, Show Message Feed
  const hero = document.getElementById('emptyHero');
  const feed = document.getElementById('messagesFeed');
  if (hero) hero.style.display = 'none';
  if (feed) feed.style.display = 'flex';

  input.value = '';
  input.style.height = 'auto';

  // 2. Append User Message
  appendUserMessage(prompt);
  APP_STATE.conversationHistory.push({ role: 'user', content: prompt });

  // 3. Append Assistant Placeholder
  const startTime = Date.now();
  const assistantBubble = appendAssistantMessage();
  const thinkContainer = assistantBubble.querySelector('.think-container');
  const thinkHeader = assistantBubble.querySelector('.think-header');
  const thinkContent = assistantBubble.querySelector('.think-content');
  const toolsBar = assistantBubble.querySelector('.agent-tools-bar');
  const textEl = assistantBubble.querySelector('.assistant-message-text');

  if (APP_STATE.deepReasoningEnabled) {
    thinkContainer.style.display = 'block';
  } else {
    thinkContainer.style.display = 'none';
  }

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: prompt,
        session_id: APP_STATE.sessionId,
        model: APP_STATE.activeModel
      })
    });

    if (!response.ok) {
      throw new Error(`Server status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let accumulatedText = '';
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop(); // Keep remaining incomplete line

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const packet = JSON.parse(line.trim());

          // 1. Handle Safe Processing Metadata
          if (packet.type === 'metadata' && packet.data) {
            renderProcessingMetadata(packet.data, thinkContent, toolsBar, assistantBubble);
          }

          // 2. Handle Stream Token
          if (packet.type === 'token') {
            accumulatedText += packet.token;
            textEl.innerHTML = renderMarkdownHTML(accumulatedText);
            scrollToBottom();
          }

          // 3. Handle Done Signal
          if (packet.type === 'done' && packet.final) {
            accumulatedText = packet.final;
            textEl.innerHTML = renderMarkdownHTML(accumulatedText);
          }
        } catch (e) {
          // If plain text token received
          accumulatedText += line;
          textEl.innerHTML = renderMarkdownHTML(accumulatedText);
        }
      }
    }

    // Finalize think header timer
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    if (thinkHeader) {
      thinkHeader.innerHTML = `
        <div class="think-title-group">
          <span>🧠 Processed in ${elapsed}s (Deterministic Pipeline)</span>
        </div>
        <svg class="think-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
      `;
    }

    APP_STATE.conversationHistory.push({ role: 'assistant', content: accumulatedText });
    syncBackendMemories();

  } catch (err) {
    console.error('Chat error:', err);
    textEl.innerHTML = `<span style="color:#ef4444;">Error communicating with local agent. Please check server.</span>`;
  }
}

// Render Safe Processing Metadata in Deep Think Panel
function renderProcessingMetadata(meta, thinkContentEl, toolsBarEl, messageBubble) {
  if (!thinkContentEl) return;

  const memKeys = Object.entries(meta.memories_used || {}).map(([k, v]) => `${k}=${v}`).join(', ');
  const toolsList = (meta.tools_executed || []).join(', ');

  thinkContentEl.innerHTML = `
    <div class="think-step-item">
      <span class="think-step-badge">INTENT</span>
      <span class="think-step-text"><strong>${escapeHTML(meta.intent)}</strong> (Tone: ${escapeHTML(meta.tone)})</span>
    </div>
    <div class="think-step-item">
      <span class="think-step-badge">LANGUAGE</span>
      <span class="think-step-text">Input: <strong>${escapeHTML(meta.input_language)}</strong> ➜ Requested Output: <strong>${escapeHTML(meta.output_language)}</strong></span>
    </div>
    ${memKeys ? `
    <div class="think-step-item">
      <span class="think-step-badge">MEMORY RETRIEVED</span>
      <span class="think-step-text"><em>${escapeHTML(memKeys)}</em></span>
    </div>` : ''}
    ${toolsList ? `
    <div class="think-step-item">
      <span class="think-step-badge">TOOLS EXECUTED</span>
      <span class="think-step-text"><strong>${escapeHTML(toolsList)}</strong></span>
    </div>` : ''}
    ${meta.rag_title ? `
    <div class="think-step-item">
      <span class="think-step-badge">KNOWLEDGE RAG</span>
      <span class="think-step-text">Verified Source: <strong>${escapeHTML(meta.rag_title)}</strong></span>
    </div>` : ''}
  `;

  // Render Tool Badges
  if (toolsBarEl && meta.tools_executed && meta.tools_executed.length > 0) {
    toolsBarEl.innerHTML = meta.tools_executed.map(t => `<div class="agent-tool-pill math">🛠️ ${escapeHTML(t)}</div>`).join('');
  }

  // Handle Image Card Display
  if (meta.image_payload && messageBubble) {
    const imgData = meta.image_payload;
    const cardEl = document.createElement('div');
    cardEl.className = 'ai-image-card';
    cardEl.innerHTML = `
      <div class="ai-image-preview-wrapper">
        <div class="ai-image-loading-overlay">
          <div class="spinner"></div>
          <div style="font-size: 0.8rem; color: #ec4899; font-weight: 500;">Synthesizing AI Visual...</div>
        </div>
        <img src="${imgData.image_url}" alt="${escapeHTML(imgData.prompt)}" onload="this.previousElementSibling.style.display='none'" onerror="this.previousElementSibling.innerHTML='<div style=\\'color:#ef4444;font-size:0.75rem;\\'>Image load error</div>'" />
      </div>
      <div class="ai-image-caption">
        <span class="ai-image-prompt-text">🎨 "${escapeHTML(imgData.prompt)}"</span>
        <div class="ai-image-btn-group">
          <a href="${imgData.image_url}" target="_blank" download="gramsetu_visual.jpg" class="ai-image-action-btn">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            <span>Download</span>
          </a>
        </div>
      </div>
    `;
    const contentBox = messageBubble.querySelector('.assistant-message-content');
    if (contentBox) contentBox.insertBefore(cardEl, contentBox.querySelector('.assistant-actions-toolbar'));
  }
}

// ==================== UI MESSAGE RENDERING ====================

function appendUserMessage(text) {
  const feed = document.getElementById('messagesFeed');
  const row = document.createElement('div');
  row.className = 'message-row user-message-row';
  row.innerHTML = `<div class="user-message-pill">${escapeHTML(text)}</div>`;
  feed.appendChild(row);
  scrollToBottom();
}

function appendAssistantMessage() {
  const feed = document.getElementById('messagesFeed');
  const row = document.createElement('div');
  row.className = 'message-row assistant-message-row';
  row.innerHTML = `
    <div class="assistant-avatar-circle">✦</div>
    <div class="assistant-message-content">
      
      <!-- Safe Deep Think Pipeline Metadata Accordion -->
      <div class="think-container" style="display: none;">
        <div class="think-header" onclick="toggleThinkBlock(this)">
          <div class="think-title-group">
            <span class="think-spinner"></span>
            <span>Processing Pipeline...</span>
          </div>
          <svg class="think-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="think-content">
          <!-- Populated from safe metadata -->
        </div>
      </div>

      <!-- Agent Tools Badges -->
      <div class="agent-tools-bar"></div>

      <!-- Main Assistant Message Stream -->
      <div class="assistant-message-text"><span style="color: var(--chatgpt-text-muted);">Thinking...</span></div>
      
      <div class="assistant-actions-toolbar">
        <button class="toolbar-btn" onclick="copyMessageText(this)" title="Copy text">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <span>Copy</span>
        </button>
        <button class="toolbar-btn" onclick="speakMessageAudio(this)" title="Read aloud">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
          <span>Listen</span>
        </button>
      </div>
    </div>
  `;
  feed.appendChild(row);
  scrollToBottom();
  return row;
}

function toggleThinkBlock(headerEl) {
  const container = headerEl.closest('.think-container');
  if (container) {
    container.classList.toggle('collapsed');
  }
}

function scrollToBottom() {
  const viewport = document.getElementById('chatViewport');
  if (viewport) {
    viewport.scrollTop = viewport.scrollHeight;
  }
}

function copyMessageText(btn) {
  const row = btn.closest('.assistant-message-row');
  const text = row.querySelector('.assistant-message-text').innerText;
  navigator.clipboard.writeText(text).then(() => {
    const span = btn.querySelector('span');
    if (span) {
      span.innerText = 'Copied!';
      setTimeout(() => span.innerText = 'Copy', 1500);
    }
  });
}

function speakMessageAudio(btn) {
  const row = btn.closest('.assistant-message-row');
  const text = row.querySelector('.assistant-message-text').innerText;
  playSpeechAudio(text);
}

// ==================== CLEAN MARKDOWN RENDERING ====================
function renderMarkdownHTML(text) {
  if (!text) return '';
  let out = escapeHTML(text);

  out = out.replace(/```(\w*)\n([\s\S]*?)```/g, function(match, lang, code) {
    return `<pre class="md-code-block"><div class="code-header"><span>${lang || 'CODE'}</span></div><code>${code.trim()}</code></pre>`;
  });

  out = out.replace(/^### (.*$)/gim, '<h4 class="md-heading">$1</h4>');
  out = out.replace(/^## (.*$)/gim, '<h3 class="md-heading">$1</h3>');
  out = out.replace(/^# (.*$)/gim, '<h2 class="md-heading">$1</h2>');

  out = out.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/\*(.*?)\*/g, '<em>$1</em>');
  out = out.replace(/`([^`]+)`/g, '<code class="md-code">$1</code>');

  out = out.replace(/^\s*[•\-]\s+(.*$)/gim, '<div class="md-bullet"><span class="md-bullet-dot">•</span><span>$1</span></div>');
  out = out.replace(/^\s*(\d+)\.\s+(.*$)/gim, '<div class="md-num-item"><span class="md-num-badge">$1.</span><span>$2</span></div>');

  out = out.replace(/\n\n+/g, '<div class="md-spacer"></div>');
  out = out.replace(/\n/g, '<br>');

  return out;
}

// ==================== LOCAL VOICE STT & TTS ====================
let speechRecognition = null;

function initSpeechEngine() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRec) {
    speechRecognition = new SpeechRec();
    speechRecognition.lang = 'hi-IN';
    speechRecognition.continuous = false;
    speechRecognition.interimResults = false;

    speechRecognition.onresult = (e) => {
      const text = e.results[0][0].transcript;
      const input = document.getElementById('chatInput');
      if (input) input.value = text;
      toggleMic(false);
      handleSend();
    };

    speechRecognition.onerror = () => toggleMic(false);
    speechRecognition.onend = () => toggleMic(false);
  }
}

function toggleMic(force) {
  const micBtn = document.getElementById('micBtn');
  const bar = document.getElementById('voiceListeningBar');

  if (force !== undefined) {
    APP_STATE.isListening = force;
  } else {
    APP_STATE.isListening = !APP_STATE.isListening;
  }

  if (APP_STATE.isListening) {
    micBtn?.classList.add('recording');
    if (bar) bar.style.display = 'flex';
    if (speechRecognition) {
      try { speechRecognition.start(); } catch (_) {}
    }
  } else {
    micBtn?.classList.remove('recording');
    if (bar) bar.style.display = 'none';
    if (speechRecognition) {
      try { speechRecognition.stop(); } catch (_) {}
    }
  }
}

function playSpeechAudio(text) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();

  const clean = text
    .replace(/[#*`_~]/g, '')
    .replace(/\[.*?\]\(.*?\)/g, '')
    .replace(/🌾|🏛️|🩺|📐|🐄|🌱|🚨|⚠️|❌|✅|💧|🔥|⚡|💻|📝|💡|🧠|🛠️|🎨/g, '')
    .replace(/\n+/g, '. ');

  const utterance = new SpeechSynthesisUtterance(clean);
  utterance.rate = APP_STATE.speechRate;

  const voices = window.speechSynthesis.getVoices();
  const indianVoice = voices.find(v => v.lang.includes('hi') || v.lang.includes('IN'));
  if (indianVoice) utterance.voice = indianVoice;

  window.speechSynthesis.speak(utterance);
}

function handleInputResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 150) + 'px';
}

function handleInputKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
}

function escapeHTML(str) {
  if (!str) return '';
  return String(str).replace(/[&<>'"]/g, tag => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[tag] || tag));
}
