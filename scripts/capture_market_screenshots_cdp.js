const fs = require("fs");
const path = require("path");

const chromeDebuggerUrl = process.env.CHROME_DEBUGGER_URL || "http://127.0.0.1:9222";
const targetUrl = process.env.PWA_URL || "http://127.0.0.1:8765/";
const outputDir = process.env.SCREENSHOT_DIR || "docs/market/screenshots";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getWebSocketUrl() {
  const response = await fetch(`${chromeDebuggerUrl}/json/new?${encodeURIComponent("about:blank")}`, {
    method: "PUT",
  });
  if (!response.ok) throw new Error(`Unable to create Chrome target: ${response.status}`);
  const target = await response.json();
  return target.webSocketDebuggerUrl;
}

async function connect(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    const callbacks = new Map();
    const events = [];
    let nextId = 1;

    ws.onopen = () => {
      resolve({
        send(method, params = {}) {
          const id = nextId++;
          ws.send(JSON.stringify({ id, method, params }));
          return new Promise((res, rej) => callbacks.set(id, { res, rej, method }));
        },
        waitEvent(method, timeoutMs = 20000) {
          const existingIndex = events.findIndex((event) => event.method === method);
          if (existingIndex !== -1) return Promise.resolve(events.splice(existingIndex, 1)[0]);
          return new Promise((res, rej) => {
            const timeout = setTimeout(() => rej(new Error(`Timed out waiting for ${method}`)), timeoutMs);
            const interval = setInterval(() => {
              const index = events.findIndex((event) => event.method === method);
              if (index !== -1) {
                clearInterval(interval);
                clearTimeout(timeout);
                res(events.splice(index, 1)[0]);
              }
            }, 50);
          });
        },
        close() {
          ws.close();
        },
      });
    };
    ws.onerror = (event) => reject(event.error || new Error("Chrome websocket error"));
    ws.onmessage = (message) => {
      const payload = JSON.parse(message.data);
      if (payload.id && callbacks.has(payload.id)) {
        const callback = callbacks.get(payload.id);
        callbacks.delete(payload.id);
        if (payload.error) callback.rej(new Error(`${callback.method}: ${payload.error.message}`));
        else callback.res(payload.result);
        return;
      }
      if (payload.method) events.push(payload);
    };
  });
}

async function evaluate(client, expression) {
  const result = await client.send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text || "Runtime evaluation failed");
  return result.result.value;
}

async function navigate(client, viewport) {
  await client.send("Emulation.setDeviceMetricsOverride", viewport);
  await client.send("Page.navigate", { url: targetUrl });
  await client.waitEvent("Page.loadEventFired", 30000);
  await sleep(2200);
  await evaluate(
    client,
    `(() => {
      const notice = document.querySelector('#safetyNotice');
      if (notice && !notice.hidden) document.querySelector('#acceptSafetyNotice')?.click();
      return true;
    })()`,
  );
  await sleep(750);
}

async function runScenario(client, name) {
  await evaluate(
    client,
    `(async () => {
      const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      document.querySelector('#clearBtn')?.click();
      await wait(120);
      document.querySelector('[data-scenario="${name}"]')?.click();
      await wait(250);
      document.querySelector('#triageForm')?.requestSubmit();
      const started = Date.now();
      while (Date.now() - started < 15000) {
        const text = document.querySelector('#riskPercent')?.textContent || '';
        if (text.trim() && !text.includes('--')) {
          const panel = document.querySelector('#resultPanel');
          const panelTop = panel.getBoundingClientRect().top + window.scrollY;
          const offset = window.innerWidth <= 600 ? 16 : 118;
          window.scrollTo(0, Math.max(0, panelTop - offset));
          await wait(300);
          return true;
        }
        await wait(150);
      }
      throw new Error('scenario did not render');
    })()`,
  );
}

async function runHeartRate150Scenario(client) {
  await evaluate(
    client,
    `(async () => {
      const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      document.querySelector('#clearBtn')?.click();
      await wait(120);
      const form = document.querySelector('#triageForm');
      const values = {
        age: 30,
        heart_rate: 150,
        systolic_bp: 120,
        diastolic_bp: 80,
        respiratory_rate: 16,
        oxygen_saturation: 98,
        temperature: 36.8,
      };
      Object.entries(values).forEach(([name, value]) => {
        form.elements[name].value = value;
      });
      form.requestSubmit();
      const started = Date.now();
      while (Date.now() - started < 15000) {
        if (document.querySelector('#riskPercent')?.textContent?.trim() === 'فوری') {
          const panel = document.querySelector('#resultPanel');
          const panelTop = panel.getBoundingClientRect().top + window.scrollY;
          const offset = window.innerWidth <= 600 ? 16 : 118;
          window.scrollTo(0, Math.max(0, panelTop - offset));
          await wait(250);
          return true;
        }
        await wait(150);
      }
      throw new Error('heart-rate-150 scenario did not render as immediate');
    })()`,
  );
}

async function capture(client, filename) {
  await sleep(1100);
  await client.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: false });
  await sleep(450);
  const result = await client.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: false });
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(path.join(outputDir, filename), Buffer.from(result.data, "base64"));
}

async function mainCdp() {
  const client = await connect(await getWebSocketUrl());
  try {
    await client.send("Page.enable");
    await client.send("Runtime.enable");

    await navigate(client, { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
    await capture(client, "emdadyar-mobile-empty.png");
    await runScenario(client, "critical");
    await capture(client, "emdadyar-mobile-critical.png");
    await runScenario(client, "sparse");
    await capture(client, "emdadyar-mobile-partial-input.png");
    await runHeartRate150Scenario(client);
    await capture(client, "emdadyar-mobile-heart-rate-150.png");

    await navigate(client, { width: 1366, height: 900, deviceScaleFactor: 1, mobile: false });
    await runScenario(client, "critical");
    await capture(client, "emdadyar-desktop-critical.png");

    console.log(JSON.stringify({ outputDir, files: fs.readdirSync(outputDir).sort() }, null, 2));
  } finally {
    client.close();
  }
}

function chromeExecutable(chromium) {
  return [
    process.env.CHROME_EXECUTABLE,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    chromium.executablePath(),
  ].find((candidate) => candidate && fs.existsSync(candidate));
}

async function preparePlaywrightPage(browser, options) {
  const context = await browser.newContext(options);
  const page = await context.newPage();
  await page.goto(targetUrl, { waitUntil: "networkidle" });
  await page.locator("#acceptSafetyNotice").click({ timeout: 3000 }).catch(() => {});
  await page.waitForTimeout(500);
  return { context, page };
}

async function runPlaywrightScenario(page, name) {
  await page.evaluate(async (scenarioName) => {
    const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    document.querySelector("#clearBtn")?.click();
    await wait(120);
    document.querySelector(`[data-scenario="${scenarioName}"]`)?.click();
    await wait(250);
    document.querySelector("#triageForm")?.requestSubmit();
    const started = Date.now();
    while (Date.now() - started < 15000) {
      const text = document.querySelector("#riskPercent")?.textContent || "";
      if (text.trim() && !text.includes("--")) {
        const panel = document.querySelector("#resultPanel");
        const panelTop = panel.getBoundingClientRect().top + window.scrollY;
        const offset = window.innerWidth <= 600 ? 16 : 118;
        window.scrollTo(0, Math.max(0, panelTop - offset));
        await wait(300);
        return;
      }
      await wait(150);
    }
    throw new Error(`Scenario ${scenarioName} did not render.`);
  }, name);
}

async function runPlaywrightHeartRate150(page) {
  await page.evaluate(async () => {
    const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    document.querySelector("#clearBtn")?.click();
    await wait(120);
    const form = document.querySelector("#triageForm");
    const values = {
      age: 30,
      heart_rate: 150,
      systolic_bp: 120,
      diastolic_bp: 80,
      respiratory_rate: 16,
      oxygen_saturation: 98,
      temperature: 36.8,
    };
    Object.entries(values).forEach(([name, value]) => {
      form.elements[name].value = value;
    });
    form.requestSubmit();
    const started = Date.now();
    while (Date.now() - started < 15000) {
      if (document.querySelector("#riskPercent")?.textContent?.trim() === "فوری") {
        const panel = document.querySelector("#resultPanel");
        const panelTop = panel.getBoundingClientRect().top + window.scrollY;
        const offset = window.innerWidth <= 600 ? 16 : 118;
        window.scrollTo(0, Math.max(0, panelTop - offset));
        await wait(300);
        return;
      }
      await wait(150);
    }
    throw new Error("Heart-rate-150 scenario did not render as immediate.");
  });
}

async function mainPlaywright() {
  const { chromium } = require("playwright");
  const executablePath = chromeExecutable(chromium);
  if (!executablePath) throw new Error("No Chromium-compatible browser executable was found.");
  const browser = await chromium.launch({ headless: true, executablePath });
  fs.mkdirSync(outputDir, { recursive: true });
  try {
    const mobile = await preparePlaywrightPage(browser, {
      viewport: { width: 390, height: 844 },
      deviceScaleFactor: 2,
      isMobile: true,
      hasTouch: true,
    });
    try {
      await mobile.page.screenshot({ path: path.join(outputDir, "emdadyar-mobile-empty.png") });
      await runPlaywrightScenario(mobile.page, "critical");
      await mobile.page.screenshot({ path: path.join(outputDir, "emdadyar-mobile-critical.png") });
      await runPlaywrightScenario(mobile.page, "sparse");
      await mobile.page.screenshot({ path: path.join(outputDir, "emdadyar-mobile-partial-input.png") });
      await runPlaywrightHeartRate150(mobile.page);
      await mobile.page.screenshot({ path: path.join(outputDir, "emdadyar-mobile-heart-rate-150.png") });
    } finally {
      await mobile.context.close();
    }

    const desktop = await preparePlaywrightPage(browser, {
      viewport: { width: 1366, height: 900 },
      deviceScaleFactor: 1,
    });
    try {
      await runPlaywrightScenario(desktop.page, "critical");
      await desktop.page.screenshot({ path: path.join(outputDir, "emdadyar-desktop-critical.png") });
    } finally {
      await desktop.context.close();
    }
  } finally {
    await browser.close();
  }
  console.log(JSON.stringify({ outputDir, files: fs.readdirSync(outputDir).sort() }, null, 2));
}

(async () => {
  try {
    await mainCdp();
  } catch (error) {
    console.warn(`CDP unavailable (${error.message}); using headless Chromium.`);
    await mainPlaywright();
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
