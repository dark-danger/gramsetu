// ChatGPT Minimalist Interface - Qwen 2.5 Universal Intelligence Engine
// Pure English UI • Zero Clutter • Real-time Streaming • Multi-turn Context & Rich Markdown

const APP_STATE = {
  activeModel: 'qwen2.5:1.5b',
  engineMode: 'ollama', // 'ollama' or 'offline'
  isListening: false,
  speechRate: 0.95,
  conversationHistory: [] // Array of { role: 'user'|'assistant', content: string }
};

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
  initOllamaProbe();
  initSpeechEngine();
});

// Auto-detect local Ollama & prioritize general Qwen 2.5 instruct over coder
async function initOllamaProbe() {
  const modelLabel = document.getElementById('activeModelLabel');
  try {
    const res = await fetch('/api/tags', { cache: 'no-store' }).catch(() =>
      fetch('http://localhost:11434/api/tags', { cache: 'no-store' })
    );

    if (res && res.ok) {
      const data = await res.json();
      const models = data.models || [];
      // Prioritize general instruct model if available
      const generalQwen = models.find(m => m.name.includes('qwen2.5:1.5b') || m.name.includes('qwen2.5:3b') || m.name.includes('qwen2.5:latest'));
      const anyQwen = models.find(m => m.name.toLowerCase().includes('qwen'));
      
      if (generalQwen) {
        APP_STATE.activeModel = generalQwen.name;
      } else if (anyQwen) {
        APP_STATE.activeModel = anyQwen.name;
      }
      
      APP_STATE.engineMode = 'ollama';
      if (modelLabel) modelLabel.innerText = 'GRAM Setu (Qwen 2.5)';
    } else {
      throw new Error();
    }
  } catch (err) {
    APP_STATE.engineMode = 'offline';
    if (modelLabel) modelLabel.innerText = 'GRAM Setu (Offline)';
  }
}

// Model dropdown menu
function toggleModelMenu() {
  const menu = document.getElementById('modelMenu');
  if (menu) menu.classList.toggle('show');
}

function setModel(mode) {
  APP_STATE.engineMode = mode;
  const menu = document.getElementById('modelMenu');
  if (menu) menu.classList.remove('show');

  const modelLabel = document.getElementById('activeModelLabel');
  if (mode === 'ollama') {
    if (modelLabel) modelLabel.innerText = 'GRAM Setu (Qwen 2.5)';
  } else {
    if (modelLabel) modelLabel.innerText = 'GRAM Setu (Offline)';
  }
}

// Close model menu when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.model-pill-wrapper')) {
    document.getElementById('modelMenu')?.classList.remove('show');
  }
});

// Sidebar Toggle
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (window.innerWidth <= 768) {
    sidebar.classList.toggle('open');
  } else {
    sidebar.classList.toggle('collapsed');
  }
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

async function handleSend() {
  const input = document.getElementById('chatInput');
  if (!input) return;
  const prompt = input.value.trim();
  if (!prompt) return;

  // Hide Empty Hero, Show Message Feed
  const hero = document.getElementById('emptyHero');
  const feed = document.getElementById('messagesFeed');
  if (hero) hero.style.display = 'none';
  if (feed) feed.style.display = 'flex';

  input.value = '';
  input.style.height = 'auto';

  // Append User Message to UI & History
  appendUserMessage(prompt);
  APP_STATE.conversationHistory.push({ role: 'user', content: prompt });

  // Append Assistant Message placeholder
  const assistantBubble = appendAssistantMessage('Thinking...');
  const textEl = assistantBubble.querySelector('.assistant-message-text');

  try {
    if (APP_STATE.engineMode === 'ollama') {
      await streamFromOllama(prompt, textEl);
    } else {
      streamFromOfflineKnowledge(prompt, textEl);
    }
  } catch (err) {
    console.warn('Ollama streaming error, falling back to Offline Knowledge:', err);
    streamFromOfflineKnowledge(prompt, textEl);
  }
}

function appendUserMessage(text) {
  const feed = document.getElementById('messagesFeed');
  const row = document.createElement('div');
  row.className = 'message-row user-message-row';
  row.innerHTML = `<div class="user-message-pill">${escapeHTML(text)}</div>`;
  feed.appendChild(row);
  scrollToBottom();
}

function appendAssistantMessage(initialText) {
  const feed = document.getElementById('messagesFeed');
  const row = document.createElement('div');
  row.className = 'message-row assistant-message-row';
  row.innerHTML = `
    <div class="assistant-avatar-circle">✦</div>
    <div class="assistant-message-content">
      <div class="assistant-message-text">${renderMarkdownHTML(initialText)}</div>
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

// ==================== STREAMING FROM OLLAMA & OFFLINE RAG ====================
async function streamFromOllama(prompt, textEl) {
  textEl.innerHTML = '';

  // Extract multi-turn context summary from recent conversation history
  const recentTurns = APP_STATE.conversationHistory.slice(-8);
  const contextStrings = recentTurns.map(t => `${t.role}: ${t.content}`).join(' | ');

  // Query offline RAG with history context
  const matched = searchOfflineKnowledge(prompt, contextStrings);
  let groundTruth = '';
  if (matched) {
    groundTruth = `\n\n[Verified Reference Knowledge]:\n${matched.response}\n\n`;
  }

  const systemPrompt = `You are "GRAM Setu", a universal, master-level AI assistant powered by Qwen 2.5 capable of answering questions across all domains: Science, Technology, Programming (Python, JavaScript, C++, Arduino, SQL, Web Dev), Mathematics, Logic, Business, Formal Writing & Letters, Education, Agriculture, Government Schemes, Health/First-Aid, Daily Life, and General Knowledge.

Universal Guidelines:
1. Answer every question directly, thoroughly, and comprehensively with practical step-by-step guidance, explanations, or code examples.
2. Understand queries fluently in English, Hindi, and Hinglish (Romanized Hindi). E.g. "mosam / mausam" = weather/season, "gehu" = wheat, "kheti / ugana" = farming/cultivation, "dhan" = rice/paddy, "khad" = fertilizer, "bimari / keeda" = disease / pest, "yojna" = government scheme, "hisab/nap" = calculation/measurement.
3. Maintain active context from previous turns in this conversation.
4. Format all responses cleanly in English using bold headings, numbered steps, bullet points, and code blocks where applicable.
5. If reference data is provided, incorporate it accurately for exact facts, timings, and dosages.`;

  // Build multi-turn chat prompt formatted for Qwen 2.5 ChatML
  let fullPrompt = `<|im_start|>system\n${systemPrompt}${groundTruth}<|im_end|>\n`;
  for (let i = 0; i < recentTurns.length - 1; i++) {
    const turn = recentTurns[i];
    fullPrompt += `<|im_start|>${turn.role}\n${turn.content}<|im_end|>\n`;
  }
  fullPrompt += `<|im_start|>user\n${prompt}<|im_end|>\n<|im_start|>assistant\n`;

  const reqBody = {
    model: APP_STATE.activeModel,
    prompt: fullPrompt,
    stream: true,
    options: {
      temperature: 0.4,
      num_predict: 1200
    }
  };

  const response = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reqBody)
  }).catch(() => fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reqBody)
  }));

  if (!response || !response.ok) {
    throw new Error('Local Ollama fetch error');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let fullOutput = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n').filter(l => l.trim().length > 0);
    for (const line of lines) {
      try {
        const json = JSON.parse(line);
        if (json.response) {
          fullOutput += json.response;
          textEl.innerHTML = renderMarkdownHTML(fullOutput);
          scrollToBottom();
        }
      } catch (e) {}
    }
  }

  // Record assistant response in history
  APP_STATE.conversationHistory.push({ role: 'assistant', content: fullOutput });
}

function streamFromOfflineKnowledge(prompt, textEl) {
  const recentTurns = APP_STATE.conversationHistory.slice(-4);
  const contextStrings = recentTurns.map(t => `${t.role}: ${t.content}`).join(' | ');

  const match = searchOfflineKnowledge(prompt, contextStrings);
  let finalAnswer = '';

  if (match) {
    finalAnswer = match.response;
  } else {
    // Intelligent Universal Offline Response
    finalAnswer = `💡 **Response to:** *"${prompt}"*\n\n1. **Overview & Analysis:**\n   • Your request involves key principles of structured reasoning and practical implementation.\n\n2. **Recommended Action Steps:**\n   • **Step 1:** Verify the prerequisite requirements or foundational concepts.\n   • **Step 2:** Follow standardized best practices and maintain clear execution checkpoints.\n   • **Step 3:** For specialized domain assistance, consult official reference documentation or local resource centers.\n\n3. **Quick Support Helplines & Links:**\n   • National Kisan Call Center: **1800-180-1551** | National Emergency: **112** | Ayushman Portal: \`beneficiary.nha.gov.in\``;
  }

  textEl.innerHTML = '';
  let index = 0;
  let accumulated = '';
  const timer = setInterval(() => {
    if (index < finalAnswer.length) {
      accumulated += finalAnswer[index];
      textEl.innerHTML = renderMarkdownHTML(accumulated);
      index++;
      scrollToBottom();
    } else {
      clearInterval(timer);
      APP_STATE.conversationHistory.push({ role: 'assistant', content: finalAnswer });
    }
  }, 6);
}

// ==================== CLEAN MARKDOWN TO HTML RENDERER ====================
function renderMarkdownHTML(text) {
  if (!text) return '';
  
  let out = escapeHTML(text);

  // Fenced Code Blocks (```lang ... ```)
  out = out.replace(/```(\w*)\n([\s\S]*?)```/g, function(match, lang, code) {
    return `<pre class="md-code-block"><div class="code-header"><span>${lang || 'CODE'}</span></div><code>${code.trim()}</code></pre>`;
  });

  // Headers (### Header)
  out = out.replace(/^### (.*$)/gim, '<h4 class="md-heading">$1</h4>');
  out = out.replace(/^## (.*$)/gim, '<h3 class="md-heading">$1</h3>');
  out = out.replace(/^# (.*$)/gim, '<h2 class="md-heading">$1</h2>');

  // Bold (**bold**)
  out = out.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // Italic (*italic*)
  out = out.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // Inline Code (`code`)
  out = out.replace(/`([^`]+)`/g, '<code class="md-code">$1</code>');

  // Bullet items (• or - ) with optional indentation
  out = out.replace(/^\s*[•\-]\s+(.*$)/gim, '<div class="md-bullet"><span class="md-bullet-dot">•</span><span>$1</span></div>');

  // Numbered list items (1. Item) with optional indentation
  out = out.replace(/^\s*(\d+)\.\s+(.*$)/gim, '<div class="md-num-item"><span class="md-num-badge">$1.</span><span>$2</span></div>');

  // Line breaks & Spacers
  out = out.replace(/\n\n+/g, '<div class="md-spacer"></div>');
  out = out.replace(/\n/g, '<br>');

  return out;
}

// ==================== VOICE INPUT & SPEECH ====================
let speechRecognition = null;

function initSpeechEngine() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRec) {
    speechRecognition = new SpeechRec();
    speechRecognition.lang = 'en-IN';
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
    .replace(/🌾|🏛️|🩺|📐|🐄|🌱|🚨|⚠️|❌|✅|💧|🔥|⚡|💻|📝|💡/g, '')
    .replace(/\n+/g, '. ');

  const utterance = new SpeechSynthesisUtterance(clean);
  utterance.lang = 'en-IN';
  utterance.rate = APP_STATE.speechRate;

  const voices = window.speechSynthesis.getVoices();
  const englishVoice = voices.find(v => v.lang.includes('en'));
  if (englishVoice) utterance.voice = englishVoice;

  window.speechSynthesis.speak(utterance);
}

// ==================== TEXTAREA AUTO-RESIZE & KEY EVENTS ====================
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

// Utility: HTML escaper
function escapeHTML(str) {
  return str.replace(/[&<>'"]/g, tag => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[tag] || tag));
}
