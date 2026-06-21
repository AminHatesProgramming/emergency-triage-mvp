const chromeDebuggerUrl = process.env.CHROME_DEBUGGER_URL || "http://127.0.0.1:9222";
const targetUrl =
  process.env.PWA_URL || "https://aminhatesprogramming.github.io/emergency-triage-mvp/";
const viewport = {
  width: Number(process.env.PWA_VIEWPORT_WIDTH || 390),
  height: Number(process.env.PWA_VIEWPORT_HEIGHT || 844),
  mobile: process.env.PWA_MOBILE !== "false",
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getWebSocketUrl() {
  const response = await fetch(`${chromeDebuggerUrl}/json/new?${encodeURIComponent("about:blank")}`, {
    method: "PUT",
  });
  if (!response.ok) {
    throw new Error(`Unable to create Chrome target: ${response.status}`);
  }
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
          return new Promise((res, rej) => {
            callbacks.set(id, { res, rej, method });
          });
        },
        waitEvent(method, timeoutMs = 20000) {
          const existingIndex = events.findIndex((event) => event.method === method);
          if (existingIndex !== -1) {
            return Promise.resolve(events.splice(existingIndex, 1)[0]);
          }
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
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.text || "Runtime evaluation failed");
  }
  return result.result.value;
}

async function runScenario(client, scenarioName) {
  return evaluate(
    client,
    `(async () => {
      const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      const until = async (predicate, timeout = 20000) => {
        const started = Date.now();
        while (Date.now() - started < timeout) {
          if (predicate()) return true;
          await wait(150);
        }
        return false;
      };
      document.querySelector('#clearBtn')?.click();
      await wait(150);
      document.querySelector('[data-scenario="${scenarioName}"]').click();
      await wait(250);
      document.querySelector('#triageForm').requestSubmit();
      const ok = await until(() => {
        const value = document.querySelector('#riskPercent')?.textContent?.trim();
        return value && value !== '--';
      });
      if (!ok) throw new Error('Prediction did not render');
      return {
        scenario: '${scenarioName}',
        status: document.querySelector('#apiStatus')?.textContent?.trim(),
        risk: document.querySelector('#riskLabel')?.textContent?.trim(),
        percent: document.querySelector('#riskPercent')?.textContent?.trim(),
        confidence: document.querySelector('#confidenceBand')?.textContent?.trim(),
        completeness: document.querySelector('#dataQuality')?.textContent?.trim(),
        triageBand: document.querySelector('#triageBand')?.textContent?.trim(),
        missingFields: document.querySelector('#missingFields')?.textContent?.trim(),
      };
    })()`,
  );
}

async function main() {
  const wsUrl = await getWebSocketUrl();
  const client = await connect(wsUrl);
  try {
    await client.send("Page.enable");
    await client.send("Runtime.enable");
    await client.send("Emulation.setDeviceMetricsOverride", {
      width: viewport.width,
      height: viewport.height,
      deviceScaleFactor: viewport.mobile ? 2 : 1,
      mobile: viewport.mobile,
    });
    await client.send("Page.navigate", { url: targetUrl });
    await client.waitEvent("Page.loadEventFired", 30000);
    await sleep(2500);

    const pageInfo = await evaluate(
      client,
      `({
        title: document.title,
        url: location.href,
        readyState: document.readyState,
        configApiBase: window.TRIAGE_APP_CONFIG?.API_BASE_URL || '',
        hasManifest: !!document.querySelector('link[rel="manifest"]'),
        hasServiceWorker: 'serviceWorker' in navigator,
        localNetworkRequests: performance.getEntriesByType('resource')
          .map((entry) => entry.name)
          .filter((name) => name.includes('localhost') || name.includes('127.0.0.1')),
      })`,
    );
    const critical = await runScenario(client, "critical");
    const sparse = await runScenario(client, "sparse");

    console.log(
      JSON.stringify(
        {
          viewport,
          pageInfo,
          scenarios: { critical, sparse },
        },
        null,
        2,
      ),
    );
  } finally {
    client.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
