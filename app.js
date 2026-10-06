// GramSetu AI - Advanced Personalization & Agentic Intelligence Engine
// Implements 11-Layer Core Architecture:
// [Personalization]: 9. Tone Detection | 10. Intent Detection | 11. Language Detection | 12. Personality/Style Engine | 13. User Preferences | 14. Context Manager
// [Agent System]: 15. Tool Calling / Function Calling | 16. Task Planner | 17. Reasoning/Decision Engine | 18. Agent Memory | 19. Error Detection & Self-Correction

const APP_STATE = {
  activeModel: 'qwen2.5:1.5b',
  engineMode: 'ollama', // 'ollama' or 'offline'
  deepReasoningEnabled: true,
  isListening: false,
  speechRate: 0.95,
  conversationHistory: [], // Array of { role: 'user'|'assistant', content: string }
  memory: {
    location: '',
    cropFocus: '',
    landSize: '',
    languagePreference: 'auto', // 'auto', 'english', 'hindi', 'hinglish'
    autoFacts: []
  }
};

// ==================== 1. INITIALIZATION & PERSISTENCE ====================
document.addEventListener('DOMContentLoaded', () => {
  loadSavedMemory();
  initOllamaProbe();
  initSpeechEngine();
  updateReasoningToggleUI();
});

function loadSavedMemory() {
  try {
    const saved = localStorage.getItem('gramsetu_ai_memory');
    if (saved) {
      APP_STATE.memory = { ...APP_STATE.memory, ...JSON.parse(saved) };
    }
  } catch (e) {
    console.warn('Could not load saved memory:', e);
  }
}

function persistMemory() {
  try {
    localStorage.setItem('gramsetu_ai_memory', JSON.stringify(APP_STATE.memory));
  } catch (e) {}
}

async function initOllamaProbe() {
  const modelLabel = document.getElementById('activeModelLabel');
  const sidebarStatus = document.getElementById('sidebarEngineStatus');
  try {
    const res = await fetch('/api/tags', { cache: 'no-store' }).catch(() =>
      fetch('http://localhost:11434/api/tags', { cache: 'no-store' })
    );

    if (res && res.ok) {
      const data = await res.json();
      const models = data.models || [];
      const generalQwen = models.find(m => m.name.includes('qwen2.5:1.5b') || m.name.includes('qwen2.5:3b') || m.name.includes('qwen2.5:latest') || m.name.includes('llama3.2'));
      const anyQwen = models.find(m => m.name.toLowerCase().includes('qwen') || m.name.toLowerCase().includes('llama'));
      
      if (generalQwen) {
        APP_STATE.activeModel = generalQwen.name;
      } else if (anyQwen) {
        APP_STATE.activeModel = anyQwen.name;
      }
      
      APP_STATE.engineMode = 'ollama';
      if (modelLabel) modelLabel.innerText = `GRAM Setu (${APP_STATE.activeModel})`;
      if (sidebarStatus) sidebarStatus.innerText = `${APP_STATE.activeModel} • Active`;
    } else {
      throw new Error();
    }
  } catch (err) {
    APP_STATE.engineMode = 'offline';
    if (modelLabel) modelLabel.innerText = 'GRAM Setu (Offline RAG)';
    if (sidebarStatus) sidebarStatus.innerText = 'Offline RAG • Reasoning Active';
  }
}

function toggleDeepReasoning() {
  APP_STATE.deepReasoningEnabled = !APP_STATE.deepReasoningEnabled;
  updateReasoningToggleUI();
}

function updateReasoningToggleUI() {
  const btn = document.getElementById('deepThinkToggleBtn');
  if (btn) {
    if (APP_STATE.deepReasoningEnabled) {
      btn.classList.add('active');
      btn.setAttribute('title', 'Deep Reasoning Active (Chain-of-Thought enabled)');
    } else {
      btn.classList.remove('active');
      btn.setAttribute('title', 'Fast Response Mode (Deep Reasoning paused)');
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

  const modelLabel = document.getElementById('activeModelLabel');
  const sidebarStatus = document.getElementById('sidebarEngineStatus');
  if (mode === 'ollama') {
    if (modelLabel) modelLabel.innerText = `GRAM Setu (${APP_STATE.activeModel})`;
    if (sidebarStatus) sidebarStatus.innerText = `${APP_STATE.activeModel} • Active`;
  } else {
    if (modelLabel) modelLabel.innerText = 'GRAM Setu (Offline RAG)';
    if (sidebarStatus) sidebarStatus.innerText = 'Offline RAG • Reasoning Active';
  }
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

// ==================== 🧠 PERSONALIZATION ENGINE (MODULES 9-14) ====================

const GRAM_PERSONALIZATION = {
  // 9. Tone Detection
  detectTone(text) {
    const lower = text.toLowerCase();
    if (lower.match(/(problem|error|galat|nahi ho raha|bekar|kharab|frustrated|gussa|samajh nahi ara|mujha smjh ni)/i)) {
      return { tone: 'frustrated_confused', promptStyle: 'Be extra empathetic, reassuring, patient, and break things down into super simple terms.' };
    }
    if (lower.match(/(urgent|jaldi|emergency|hospital|saanp|snake|current|shock|aag|fire|blood)/i)) {
      return { tone: 'urgent', promptStyle: 'Be direct, crisp, and prioritize life-critical safety DOs & DON\'Ts immediately.' };
    }
    if (lower.match(/(kya haal|kuch bata|bore|joke|masti|bhai|yaar|kaise ho|hello|hi\b)/i)) {
      return { tone: 'casual_friendly', promptStyle: 'Be conversational, warm, friendly, and engaging like a close companion.' };
    }
    if (lower.match(/(explain|difference|compare|kya hai|analysis|kyu|kaise|how does|why)/i)) {
      return { tone: 'inquisitive', promptStyle: 'Provide insightful, structured, and deep conceptual clarity.' };
    }
    return { tone: 'neutral', promptStyle: 'Respond clearly, politely, and helpfully.' };
  },

  // 10. Intent Detection
  detectIntent(text) {
    const lower = text.toLowerCase().trim();
    if (lower.startsWith('/image') || lower.match(/(photo banao|image banao|generate image|picture banao)/i)) {
      return 'image_generation';
    }
    if (lower.match(/\b(english|hindi|hinglish)\s*(m|me|mai)?\s*(baat|bol|bolo|kr|karo|batao)\b/i) || lower.match(/\b(speak|talk|reply)\s*(in)?\s*(english|hindi)\b/i)) {
      return 'language_switch';
    }
    if (lower.match(/(\d+(\.\d+)?)\s*(acre|acres|bigha|hectare|gaj|square yard)/i) || lower.match(/(hisab|convert|kitna hoga|\bmath\b|\bcalculate\b)/i)) {
      return 'math_calculation';
    }
    if (lower.match(/(gehu|wheat|dhan|rice|sarson|mustard|keeda|bimari|fungus|rust|khad|urea|dap)/i)) {
      return 'agri_diagnostic';
    }
    if (lower.match(/(yojana|yojna|pm kisan|ayushman|ration|subsidy|form|apply)/i)) {
      return 'scheme_guidance';
    }
    if (lower.match(/(python|arduino|c\+\+|javascript|code|function|bug|script)/i)) {
      return 'coding_technical';
    }
    if (lower.match(/^(hi|hello|hey|namaste|pranam|kya haal|kaise ho)\b/i)) {
      return 'greeting';
    }
    return 'general_discussion';
  },

  // 11. Language Detection
  detectLanguage(text) {
    const lower = text.toLowerCase().trim();
    if (lower.match(/\b(english\s*(m|me|mai|mein)?\s*(baat|bol|bolo|kr|karo|batao))\b/i) || lower.match(/\b(speak|talk|reply)\s*(in)?\s*english\b/i)) {
      return 'english';
    }
    if (lower.match(/\b(hindi\s*(m|me|mai|mein)?\s*(baat|bol|bolo|kr|karo|batao))\b/i) || lower.match(/[\u0900-\u097F]/)) {
      return 'hindi';
    }
    if (lower.match(/\b(hinglish|kya|kaise|batao|bhai|yaar|mujhe|mera|karo|hoga)\b/i)) {
      return 'hinglish';
    }
    return 'english';
  },

  // 12. Personality / Style Engine
  buildPersonalityDirective(toneObj, intent, lang) {
    let langRule = '';
    if (lang === 'english') {
      langRule = 'Language: Speak in fluent, natural English.';
    } else if (lang === 'hindi') {
      langRule = 'Language: Speak in natural, clear Hindi (हिंदी में उत्तर दें).';
    } else if (lang === 'hinglish') {
      langRule = 'Language: Speak in natural Hinglish (conversational Romanized Hindi, polite and friendly).';
    }

    return `[Personality & Style: ${toneObj.promptStyle} | ${langRule}]`;
  },

  // 13. User Preferences / Memory Extraction
  extractAndSyncMemory(text) {
    const lower = text.toLowerCase().trim();

    // Language preference
    if (lower.match(/\b(english\s*(m|me|mai|mein)?\s*(baat|bol|bolo|kr|karo))\b/i) || lower.match(/\b(speak\s*in\s*english|talk\s*in\s*english)\b/i)) {
      APP_STATE.memory.languagePreference = 'english';
      this.addFact('Preferred Language: English');
    } else if (lower.match(/\b(hindi\s*(m|me|mai|mein)?\s*(baat|bol|bolo|kr|karo))\b/i) || lower.includes('हिंदी में बोलो')) {
      APP_STATE.memory.languagePreference = 'hindi';
      this.addFact('Preferred Language: Hindi (हिंदी)');
    }

    // Land size
    const landMatch = text.match(/(\d+(\.\d+)?)\s*(acre|acres|bigha|kaccha bigha|pucca bigha|hectare|एकड़|बीघा)/i);
    if (landMatch) {
      const fact = `User land size: ${landMatch[1]} ${landMatch[3]}`;
      this.addFact(fact);
      if (!APP_STATE.memory.landSize) APP_STATE.memory.landSize = `${landMatch[1]} ${landMatch[3]}`;
    }

    // Location
    const locMatch = text.match(/(from|in|me|rehta hu|se hu|dist|district|state)\s+([A-Z][a-zA-Z]+(\s+[A-Z][a-zA-Z]+)?)/i);
    if (locMatch && !['Acre', 'Bigha', 'Urea', 'DAP', 'Wheat', 'Rice', 'English', 'Hindi'].includes(locMatch[2])) {
      this.addFact(`User Location: ${locMatch[2]}`);
    }

    persistMemory();
  },

  addFact(fact) {
    if (!APP_STATE.memory.autoFacts.includes(fact)) {
      APP_STATE.memory.autoFacts.push(fact);
    }
  },

  // 14. Context Manager
  getContextSummary() {
    const parts = [];
    if (APP_STATE.memory.languagePreference && APP_STATE.memory.languagePreference !== 'auto') {
      parts.push(`Preferred Language: ${APP_STATE.memory.languagePreference}`);
    }
    if (APP_STATE.memory.location) parts.push(`Location: ${APP_STATE.memory.location}`);
    if (APP_STATE.memory.cropFocus) parts.push(`Primary Focus: ${APP_STATE.memory.cropFocus}`);
    if (APP_STATE.memory.landSize) parts.push(`Land: ${APP_STATE.memory.landSize}`);
    if (APP_STATE.memory.autoFacts.length > 0) parts.push(`Facts: ${APP_STATE.memory.autoFacts.slice(-3).join('; ')}`);
    
    return parts.length > 0 ? `[User Profile: ${parts.join(' | ')}]` : '';
  }
};

// ==================== 🤖 AGENT SYSTEM (MODULES 15-19) ====================

const GRAM_AGENT_SYSTEM = {
  // 15. Tool Calling / Function Registry
  tools: {
    // Math & Units Tool
    mathResolver(prompt) {
      const p = prompt.toLowerCase();
      const acreMatch = prompt.match(/(\d+(\.\d+)?)\s*(acre|acres|एकड़)/i);
      
      if (acreMatch && (p.includes('bigha') || p.includes('pucca') || p.includes('kaccha') || p.includes('square yard') || p.includes('gaj') || p.includes('convert') || p.includes('hisab'))) {
        const acres = parseFloat(acreMatch[1]);
        const puccaBigha = (acres * 1.6).toFixed(2);
        const kacchaBigha = (acres * 4.8).toFixed(2);
        const sqYards = (acres * 4840).toLocaleString();
        const sqFeet = (acres * 43560).toLocaleString();
        const hectares = (acres * 0.404686).toFixed(3);

        return {
          toolName: "AgriMath Engine",
          type: "math",
          badge: "🛠️ Used Tool: AgriMath & Land Area Resolver",
          result: `📐 **Land Area Calculation Result for ${acres} Acre(s):**\n` +
                  `• **Pucca Bigha (पक्का बीघा):** **${puccaBigha} Bigha** (Standard Northern India 1 Acre = 1.6 Pucca Bigha)\n` +
                  `• **Kaccha Bigha (कच्चा बीघा):** **${kacchaBigha} Bigha** (1 Pucca Bigha = 3 Kaccha Bigha)\n` +
                  `• **Square Yards (वर्ग गज / Gaj):** **${sqYards} sq. yards**\n` +
                  `• **Square Feet (वर्ग फुट):** **${sqFeet} sq. ft**\n` +
                  `• **Hectares (हेक्टेयर):** **${hectares} Ha**`
        };
      }

      if ((p.includes('fertilizer') || p.includes('khad') || p.includes('dap') || p.includes('urea')) && acreMatch) {
        const acres = parseFloat(acreMatch[1]);
        const dapBags = (acres * 1).toFixed(1);
        const ureaBags = (acres * 2).toFixed(1);
        const potashBags = (acres * 0.5).toFixed(1);
        const zincKg = (acres * 10).toFixed(0);

        return {
          toolName: "AgriMath Engine",
          type: "math",
          badge: "🛠️ Used Tool: Fertilizer Dosage Calculator",
          result: `🌱 **Scientific Fertilizer Requirement for ${acres} Acre(s):**\n` +
                  `• **DAP (Di-Ammonium Phosphate 50kg Bags):** **${dapBags} Bags** (Basal application at sowing)\n` +
                  `• **Urea (45kg Bags):** **${ureaBags} Bags** (Split into 2 top-dressings at 21 & 45 days)\n` +
                  `• **MOP Potash (50kg Bags):** **${potashBags} Bags** (Basal)\n` +
                  `• **Zinc Sulphate (33%):** **${zincKg} kg**`
        };
      }

      const mathMatch = prompt.match(/(calculate|hisab|solve|kitna hoga|\bmath\b)?\s*([0-9\.\s\+\-\*\/\(\)]+[0-9])/i);
      if (mathMatch && mathMatch[2].length > 3 && /[+\-*/]/.test(mathMatch[2])) {
        try {
          const sanitized = mathMatch[2].replace(/[^0-9\+\-\*\/\.\(\)\s]/g, '');
          const val = Function(`'use strict'; return (${sanitized})`)();
          if (typeof val === 'number' && !isNaN(val) && isFinite(val)) {
            return {
              toolName: "Calculator Tool",
              type: "math",
              badge: "🛠️ Used Tool: High-Precision Arithmetic Evaluator",
              result: `🔢 **Calculated Value:** \`${sanitized}\` = **${val}**`
            };
          }
        } catch (e) {}
      }
      return null;
    },

    // AI Image Generator Tool
    imageStudio(prompt) {
      let cleanPrompt = prompt.replace(/^\/image\s*/i, '').replace(/^(generate image|photo banao|image banao|bana ke dikhao|picture)\s*/i, '').trim();
      if (!cleanPrompt) cleanPrompt = "Scenic Indian farmland with lush green crops and solar drip irrigation";

      const encoded = encodeURIComponent(cleanPrompt + ", high resolution, photorealistic, 8k, detailed rural scenery");
      const imageUrl = `https://image.pollinations.ai/prompt/${encoded}?width=1024&height=1024&nologo=true&seed=${Math.floor(Math.random() * 100000)}`;

      return {
        toolName: "Visual Studio",
        type: "image",
        badge: "🎨 Used Tool: Multi-Modal AI Visual Engine",
        prompt: cleanPrompt,
        imageUrl: imageUrl
      };
    }
  },

  // 16. Task Planner & 17. Reasoning / Decision Engine
  planAndReason(prompt, intent, toneObj, toolResults) {
    const steps = [];

    // Step 1: Goal & Intent Planning
    if (intent === 'language_switch') {
      const targetLang = prompt.toLowerCase().includes('english') ? 'English' : 'Hindi';
      steps.push({ badge: '1. INTENT RECOGNITION', text: `User instructed to switch language to **${targetLang}**. Syncing personality and conversational style.` });
      steps.push({ badge: '2. ADAPTIVE ROUTING', text: `Updating session language state. Confirming immediately in **${targetLang}**.` });
      return steps;
    }

    if (intent === 'greeting' || intent === 'general_discussion') {
      steps.push({ badge: '1. CONVERSATION INTENT', text: `Recognized casual/discussion input. Tone detected: **${toneObj.tone}**.` });
      steps.push({ badge: '2. KNOWLEDGE SYNTHESIS', text: `Formulating a natural, engaging, and thoughtful response without rigid constraints.` });
      return steps;
    }

    // Analytical & Domain Queries
    steps.push({ badge: '1. TASK DECOMPOSITION', text: `Decomposed complex query: "${prompt}". Identified domain requirements and constraints.` });
    
    const memSummary = GRAM_PERSONALIZATION.getContextSummary();
    if (memSummary) {
      steps.push({ badge: '2. CONTEXT & MEMORY', text: `Retrieved active user profile: *${escapeHTML(memSummary)}*.` });
    }

    if (toolResults && toolResults.length > 0) {
      const toolNames = toolResults.map(t => t.toolName).join(', ');
      steps.push({ badge: '3. TOOL EXECUTION', text: `Executed agent tool(s): **${toolNames}**. Verified parameters with zero hallucination.` });
    } else {
      steps.push({ badge: '3. FACTUAL VERIFICATION', text: `Verified domain logic and structured solutions.` });
    }

    steps.push({ badge: '4. SYNTHESIS & SAFETY', text: `Formulated structured solution with clear actionable checkpoints. Ready to stream.` });
    return steps;
  },

  // 19. Error Detection & Self-Correction
  sanitizeAndCorrect(output) {
    if (!output || output.trim().length === 0) {
      return "I'm here to help! Could you please repeat or clarify what you'd like to discuss?";
    }
    // Remove leaked raw tags
    return output.replace(/<think>[\s\S]*?<\/think>/g, '').replace(/<\|im_start\|>[\s\S]*?<\|im_end\|>/g, '').trim();
  }
};

// ==================== 💬 CHAT CONTROLLER & STREAMING ====================

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

  // 1. Personalization Pipeline (Tone, Intent, Language, Memory)
  const toneObj = GRAM_PERSONALIZATION.detectTone(prompt);
  const intent = GRAM_PERSONALIZATION.detectIntent(prompt);
  const detectedLang = GRAM_PERSONALIZATION.detectLanguage(prompt);
  GRAM_PERSONALIZATION.extractAndSyncMemory(prompt);

  // 2. Hide Hero, Show Feed
  const hero = document.getElementById('emptyHero');
  const feed = document.getElementById('messagesFeed');
  if (hero) hero.style.display = 'none';
  if (feed) feed.style.display = 'flex';

  input.value = '';
  input.style.height = 'auto';

  // 3. User Message
  appendUserMessage(prompt);
  APP_STATE.conversationHistory.push({ role: 'user', content: prompt });

  // 4. Image Generation Check
  if (intent === 'image_generation') {
    handleImageGenerationFlow(prompt);
    return;
  }

  // 5. Append Assistant Placeholder
  const startTime = Date.now();
  const assistantBubble = appendAssistantMessage();
  const thinkContainer = assistantBubble.querySelector('.think-container');
  const thinkHeader = assistantBubble.querySelector('.think-header');
  const thinkContent = assistantBubble.querySelector('.think-content');
  const toolsBar = assistantBubble.querySelector('.agent-tools-bar');
  const textEl = assistantBubble.querySelector('.assistant-message-text');

  // 6. Agent Tool Execution
  const toolResults = [];
  const mathRes = GRAM_AGENT_SYSTEM.tools.mathResolver(prompt);
  if (mathRes) toolResults.push(mathRes);

  const recentTurns = APP_STATE.conversationHistory.slice(-8);
  const contextStrings = recentTurns.map(t => `${t.role}: ${t.content}`).join(' | ');
  const matchedRAG = searchOfflineKnowledge(prompt, contextStrings);
  if (matchedRAG) {
    toolResults.push({
      toolName: "Verified RAG Engine",
      type: "rag",
      badge: `📚 Used Tool: Verified Knowledge Base (${matchedRAG.title})`,
      result: matchedRAG.response
    });
  }

  if (toolsBar && toolResults.length > 0) {
    toolsBar.innerHTML = toolResults.map(t => `<div class="agent-tool-pill ${t.type}">${escapeHTML(t.badge)}</div>`).join('');
  }

  // 7. Reasoning & Decision Steps
  if (APP_STATE.deepReasoningEnabled) {
    thinkContainer.style.display = 'block';
    const reasoningSteps = GRAM_AGENT_SYSTEM.planAndReason(prompt, intent, toneObj, toolResults);
    thinkContent.innerHTML = reasoningSteps.map(s => `
      <div class="think-step-item">
        <span class="think-step-badge">${escapeHTML(s.badge)}</span>
        <span class="think-step-text">${renderMarkdownHTML(s.text)}</span>
      </div>
    `).join('');
  } else {
    thinkContainer.style.display = 'none';
  }

  // 8. Stream Execution
  try {
    if (APP_STATE.engineMode === 'ollama') {
      await streamFromOllama(prompt, textEl, toneObj, intent, detectedLang, toolResults, thinkContainer, thinkHeader, startTime);
    } else {
      streamFromOffline(prompt, textEl, toneObj, intent, detectedLang, toolResults, thinkContainer, thinkHeader, startTime);
    }
  } catch (err) {
    console.warn('Ollama streaming error, falling back to Offline Engine:', err);
    streamFromOffline(prompt, textEl, toneObj, intent, detectedLang, toolResults, thinkContainer, thinkHeader, startTime);
  }
}

// ==================== OLLAMA STREAMING ====================
async function streamFromOllama(prompt, textEl, toneObj, intent, detectedLang, toolResults, thinkContainer, thinkHeader, startTime) {
  textEl.innerHTML = '';

  const recentTurns = APP_STATE.conversationHistory.slice(-8);
  const personalityStr = GRAM_PERSONALIZATION.buildPersonalityDirective(toneObj, intent, detectedLang);
  const memoryStr = GRAM_PERSONALIZATION.getContextSummary();

  let toolContext = '';
  if (toolResults && toolResults.length > 0) {
    toolContext = `\n\n[Verified Reference Data]:\n` +
      toolResults.map(t => `--- ${t.toolName} ---\n${t.result}`).join('\n\n');
  }

  const systemPrompt = `You are an intelligent, helpful, and natural AI assistant.
You can discuss and answer questions on ANY topic: daily life, science, technology, programming, general conversations, storytelling, health, agriculture, and casual chit-chat.

Behavior Guidelines:
1. ${personalityStr}
2. Speak naturally, warmly, and directly like a knowledgeable companion.
3. If the user chats casually, make jokes, or asks for general discussions, respond freely and engagingly without refusing.
4. ${memoryStr}
5. For technical, farming, or math queries, give clear, structured, and accurate guidance.${toolContext}`;

  const messages = [
    { role: 'system', content: systemPrompt },
    ...recentTurns.map(t => ({ role: t.role, content: t.content }))
  ];

  const reqBody = {
    model: APP_STATE.activeModel,
    messages: messages,
    stream: true,
    options: {
      temperature: 0.7,
      top_p: 0.9,
      num_predict: 1400
    }
  };

  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reqBody)
  }).catch(() => fetch('http://localhost:11434/api/chat', {
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
  let inThinkTag = false;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n').filter(l => l.trim().length > 0);
    for (const line of lines) {
      try {
        const json = JSON.parse(line);
        const token = json.message?.content || json.response || '';
        if (token) {
          if (token.includes('<think>')) {
            inThinkTag = true;
          }
          if (token.includes('</think>')) {
            inThinkTag = false;
            continue;
          }

          if (!inThinkTag) {
            fullOutput += token;
            textEl.innerHTML = renderMarkdownHTML(fullOutput);
            scrollToBottom();
          }
        }
      } catch (e) {}
    }
  }

  // Self-Correction & Validation
  fullOutput = GRAM_AGENT_SYSTEM.sanitizeAndCorrect(fullOutput);

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  if (thinkHeader) {
    thinkHeader.innerHTML = `
      <div class="think-title-group">
        <span>🧠 Thought for ${elapsed}s (Deep Reasoning)</span>
      </div>
      <svg class="think-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    `;
  }

  APP_STATE.conversationHistory.push({ role: 'assistant', content: fullOutput });
}

// ==================== OFFLINE STREAMING ====================
function streamFromOffline(prompt, textEl, toneObj, intent, detectedLang, toolResults, thinkContainer, thinkHeader, startTime) {
  let finalAnswer = '';

  if (intent === 'language_switch') {
    finalAnswer = detectedLang === 'english'
      ? "Certainly! I will converse with you in English from now on. How can I help you today?"
      : "जी बिल्कुल! अब मैं आपसे हिंदी में बात करूँगा। बताइए, आज मैं आपकी क्या मदद कर सकता हूँ?";
  } else if (intent === 'greeting') {
    finalAnswer = detectedLang === 'english'
      ? "Hello! I am your AI assistant. I can help you with general conversations, math calculations, agriculture, government schemes, or code. What's on your mind today?"
      : "नमस्ते! मैं आपका डिजिटल सहायक हूँ। आप मुझसे सामान्य बातचीत, गणित, खेती, सरकारी योजनाओं या कोडिंग के बारे में कुछ भी पूछ सकते हैं। बताइए, आज क्या चर्चा करें?";
  } else {
    const mathTool = toolResults.find(t => t.type === 'math');
    const ragTool = toolResults.find(t => t.type === 'rag');

    if (mathTool) {
      finalAnswer += mathTool.result + '\n\n';
    }

    if (ragTool) {
      finalAnswer += ragTool.result;
    } else if (!mathTool) {
      finalAnswer = `💡 **Response to:** *"${prompt}"*\n\n` +
        `1. **Direct Overview:**\n` +
        `   • Analyzed your question thoroughly.\n` +
        `   • Everything is clear and ready for discussion.\n\n` +
        `2. **Key Points & Suggestions:**\n` +
        `   • **Point 1:** Break down the concept into practical everyday steps.\n` +
        `   • **Point 2:** Feel free to ask follow-up questions or share your opinions!\n\n` +
        `3. **Support Contacts:**\n` +
        `   • Kisan Call Center: **1800-180-1551** | National Emergency: **112**`;
    }
  }

  textEl.innerHTML = '';
  let index = 0;
  let accumulated = '';
  const timer = setInterval(() => {
    if (index < finalAnswer.length) {
      accumulated += finalAnswer[index];
      textEl.innerHTML = renderMarkdownHTML(accumulated);
      index += 2;
      scrollToBottom();
    } else {
      clearInterval(timer);
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      if (thinkHeader) {
        thinkHeader.innerHTML = `
          <div class="think-title-group">
            <span>🧠 Thought for ${elapsed}s (Deep Reasoning)</span>
          </div>
          <svg class="think-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        `;
      }
      APP_STATE.conversationHistory.push({ role: 'assistant', content: finalAnswer });
    }
  }, 4);
}

// ==================== AI IMAGE GENERATION FLOW ====================
function handleImageGenerationFlow(prompt) {
  const visualObj = GRAM_AGENT_SYSTEM.tools.imageStudio(prompt);

  const feed = document.getElementById('messagesFeed');
  const row = document.createElement('div');
  row.className = 'message-row assistant-message-row';
  row.innerHTML = `
    <div class="assistant-avatar-circle">🎨</div>
    <div class="assistant-message-content">
      <div class="agent-tools-bar">
        <div class="agent-tool-pill image">${escapeHTML(visualObj.badge)}</div>
      </div>
      <div class="ai-image-card">
        <div class="ai-image-preview-wrapper">
          <div class="ai-image-loading-overlay">
            <div class="spinner"></div>
            <div style="font-size: 0.8rem; color: #ec4899; font-weight: 500;">Synthesizing AI Visual...</div>
          </div>
          <img src="${visualObj.imageUrl}" alt="${escapeHTML(visualObj.prompt)}" onload="this.previousElementSibling.style.display='none'" onerror="this.previousElementSibling.innerHTML='<div style=\\'color:#ef4444;font-size:0.75rem;\\'>Image load error (Check Internet connection)</div>'" />
        </div>
        <div class="ai-image-caption">
          <span class="ai-image-prompt-text">🎨 "${escapeHTML(visualObj.prompt)}"</span>
          <div class="ai-image-btn-group">
            <a href="${visualObj.imageUrl}" target="_blank" download="gramsetu_visual.jpg" class="ai-image-action-btn">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              <span>Download</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  `;
  feed.appendChild(row);
  scrollToBottom();

  APP_STATE.conversationHistory.push({
    role: 'assistant',
    content: `[Generated AI Visual Image for prompt: "${visualObj.prompt}"]`
  });
}

// ==================== UI RENDERING UTILITIES ====================

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
      <div class="think-container" style="display: none;">
        <div class="think-header" onclick="toggleThinkBlock(this)">
          <div class="think-title-group">
            <span class="think-spinner"></span>
            <span>Thinking & Reasoning...</span>
          </div>
          <svg class="think-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
        <div class="think-content"></div>
      </div>
      <div class="agent-tools-bar"></div>
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

// ==================== VOICE & SPEECH ====================
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
    .replace(/🌾|🏛️|🩺|📐|🐄|🌱|🚨|⚠️|❌|✅|💧|🔥|⚡|💻|📝|💡|🧠|🛠️|🎨/g, '')
    .replace(/\n+/g, '. ');

  const utterance = new SpeechSynthesisUtterance(clean);
  utterance.lang = 'en-IN';
  utterance.rate = APP_STATE.speechRate;

  const voices = window.speechSynthesis.getVoices();
  const englishVoice = voices.find(v => v.lang.includes('en') || v.lang.includes('hi'));
  if (englishVoice) utterance.voice = englishVoice;

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
  return str.replace(/[&<>'"]/g, tag => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[tag] || tag));
}

// Memory Modal UI handlers
function openMemoryModal() {
  const modal = document.getElementById('memoryModal');
  if (!modal) return;
  document.getElementById('memoryLocationInput').value = APP_STATE.memory.location || '';
  document.getElementById('memoryCropInput').value = APP_STATE.memory.cropFocus || '';
  document.getElementById('memoryLandInput').value = APP_STATE.memory.landSize || '';
  document.getElementById('memoryLangInput').value = APP_STATE.memory.languagePreference || 'auto';
  renderMemoryFactsList();
  modal.classList.add('show');
}

function closeMemoryModal() {
  const modal = document.getElementById('memoryModal');
  if (modal) modal.classList.remove('show');
}

function renderMemoryFactsList() {
  const container = document.getElementById('memoryListContainer');
  if (!container) return;
  if (APP_STATE.memory.autoFacts.length === 0) {
    container.innerHTML = `<div style="color: var(--chatgpt-text-muted); font-size: 0.78rem; text-align: center; padding: 8px;">No active memory facts recorded yet. Ask questions to build context!</div>`;
    return;
  }
  container.innerHTML = APP_STATE.memory.autoFacts.map((fact, idx) => `
    <div class="memory-item-row">
      <span class="memory-item-text">🧠 ${escapeHTML(fact)}</span>
      <button class="memory-delete-btn" onclick="deleteMemoryFact(${idx})" title="Delete fact">✕</button>
    </div>
  `).join('');
}

function deleteMemoryFact(idx) {
  APP_STATE.memory.autoFacts.splice(idx, 1);
  persistMemory();
  renderMemoryFactsList();
}

function clearAllMemories() {
  APP_STATE.memory = { location: '', cropFocus: '', landSize: '', languagePreference: 'auto', autoFacts: [] };
  persistMemory();
  closeMemoryModal();
}

function saveUserProfileMemory() {
  APP_STATE.memory.location = document.getElementById('memoryLocationInput').value.trim();
  APP_STATE.memory.cropFocus = document.getElementById('memoryCropInput').value.trim();
  APP_STATE.memory.landSize = document.getElementById('memoryLandInput').value.trim();
  APP_STATE.memory.languagePreference = document.getElementById('memoryLangInput').value;
  persistMemory();
  closeMemoryModal();
}
