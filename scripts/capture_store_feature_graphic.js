const fs = require("fs");
const path = require("path");

const debuggerUrl = process.env.CHROME_DEBUGGER_URL || "http://127.0.0.1:9222";
const source = path.resolve("docs/market/assets/store-feature-graphic.html");
const output = path.resolve("docs/market/release/Emdadyar-feature-graphic-1024x500.png");

async function createTarget() {
  const response = await fetch(`${debuggerUrl}/json/new?${encodeURIComponent("about:blank")}`, { method: "PUT" });
  if (!response.ok) throw new Error(`Unable to create Chrome target: ${response.status}`);
  return (await response.json()).webSocketDebuggerUrl;
}

function connect(url) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(url);
    const callbacks = new Map();
    const events = [];
    let id = 0;
    ws.onopen = () => resolve({
      send(method, params = {}) {
        const callId = ++id;
        ws.send(JSON.stringify({ id: callId, method, params }));
        return new Promise((res, rej) => callbacks.set(callId, { res, rej }));
      },
      wait(method) {
        return new Promise((res) => {
          const timer = setInterval(() => {
            const index = events.findIndex((event) => event.method === method);
            if (index >= 0) {
              clearInterval(timer);
              res(events.splice(index, 1)[0]);
            }
          }, 40);
        });
      },
      close() { ws.close(); },
    });
    ws.onerror = () => reject(new Error("Chrome websocket error"));
    ws.onmessage = ({ data }) => {
      const message = JSON.parse(data);
      if (message.id && callbacks.has(message.id)) {
        const callback = callbacks.get(message.id);
        callbacks.delete(message.id);
        if (message.error) callback.rej(new Error(message.error.message));
        else callback.res(message.result);
      } else if (message.method) {
        events.push(message);
      }
    };
  });
}

async function captureViaCdp() {
  const client = await connect(await createTarget());
  try {
    await client.send("Page.enable");
    await client.send("Emulation.setDeviceMetricsOverride", {
      width: 1024,
      height: 500,
      deviceScaleFactor: 1,
      mobile: false,
    });
    await client.send("Page.navigate", { url: `file:///${source.replace(/\\/g, "/")}` });
    await client.wait("Page.loadEventFired");
    await new Promise((resolve) => setTimeout(resolve, 900));
    const screenshot = await client.send("Page.captureScreenshot", {
      format: "png",
      captureBeyondViewport: false,
    });
    fs.mkdirSync(path.dirname(output), { recursive: true });
    fs.writeFileSync(output, Buffer.from(screenshot.data, "base64"));
  } finally {
    client.close();
  }
}

async function captureViaPlaywright() {
  const { chromium } = require("playwright");
  const executablePath = [
    process.env.CHROME_EXECUTABLE,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    chromium.executablePath(),
  ].find((candidate) => candidate && fs.existsSync(candidate));
  if (!executablePath) throw new Error("No Chromium-compatible browser executable was found.");
  const browser = await chromium.launch({
    headless: true,
    executablePath,
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1024, height: 500 } });
    await page.goto(`file:///${source.replace(/\\/g, "/")}`, { waitUntil: "load" });
    await page.screenshot({ path: output });
  } finally {
    await browser.close();
  }
}

(async () => {
  fs.mkdirSync(path.dirname(output), { recursive: true });
  try {
    await captureViaCdp();
  } catch (error) {
    console.warn(`CDP unavailable (${error.message}); using headless Chromium.`);
    await captureViaPlaywright();
  }
  console.log(output);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
