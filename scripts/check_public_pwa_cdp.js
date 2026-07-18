const fs = require("fs");
const path = require("path");

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
    await client.send("Network.enable");
    await client.send("Network.setCacheDisabled", { cacheDisabled: true });
    await client.send("Network.setBypassServiceWorker", { bypass: true });
    await client.send("Page.addScriptToEvaluateOnNewDocument", {
      source: `
        window.__emdadyarReleaseErrors = [];
        window.addEventListener('error', (event) => {
          window.__emdadyarReleaseErrors.push(String(event.message || event.error || 'window error'));
        });
        window.addEventListener('unhandledrejection', (event) => {
          window.__emdadyarReleaseErrors.push(String(event.reason || 'unhandled rejection'));
        });
      `,
    });
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

    const copySummary = await evaluate(
      client,
      `(async () => {
        window.__emdadyarCopiedSummary = '';
        Object.defineProperty(navigator, 'clipboard', {
          configurable: true,
          value: {
            writeText: async (value) => {
              window.__emdadyarCopiedSummary = String(value || '');
            },
          },
        });
        document.querySelector('#copyCaseBtn')?.click();
        await new Promise((resolve) => setTimeout(resolve, 100));
        return {
          buttonLabel: document.querySelector('#copyCaseBtn')?.textContent?.trim(),
          copiedLength: window.__emdadyarCopiedSummary.length,
          containsDisclaimer: window.__emdadyarCopiedSummary.includes('پشتیبان تصمیم'),
        };
      })()`,
    );

    const evaluatorChecks = await evaluate(
      client,
      `(async () => {
        const base = {
          chief_complaint: 'abdominalpain', age: 30, gender: 'Female', arrivalmode: 'Walk-in',
          heart_rate: 78, systolic_bp: 120, diastolic_bp: 75, respiratory_rate: 16,
          oxygen_saturation: 98, temperature: 36.8, previous_ed_visits: null,
          previous_admissions: null, previous_surgeries: null, oxygen_device: 0,
          history_conditions: [],
        };
        const sparsePayload = {
          ...base, chief_complaint: 'shortnessofbreath', age: null, heart_rate: 125,
          oxygen_saturation: 92, systolic_bp: null, diastolic_bp: null,
          respiratory_rate: null, temperature: null,
        };
        const sparse3 = await predictInBrowser(sparsePayload);
        const sparse4 = await predictInBrowser({ ...sparsePayload, age: 68 });
        const heartRate150 = await predictInBrowser({ ...base, heart_rate: 150 });
        const normal = await predictInBrowser(base);
        return {
          sparse3: {
            profile: sparse3.operating_profile,
            threshold: sparse3.threshold,
            risk: sparse3.risk_level,
          },
          sparse4: {
            profile: sparse4.operating_profile,
            threshold: sparse4.threshold,
            risk: sparse4.risk_level,
          },
          heartRate150: {
            profile: heartRate150.operating_profile,
            risk: heartRate150.risk_level,
            safetyOverride: heartRate150.safety_override,
            severity: heartRate150.safety_severity,
            reasons: heartRate150.safety_flags,
          },
          normal: {
            profile: normal.operating_profile,
            risk: normal.risk_level,
            safetyOverride: normal.safety_override,
          },
          runtimeErrors: window.__emdadyarReleaseErrors || [],
        };
      })()`,
    );

    const documentReset = await evaluate(
      client,
      `(() => {
        document.querySelector('#clearBtn')?.click();
        return {
          riskPercent: document.querySelector('#riskPercent')?.textContent?.trim(),
          selectedScenario: document.querySelector('[data-scenario].is-active')?.dataset?.scenario || null,
        };
      })()`,
    );

    const checks = {
      title: pageInfo.title.includes("امداد یار"),
      loaded: pageInfo.readyState === "complete",
      manifest: pageInfo.hasManifest,
      serviceWorkerCapability: pageInfo.hasServiceWorker,
      noRuntimeErrors: evaluatorChecks.runtimeErrors.length === 0,
      criticalScenarioRendered: critical.percent !== "--" && Boolean(critical.triageBand),
      sparseScenarioRendered: sparse.percent !== "--" && Boolean(sparse.missingFields),
      caseSummaryCopyWorks:
        copySummary.buttonLabel === "کپی شد"
        && copySummary.copiedLength > 30
        && copySummary.containsDisclaimer,
      sparse3Profile: evaluatorChecks.sparse3.profile === "validated_sparse_3",
      sparse4Profile: evaluatorChecks.sparse4.profile === "validated_sparse_4",
      heartRate150Escalates:
        evaluatorChecks.heartRate150.risk === "critical"
        && evaluatorChecks.heartRate150.safetyOverride === true
        && evaluatorChecks.heartRate150.severity === "immediate",
      normalDoesNotSafetyEscalate: evaluatorChecks.normal.safetyOverride === false,
      clearResetsResult: documentReset.riskPercent === "--",
    };

    const report = {
      generated_at: new Date().toISOString(),
      targetUrl,
      viewport,
      pageInfo,
      scenarios: { critical, sparse },
      copySummary,
      evaluatorChecks,
      documentReset,
      checks,
      passed: Object.values(checks).every(Boolean),
    };

    const reportPath = path.resolve(__dirname, "..", "reports", "model", "ui_smoke_v7.json");
    fs.mkdirSync(path.dirname(reportPath), { recursive: true });
    fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");

    console.log(JSON.stringify(report, null, 2));
    if (!report.passed) process.exitCode = 1;
  } finally {
    client.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
