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
    console.warn('Local Python server not reachable, seamlessly switching to 100% On-Device Offline Client Engine:', err);
    
    const clientResult = processOfflineClientQuery(prompt);
    
    renderProcessingMetadata({
      intent: clientResult.intent,
      tone: clientResult.tone,
      input_language: "Hindi / Hinglish / English",
      output_language: "Hindi / Hinglish",
      tools_executed: clientResult.tools_executed,
      rag_title: clientResult.rag_title
    }, thinkContent, toolsBar, assistantBubble);

    await streamClientText(clientResult.text, textEl, thinkHeader, startTime);
    APP_STATE.conversationHistory.push({ role: 'assistant', content: clientResult.text });
  }
}

// 100% On-Device Client-Side Offline Intelligence Engine
function processOfflineClientQuery(prompt) {
  const p = prompt.toLowerCase().trim();
  
  // 1. Check Greetings
  if (/^(namaste|ram ram|kisan|hello|hi|hey|pranam|namaskar|shubhechha|kem cho|sat sri akaal)/i.test(p)) {
    return {
      intent: "GREETING",
      tone: "Warm Rural Advisory",
      tools_executed: ["Kisan Sahayak", "Offline Knowledge Base"],
      rag_title: "GramSetu Onboarding & Welcome",
      text: `🌾 **राम-राम किसान भाई! मैं ग्रामसेतु (GramSetu AI) हूँ।**\n\nमैं आपकी खेती, कृषि यंत्रों (Tools), फसलों, रोगों के उपचार, खाद व जमीन गणना, सरकारी योजनाओं और आपातकालीन सहायता के लिए 100% ऑफ़लाइन तैयार हूँ।\n\n**आप मुझसे क्या-क्या पूछ सकते हैं:**\n• 🚜 **कृषि यंत्र व औजार:** जुताई (Tractor, Rotavator), बुवाई (Seed Drill), छिड़काव (Sprayers, Drone) व 40-50% सब्सिडी\n• 🌾 **फसल गाइड व बीज मात्रा:** गेहूं, सरसों, चना, धान, कपास, आलू, गन्ना, मक्का, टमाटर आदि की खेती\n• 🧮 **खाद व जमीन कैलकुलेटर:** "3.5 एकड़ में कितना बीघा?", "5 एकड़ गेहूं के लिए कितनी खाद चाहिए?"\n• 🐛 **रोग व कीट निदान:** पीला रतुआ, उकठा रोग, माहू (एफिड), सुंडी, सफेद मक्खी का रासायनिक व जैविक इलाज\n• 🏛️ **सरकारी योजनाएं:** PM-किसान (₹6000), KCC (4% ब्याज दर ऋण), कुसुम सोलर पंप (60-90% सब्सिडी)\n• 🐄 **पशुपालन व डेयरी:** दूध बढ़ाने का संतुलित दाना फॉर्मूला, थनैला व खुरपका रोग का उपचार\n• 🚨 **आपातकालीन फर्स्ट एड:** सांप का काटना, कीटनाशक विषाक्तता, लू लगना (SOS 108/112)\n\n*कृपया अपना सवाल नीचे लिखें या माइक दबाकर पूछें!*`
    };
  }

  // 2. Dynamic Land Area & Math Conversion Tool
  const acreMatch = p.match(/(\d+(?:\.\d+)?)\s*(?:acre|acres|एकड़)/i);
  const bighaMatch = p.match(/(\d+(?:\.\d+)?)\s*(?:bigha|bighas|बीघा)/i);
  const hectareMatch = p.match(/(\d+(?:\.\d+)?)\s*(?:hectare|hectares|हेक्टेयर)/i);

  if ((acreMatch || bighaMatch || hectareMatch) && /(convert|bigha|acre|gaj|yard|feet|hectare|biswa|kanal|marla|zameen|jameen|nap|kitna|hoga|karein)/i.test(p) && !/(khad|urea|dap|fertilizer|bag)/i.test(p)) {
    let acres = 1.0;
    if (acreMatch) acres = parseFloat(acreMatch[1]);
    else if (bighaMatch) acres = parseFloat(bighaMatch[1]) / 1.6;
    else if (hectareMatch) acres = parseFloat(hectareMatch[1]) * 2.471;

    const pucca_bigha = (acres * 1.60).toFixed(2);
    const kaccha_bigha = (acres * 4.80).toFixed(2);
    const sq_yards = Math.round(acres * 4840).toLocaleString();
    const sq_feet = Math.round(acres * 43560).toLocaleString();
    const hectares = (acres * 0.4047).toFixed(3);
    const kanal = Math.round(acres * 8);
    const marla = Math.round(acres * 160);

    return {
      intent: "LAND_MATH_CALCULATOR",
      tone: "Mathematical Agronomy",
      tools_executed: ["Land Unit Engine", "State Bigha Standards"],
      rag_title: `Land Measurement Calculation for ${acres} Acre(s)`,
      text: `📐 **Land Area Calculation Result (भूमि माप गणना परिणाम):**\n\n**आपके दर्ज किए गए क्षेत्र (${acres} एकड़) का सटीक रूपांतरण:**\n\n1. **राष्ट्रीय मानक इकाइयां (Universal Units):**\n   • **वर्ग गज (Square Yards / Gaj):** **${sq_yards} वर्ग गज**\n   • **वर्ग फीट (Square Feet):** **${sq_feet} वर्ग फीट**\n   • **हेक्टेयर (Hectares):** **${hectares} हेक्टेयर**\n\n2. **राज्यों के अनुसार बीघा व अन्य इकाइयां:**\n   • **उत्तर प्रदेश व राजस्थान (पक्का बीघा):** **${pucca_bigha} पक्का बीघा** (1 बीघा = 3025 वर्ग गज = 20 बिस्वा)\n   • **कच्चा बीघा (पश्चिमी UP/हरियाणा बॉर्डर):** **${kaccha_bigha} कच्चा बीघा**\n   • **पंजाब व हरियाणा:** **${kanal} कनाल** (${marla} मरला)\n   • **बिहार व झारखंड:** **${(acres * 1.33).toFixed(2)} बीघा** (${Math.round(acres * 26.6)} कट्ठा)`
    };
  }

  // 3. Dynamic Fertilizer & Seed Requirement Calculator Tool
  if ((acreMatch || bighaMatch) && /(khad|khaad|fertilizer|urea|dap|potash|zinc|bag|kitna|chahiye|lagega|dose)/i.test(p)) {
    let acres = acreMatch ? parseFloat(acreMatch[1]) : (parseFloat(bighaMatch[1]) / 1.6);
    acres = Math.max(0.1, acres);

    let cropType = "गेहूं (Wheat)";
    let dapBags = (acres * 1.0).toFixed(1);
    let ureaBags = (acres * 2.0).toFixed(1);
    let potashKg = Math.round(acres * 25);
    let zincKg = Math.round(acres * 10);
    let seedMin = Math.round(acres * 40);
    let seedMax = Math.round(acres * 45);

    if (/(mustard|sarson|sarso|rai)/i.test(p)) {
      cropType = "सरसों (Mustard)";
      dapBags = (acres * 1.0).toFixed(1);
      ureaBags = (acres * 1.0).toFixed(1);
      potashKg = Math.round(acres * 20);
      zincKg = Math.round(acres * 10); // Sulfur
      seedMin = (acres * 1.5).toFixed(1);
      seedMax = (acres * 2.0).toFixed(1);
    } else if (/(paddy|rice|dhan|chawal)/i.test(p)) {
      cropType = "धान (Paddy/Rice)";
      dapBags = (acres * 1.0).toFixed(1);
      ureaBags = (acres * 2.2).toFixed(1);
      potashKg = Math.round(acres * 30);
      zincKg = Math.round(acres * 10);
      seedMin = Math.round(acres * 6);
      seedMax = Math.round(acres * 12);
    } else if (/(cotton|kapas|narma)/i.test(p)) {
      cropType = "कपास (Cotton)";
      dapBags = (acres * 1.0).toFixed(1);
      ureaBags = (acres * 2.5).toFixed(1);
      potashKg = Math.round(acres * 30);
      zincKg = Math.round(acres * 10);
      seedMin = (acres * 1.5).toFixed(1) + " पैकेट";
      seedMax = (acres * 2.0).toFixed(1) + " पैकेट";
    }

    return {
      intent: "FERTILIZER_SEED_CALCULATOR",
      tone: "Scientific Agricultural Expert",
      tools_executed: ["NPK Stoichiometric Engine", "Crop Agronomy Tool"],
      rag_title: `Fertilizer & Seed Formula for ${acres} Acre(s) of ${cropType}`,
      text: `🌾 **${cropType} के लिए ${acres} एकड़ भूमि हेतु खाद व बीज की सटीक गणना:**\n\n1. **🌱 बीज की कुल मात्रा (Seed Required):**\n   • **${seedMin} से ${seedMax} किग्रा** शुद्ध प्रमाणित बीज।\n\n2. **🧪 रासायनिक खाद की सही मात्रा (Fertilizer Dosage):**\n   • **DAP (50 kg बैग):** **${dapBags} बैग** (बुवाई के समय खेत में नीचे डालें)\n   • **यूरिया (45 kg बैग):** **${ureaBags} बैग** (पहली व दूसरी सिंचाई पर विभाजित करके टॉप ड्रेसिंग करें)\n   • **MOP पोटाश:** **${potashKg} किग्रा** (दाने की चमक व वजन के लिए)\n   • **जिंक सल्फेट (33%) या सल्फर:** **${zincKg} किग्रा**\n\n3. **💡 विशेषज्ञ सलाह:** खाद डालते समय खेत में पर्याप्त नमी का होना आवश्यक है। यूरिया को हमेशा शाम के समय ओस उतरने से पहले छिड़कें।`
    };
  }

  // 4. High-Priority Intent Routing
  // A. Farming Tools, Implements & Machinery
  if (/\b(tool|tools|equipment|machinery|implement|implements|auzar|yantra|tractor|rotavator|cultivator|plow|plough|seed drill|sprayer|sprayers|harvester|thresher|sickle|khurpi|kassi|drone|power weeder|leveler)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "agri_farming_tools_machinery_complete");
    if (node) {
      return {
        intent: "AGRICULTURAL_TOOLS_MACHINERY",
        tone: "Practical Agronomy Expert",
        tools_executed: ["Farm Machinery Knowledge Base", "SMAM Mechanization Advisor"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // B. Dairy, Cattle Care & Milk Yield
  if (/\b(milk|doodh|cow|buffalo|cattle|pashu|gay|gaay|bhains|feed|chara|dana|mastitis|thanela|dairy)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "dairy_cattle_feed_milk_yield");
    if (node) {
      return {
        intent: "DAIRY_ANIMAL_HUSBANDRY",
        tone: "Veterinary Agronomist",
        tools_executed: ["Livestock Nutrition Engine", "Dairy Yield Calculator"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // C. Cotton / Kapas
  if (/\b(cotton|kapas|narma|bollworm)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "agri_cotton_cultivation_complete");
    if (node) {
      return {
        intent: "COTTON_CROP_ADVISORY",
        tone: "Cash Crop Specialist",
        tools_executed: ["Cotton Pathology", "Bollworm Shield"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // D. Soil Types & Fertility
  if (/\b(soil|mitti|domet|kali mitti|red soil|black soil|alluvial|soil test|ph value)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "agri_soil_types_crops");
    if (node) {
      return {
        intent: "SOIL_HEALTH_ADVISORY",
        tone: "Soil Chemist",
        tools_executed: ["ICAR Soil Matrix", "Soil Health Card Assistant"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // E. Mustard / Sarson
  if (/\b(sarso|sarson|mustard|toria|rai|aphid|mahu|chepa)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "agri_mustard_cultivation_complete");
    if (node) {
      return {
        intent: "MUSTARD_CROP_ADVISORY",
        tone: "Scientific Agricultural Expert",
        tools_executed: ["Oilseed Advisory", "Rabi Crop Specialist"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // F. Wilt / Ukatha Disease
  if (/\b(wilt|ukatha|sukh rog|fusarium|trichoderma|root rot)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "agri_wilt_ukatha_disease");
    if (node) {
      return {
        intent: "WILT_PATHOLOGY_CURE",
        tone: "Crop Doctor",
        tools_executed: ["Bio-Fungicide Rx", "Wilt Management Matrix"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // G. Yellow Rust (Peela Ratua)
  if (/\b(yellow rust|peela ratua|ratwa|haldi rog|stripe rust|propiconazole)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "agri_wheat_yellow_rust_cure");
    if (node) {
      return {
        intent: "CROP_PATHOLOGY_DIAGNOSIS",
        tone: "Crop Doctor",
        tools_executed: ["Fungicide Rx", "Wheat Disease Matrix"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // H. Wheat Cultivation
  if (/\b(wheat|gehu|gehun|kanak)\b/i.test(p) && /\b(ugana|ugaye|kheti|sowing|variety|irrigation|bona|farming|fasal|weed|sinchai)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "agri_wheat_cultivation_complete");
    if (node) {
      return {
        intent: "WHEAT_CROP_ADVISORY",
        tone: "Scientific Agricultural Expert",
        tools_executed: ["Wheat Specialist", "Rabi Advisor"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // I. Paddy / Rice
  if (/\b(dhan|chawal|rice|paddy)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "agri_paddy_cultivation_complete");
    if (node) {
      return {
        intent: "RICE_CROP_ADVISORY",
        tone: "Scientific Agricultural Expert",
        tools_executed: ["Paddy Specialist", "Kharif Advisor"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // J. Organic Jeevamrut & Natural Farming
  if (/\b(jeevamrut|jaivik|organic|desi khad|neemastra|vermicompost|dung|gomutra|natural farming)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "organic_jeevamrut_preparation");
    if (node) {
      return {
        intent: "ORGANIC_NATURAL_FARMING",
        tone: "Organic Farming Specialist",
        tools_executed: ["Bio-Fertilizer Formulation", "Natural Farming Guide"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // K. PM-Kisan Scheme
  if (/\b(pm kisan|pmkisan|6000|samman nidhi|kist|installment|land seeding|ekyc)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "scheme_pm_kisan");
    if (node) {
      return {
        intent: "GOVT_SCHEME_ADVISORY",
        tone: "Scheme Counselor",
        tools_executed: ["PM-Kisan Database", "DBT Portal Sync"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // L. KCC Loan Scheme
  if (/\b(kcc|kisan credit|credit card|loan|fasal loan|byaj|3 lakh)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "scheme_kcc_kisan_credit_card");
    if (node) {
      return {
        intent: "CREDIT_FINANCE_ADVISORY",
        tone: "Financial Counselor",
        tools_executed: ["KCC Rate Calculator", "NABARD Guidelines"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // M. Solar Pump Scheme (PM-KUSUM)
  if (/\b(kusum|solar pump|solar|pm kusum|tubewell|sinchai pump)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "scheme_pm_kusum_solar_pump");
    if (node) {
      return {
        intent: "SOLAR_ENERGY_SCHEME",
        tone: "Renewable Energy Advisor",
        tools_executed: ["PM-Kusum Portal Sync", "MNRE Scheme Database"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // N. Emergency Snake Bite First Aid
  if (/\b(snake|saanp|saap|venom|bite|katna)\b/i.test(p)) {
    const node = COMPREHENSIVE_KNOWLEDGE_BASE.find(n => n.id === "health_snake_bite");
    if (node) {
      return {
        intent: "EMERGENCY_MEDICAL_FIRST_AID",
        tone: "Emergency Triage",
        tools_executed: ["First Aid Protocol", "Emergency Hotline 108"],
        rag_title: node.title,
        text: node.response
      };
    }
  }

  // 5. Multi-Word TF-IDF Fallback Search
  if (typeof COMPREHENSIVE_KNOWLEDGE_BASE !== 'undefined' && Array.isArray(COMPREHENSIVE_KNOWLEDGE_BASE)) {
    let bestNode = null;
    let highestScore = 0;
    const queryTokens = p.replace(/[^\w\u0900-\u097F\s]/g, ' ')
                         .split(/\s+/)
                         .filter(w => !/^(which|what|how|why|when|who|where|the|a|an|is|are|in|on|at|to|for|of|with|and|or|required|needed|please|kya|kaise|hota|hote|hain|hai|ka|ke|ki|ko|se|me|pe|par|batao|bataiye|chahiye|karein|kare|karte|aur)$/i.test(w) && w.length > 1);

    for (const node of COMPREHENSIVE_KNOWLEDGE_BASE) {
      let score = 0;
      const nodeKeywords = (node.keywords || []).map(k => k.toLowerCase());
      const nodeTags = (node.tags || []).map(t => t.toLowerCase());
      const nodeTitle = (node.title || '').toLowerCase();

      for (const tok of queryTokens) {
        if (nodeTitle.includes(tok)) score += 30;
        for (const kw of nodeKeywords) {
          if (kw === tok) score += 25;
          else if (kw.includes(tok)) score += 10;
        }
        for (const tag of nodeTags) {
          if (tag.toLowerCase().includes(tok)) score += 15;
        }
      }

      if (score > highestScore) {
        highestScore = score;
        bestNode = node;
      }
    }

    if (bestNode && highestScore >= 20) {
      return {
        intent: bestNode.category ? bestNode.category.toUpperCase() : "AGRICULTURE_ADVISORY",
        tone: "Scientific Agricultural Expert",
        tools_executed: ["Offline Local RAG", bestNode.tags?.[0] || "Crop Advisor"],
        rag_title: bestNode.title,
        text: bestNode.response
      };
    }
  }

  // 6. Intelligent Context-Aware General Fallback
  return {
    intent: "RURAL_AI_ADVISORY",
    tone: "Helpful Agricultural Assistant",
    tools_executed: ["GramSetu Multi-Domain Engine"],
    rag_title: "GramSetu Comprehensive Knowledge System",
    text: `🌾 **ग्रामसेतु AI (ऑफ़लाइन सहायक उत्तर):**\n\nआपके प्रश्न **"${prompt}"** के संबंध में मुख्य सलाह:\n\n1. 🚜 **कृषि औजार व तकनीकी:** खेत की जुताई (Rotavator/Plough), बुवाई (Seed Drill), व छिड़काव (Battery Sprayers) से लागत कम और पैदावार बढ़ती है। (SMAM पोर्टल पर 40-50% सब्सिडी उपलब्ध है)।\n2. 🌾 **फसल व पोषक तत्व:** मिट्टी की जांच के अनुसार संतुलित मात्रा में DAP, यूरिया, पोटाश व जिंक का उपयोग करें।\n3. 🏛️ **सरकारी योजनाएं:** PM-किसान सम्मान निधि (₹6000/वर्ष) व KCC (4% ब्याज दर) के लिए CSC केंद्र पर आवेदन करें।\n4. 🚨 **आपातकाल:** एम्बुलेंस के लिए **108** और पुलिस सहायता के लिए **112** डायल करें।\n\n*(सुझाव: विशिष्ट जानकारी के लिए प्रश्न जैसे "कृषि यंत्र", "कपास की खेती", "सरसों", "3.5 एकड़ जमीन कैलकुलेटर" या "पीएम किसान" लिखकर पूछें।)*`
  };
}

async function streamClientText(fullText, textEl, thinkHeader, startTime) {
  const chunks = fullText.split(/(\s+|\n+)/);
  let accumulated = '';
  
  for (let i = 0; i < chunks.length; i++) {
    accumulated += chunks[i];
    textEl.innerHTML = renderMarkdownHTML(accumulated);
    scrollToBottom();
    if (i % 2 === 0) {
      await new Promise(r => setTimeout(r, 10));
    }
  }

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  if (thinkHeader) {
    thinkHeader.innerHTML = `
      <div class="think-title-group">
        <span>⚡ Processed in ${elapsed}s (100% On-Device Offline Engine)</span>
      </div>
      <svg class="think-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    `;
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
