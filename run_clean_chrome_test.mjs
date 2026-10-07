import fs from 'fs';

class ChromeCDP {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.msgId = 1;
    this.pending = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (e) => {
        const d = JSON.parse(e.data);
        if (d.id && this.pending.has(d.id)) {
          const { resolve, reject } = this.pending.get(d.id);
          this.pending.delete(d.id);
          if (d.error) reject(d.error);
          else resolve(d.result);
        }
      };
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.msgId++;
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async eval(code) {
    const res = await this.send('Runtime.evaluate', {
      expression: code,
      returnByValue: true,
      awaitPromise: true
    });
    return res.result ? res.result.value : null;
  }

  async screenshot(filePath) {
    const res = await this.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(filePath, Buffer.from(res.data, 'base64'));
    return filePath;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function main() {
  console.log('🔗 Connecting to existing open Chrome tab (port 9222)...');
  const tabsRes = await fetch('http://localhost:9222/json');
  const tabs = await tabsRes.json();
  const tab = tabs.find(t => t.url.includes('localhost:8000'));
  if (!tab) {
    console.error('❌ GramSetu tab not found!');
    process.exit(1);
  }

  const cdp = new ChromeCDP(tab.webSocketDebuggerUrl);
  await cdp.connect();
  console.log('✅ Connected to Chrome tab:', tab.title);

  // Function to send a prompt and wait for assistant response to finish in DOM
  async function sendAndAwait(prompt, timeoutMs = 30000) {
    console.log(`\n======================================================`);
    console.log(`💬 USER INPUT: "${prompt}"`);
    console.log(`======================================================`);

    // Count existing assistant rows
    const initialRows = await cdp.eval(`document.querySelectorAll('.message-row.assistant-message-row').length`);

    // Set input and trigger send
    await cdp.eval(`(() => {
      const input = document.getElementById('chatInput');
      input.value = ${JSON.stringify(prompt)};
      handleSend();
    })()`);

    console.log('⏳ Dispatched into live Chrome DOM. Waiting for streaming to complete...');

    const start = Date.now();
    let finalResult = null;

    while (Date.now() - start < timeoutMs) {
      await sleep(1000);

      const status = await cdp.eval(`(() => {
        const rows = document.querySelectorAll('.message-row.assistant-message-row');
        if (rows.length <= ${initialRows}) return null;
        const lastRow = rows[rows.length - 1];
        const textEl = lastRow.querySelector('.assistant-message-text');
        const text = textEl ? textEl.innerText.trim() : '';
        const isStreaming = text.includes('Thinking...') || !!lastRow.querySelector('.cursor-pulse') || !!lastRow.querySelector('.think-spinner');
        const thinkSteps = Array.from(lastRow.querySelectorAll('.think-step-item')).map(s => s.innerText.replace(/\\s+/g, ' ').trim());
        const toolPills = Array.from(lastRow.querySelectorAll('.agent-tool-pill')).map(p => p.innerText.trim());
        const hasCodeBlock = !!lastRow.querySelector('pre, code');
        
        return {
          text,
          isStreaming,
          thinkSteps,
          toolPills,
          hasCodeBlock,
          length: text.length
        };
      })()`);

      if (status && status.length > 10 && !status.isStreaming) {
        finalResult = status;
        break;
      }
    }

    if (!finalResult) {
      // Grab whatever is there
      finalResult = await cdp.eval(`(() => {
        const rows = document.querySelectorAll('.message-row.assistant-message-row');
        const lastRow = rows[rows.length - 1];
        return {
          text: lastRow?.querySelector('.assistant-message-text')?.innerText || 'TIMEOUT',
          thinkSteps: Array.from(lastRow?.querySelectorAll('.think-step-item') || []).map(s => s.innerText.trim()),
          toolPills: Array.from(lastRow?.querySelectorAll('.agent-tool-pill') || []).map(p => p.innerText.trim())
        };
      })()`);
    }

    console.log('\n🎯 LIVE DOM RENDER RESULT:');
    if (finalResult.thinkSteps && finalResult.thinkSteps.length > 0) {
      console.log('🧠 Pipeline Metadata (Deep Think):');
      finalResult.thinkSteps.forEach(s => console.log('   • ' + s));
    }
    if (finalResult.toolPills && finalResult.toolPills.length > 0) {
      console.log('🛠️ Tool Badges: ' + finalResult.toolPills.join(', '));
    }
    if (finalResult.hasCodeBlock) {
      console.log('💻 Code Block (<pre><code>): Rendered in DOM');
    }
    console.log('\n📄 Assistant Text Content:');
    console.log(finalResult.text);
    return finalResult;
  }

  // Clear chat first for a fresh visual test
  await cdp.eval(`createNewChat()`);
  await sleep(600);

  // Test 1: Hinglish Greeting
  await sendAndAwait('kya hal h');

  // Test 2: Memory Ingestion
  await sendAndAwait('Mera naam Yash hai aur mere paas 5 acre zameen hai Karnal me');

  // Test 3: Math & Agriculture Calculation using Stored Memory
  await sendAndAwait('5 acre gehu ke liye kitna DAP aur Urea lagega?');

  // Test 4: Hardware / Tech Programming
  await sendAndAwait('arduino flame sensor relay wiring aur code batao');

  // Capture final screenshot
  const screenshotPath = '/Users/yash/.gemini/antigravity-ide/brain/f04c438d-3ad9-46ad-8c2e-0911c531ecf3/live_chrome_dom_final.png';
  await cdp.screenshot(screenshotPath);
  console.log(`\n📸 Full-page screenshot captured in Chrome: ${screenshotPath}`);

  cdp.close();
  console.log('\n🎉 ALL LIVE CHROME DOM TESTS FINISHED!');
}

main().catch(console.error);
