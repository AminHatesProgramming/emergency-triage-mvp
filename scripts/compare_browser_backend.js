const fs = require("fs");
const path = require("path");

const chromeDebuggerUrl = process.env.CHROME_DEBUGGER_URL || "http://127.0.0.1:9222";
const frontendUrl = process.env.PWA_URL || "http://127.0.0.1:8765/";
const backendUrl = (process.env.BACKEND_URL || "http://127.0.0.1:8001").replace(/\/$/, "");
const probabilityTolerance = 1e-6;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function connectChrome() {
  const response = await fetch(`${chromeDebuggerUrl}/json/new?${encodeURIComponent("about:blank")}`, {
    method: "PUT",
  });
  if (!response.ok) throw new Error(`Unable to create Chrome target: ${response.status}`);
  const target = await response.json();
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    const callbacks = new Map();
    const events = [];
    let nextId = 1;
    ws.onopen = () => resolve({
      send(method, params = {}) {
        const id = nextId++;
        ws.send(JSON.stringify({ id, method, params }));
        return new Promise((res, rej) => callbacks.set(id, { res, rej, method }));
      },
      waitEvent(method, timeoutMs = 30000) {
        return new Promise((res, rej) => {
          const started = Date.now();
          const timer = setInterval(() => {
            const index = events.findIndex((event) => event.method === method);
            if (index !== -1) {
              clearInterval(timer);
              res(events.splice(index, 1)[0]);
            } else if (Date.now() - started > timeoutMs) {
              clearInterval(timer);
              rej(new Error(`Timed out waiting for ${method}`));
            }
          }, 50);
        });
      },
      close() { ws.close(); },
    });
    ws.onerror = () => reject(new Error("Chrome websocket error"));
    ws.onmessage = (message) => {
      const payload = JSON.parse(message.data);
      if (payload.id && callbacks.has(payload.id)) {
        const callback = callbacks.get(payload.id);
        callbacks.delete(payload.id);
        if (payload.error) callback.rej(new Error(`${callback.method}: ${payload.error.message}`));
        else callback.res(payload.result);
      } else if (payload.method) {
        events.push(payload);
      }
    };
  });
}

async function evaluate(client, expression) {
  const result = await client.send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text || "Browser evaluation failed");
  return result.result.value;
}

function buildScenarios() {
  const normal = {
    chief_complaint: "abdominalpain",
    age: 30,
    gender: "Female",
    arrivalmode: "Walk-in",
    heart_rate: 78,
    systolic_bp: 120,
    diastolic_bp: 75,
    respiratory_rate: 16,
    oxygen_saturation: 98,
    temperature: 36.8,
    previous_ed_visits: null,
    previous_admissions: null,
    previous_surgeries: null,
    oxygen_device: 0,
    history_conditions: [],
  };
  const scenarios = [{ name: "normal_adult", payload: normal }];
  const ages = [0.1, 0.4, 0.5, 1, 3, 5, 6, 8, 12, 15.9, 16, 30, 65, 90];
  const boundaries = {
    heart_rate: [20, 39, 40, 50, 60, 90, 110, 111, 129, 130, 149, 150, 180, 219, 220, 250],
    systolic_bp: [40, 69, 70, 79, 80, 89, 90, 91, 100, 101, 110, 120, 220, 260],
    respiratory_rate: [3, 8, 9, 11, 12, 20, 21, 24, 25, 29, 30, 40, 50, 60, 70],
    oxygen_saturation: [50, 80, 89, 90, 91, 93, 94, 95, 96, 100],
    temperature: [30, 35, 35.9, 36, 37.9, 38, 39, 39.1, 40, 43],
  };
  for (const age of ages) {
    for (const [field, values] of Object.entries(boundaries)) {
      for (const value of values) {
        scenarios.push({
          name: `boundary_${field}_${age}_${value}`,
          payload: { ...normal, age, [field]: value },
        });
      }
    }
  }
  scenarios.push(
    { name: "fever_alias", payload: { ...normal, chief_complaint: "fever" } },
    { name: "headache_alias", payload: { ...normal, chief_complaint: "headache" } },
    { name: "elderly_fall_alias", payload: { ...normal, age: 70, chief_complaint: "fall" } },
    {
      name: "cardiac_history_rule",
      payload: { ...normal, age: 68, chief_complaint: "chestpain", history_conditions: ["coronathero"] },
    },
    {
      name: "inconsistent_bp",
      payload: { ...normal, systolic_bp: 100, diastolic_bp: 105 },
    },
    {
      name: "sparse_four",
      payload: {
        chief_complaint: "chestpain",
        age: 63,
        heart_rate: 112,
        oxygen_saturation: 91,
        history_conditions: [],
      },
    },
  );

  let state = 20260716;
  const random = () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 2 ** 32;
  };
  const pick = (items) => items[Math.floor(random() * items.length)];
  for (let index = 0; index < 250; index += 1) {
    const payload = {
      ...normal,
      chief_complaint: pick(["chestpain", "shortnessofbreath", "fever", "headache", "fall", "weakness", ""]),
      age: pick(ages),
      heart_rate: pick([...boundaries.heart_rate, null]),
      systolic_bp: pick([...boundaries.systolic_bp, null]),
      diastolic_bp: pick([20, 40, 60, 80, 100, 140, 160, null]),
      respiratory_rate: pick([...boundaries.respiratory_rate, null]),
      oxygen_saturation: pick([...boundaries.oxygen_saturation, null]),
      temperature: pick([...boundaries.temperature, null]),
      oxygen_device: pick([0, 0, 0, 1]),
      history_conditions: pick([[], ["htn"], ["copd"], ["coronathero", "acutemi"]]),
    };
    if (!payload.chief_complaint && ["heart_rate", "systolic_bp", "respiratory_rate", "oxygen_saturation", "temperature"].every((key) => payload[key] === null)) {
      payload.heart_rate = 78;
    }
    scenarios.push({ name: `seeded_random_${index + 1}`, payload });
  }
  return scenarios;
}

async function backendPredictions(scenarios) {
  const outputs = [];
  for (let start = 0; start < scenarios.length; start += 20) {
    const batch = scenarios.slice(start, start + 20);
    const results = await Promise.all(batch.map(async (scenario) => {
      const response = await fetch(`${backendUrl}/predict`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(scenario.payload),
      });
      if (!response.ok) throw new Error(`${scenario.name}: backend ${response.status} ${await response.text()}`);
      return response.json();
    }));
    outputs.push(...results);
  }
  return outputs;
}

function sameArray(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

async function main() {
  const requestedLimit = Number(process.env.SCENARIO_LIMIT || 0);
  const allScenarios = buildScenarios();
  const scenarios = requestedLimit > 0 ? allScenarios.slice(0, requestedLimit) : allScenarios;
  const client = await connectChrome();
  let browserOutputs;
  try {
    await client.send("Page.enable");
    await client.send("Runtime.enable");
    await client.send("Network.enable");
    await client.send("Network.setCacheDisabled", { cacheDisabled: true });
    await client.send("Network.setBypassServiceWorker", { bypass: true });
    await client.send("Network.clearBrowserCache");
    await client.send("Page.navigate", { url: `${frontendUrl}?qa=${Date.now()}` });
    await client.waitEvent("Page.loadEventFired");
    await sleep(1200);
    browserOutputs = await evaluate(
      client,
      `(async () => Promise.all(${JSON.stringify(scenarios.map((item) => item.payload))}.map((payload) => predictInBrowser(payload))))()`,
    );
  } finally {
    client.close();
  }
  const apiOutputs = await backendPredictions(scenarios);
  const mismatches = [];
  let maxProbabilityDifference = 0;
  scenarios.forEach((scenario, index) => {
    const browser = browserOutputs[index];
    const api = apiOutputs[index];
    const probabilityDifference = Math.abs(browser.model_probability - api.model_probability);
    maxProbabilityDifference = Math.max(maxProbabilityDifference, probabilityDifference);
    const differences = [];
    if (probabilityDifference > probabilityTolerance) differences.push(`model_probability:${probabilityDifference}`);
    if (Math.abs(browser.threshold - api.threshold) > Number.EPSILON) differences.push("threshold");
    for (const key of ["risk_level", "safety_severity", "assessment_basis", "operating_profile", "safety_rule_version", "out_of_distribution"]) {
      if (browser[key] !== api[key]) differences.push(`${key}:${browser[key]}!=${api[key]}`);
    }
    if (!sameArray(browser.safety_flags, api.safety_flags)) differences.push("safety_flags");
    if (!sameArray(browser.measurement_warnings, api.measurement_warnings)) differences.push("measurement_warnings");
    if (differences.length) mismatches.push({ name: scenario.name, payload: scenario.payload, differences, browser, api });
  });

  const report = {
    generated_at_utc: new Date().toISOString(),
    frontend_url: frontendUrl,
    backend_url: backendUrl,
    model_version: apiOutputs[0]?.model_version,
    safety_rule_version: apiOutputs[0]?.safety_rule_version,
    scenario_count: scenarios.length,
    probability_tolerance: probabilityTolerance,
    max_probability_difference: maxProbabilityDifference,
    mismatch_count: mismatches.length,
    passed: mismatches.length === 0,
    mismatch_sample: mismatches.slice(0, 20),
  };
  const outputName = requestedLimit > 0
    ? "browser_backend_differential_debug_v7.json"
    : "browser_backend_differential_v7.json";
  const outputPath = path.resolve("reports", "model", outputName);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2), "utf8");
  console.log(JSON.stringify(report, null, 2));
  if (!report.passed) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
