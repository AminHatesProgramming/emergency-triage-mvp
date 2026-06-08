const API_BASE = window.location.protocol === "file:" ? "http://127.0.0.1:8000" : "";

const scenarios = {
  critical: {
    chief_complaint: "shortnessofbreath",
    age: 72,
    gender: "Female",
    arrivalmode: "Ambulance",
    heart_rate: 118,
    systolic_bp: 92,
    diastolic_bp: 58,
    respiratory_rate: 28,
    oxygen_saturation: 88,
    temperature: 38.4,
    previous_ed_visits: 2,
    previous_admissions: 1,
    previous_surgeries: 1,
    history_conditions: ["copd", "chfnonhp"],
  },
  moderate: {
    chief_complaint: "fever",
    age: 34,
    gender: "Male",
    arrivalmode: "Walk-in",
    heart_rate: 94,
    systolic_bp: 124,
    diastolic_bp: 78,
    respiratory_rate: 18,
    oxygen_saturation: 97,
    temperature: 38.1,
    previous_ed_visits: 0,
    previous_admissions: 0,
    previous_surgeries: 0,
    history_conditions: ["asthma"],
  },
  sparse: {
    chief_complaint: "chestpain",
    age: 63,
    heart_rate: 112,
    oxygen_saturation: 91,
    history_conditions: ["coronathero"],
  },
};

const form = document.querySelector("#triageForm");
const apiStatus = document.querySelector("#apiStatus");
const riskPercent = document.querySelector("#riskPercent");
const riskLabel = document.querySelector("#riskLabel");
const riskAction = document.querySelector("#riskAction");
const gaugeRing = document.querySelector("#gaugeRing");
const explanations = document.querySelector("#explanations");
const dataQuality = document.querySelector("#dataQuality");
const qualityBar = document.querySelector("#qualityBar");
const confidenceBand = document.querySelector("#confidenceBand");
const missingFields = document.querySelector("#missingFields");

function setStatus(ok) {
  apiStatus.textContent = ok ? "سرویس آماده است" : "اتصال API برقرار نیست";
  apiStatus.className = `status-pill ${ok ? "ok" : "fail"}`;
}

async function checkApi() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    setStatus(res.ok);
  } catch {
    setStatus(false);
  }
}

function readPayload() {
  const data = new FormData(form);
  const payload = {};
  for (const [key, value] of data.entries()) {
    if (value === "") continue;
    if (key === "history_conditions") {
      if (!payload.history_conditions) payload.history_conditions = [];
      payload.history_conditions.push(value);
      continue;
    }
    const input = form.elements[key];
    payload[key] = input && input.type === "number" ? Number(value) : value;
  }
  return payload;
}

function fillScenario(name) {
  form.reset();
  const scenario = scenarios[name];
  Object.entries(scenario).forEach(([key, value]) => {
    if (key === "history_conditions") {
      value.forEach((condition) => {
        const checkbox = form.querySelector(`input[name="history_conditions"][value="${condition}"]`);
        if (checkbox) checkbox.checked = true;
      });
      return;
    }
    if (form.elements[key]) form.elements[key].value = value;
  });
}

function bandLabel(value) {
  if (value === "high") return "اعتماد بالا";
  if (value === "medium") return "اعتماد متوسط";
  return "داده محدود";
}

function updateResult(result) {
  const percent = Math.round(result.critical_probability * 100);
  const degrees = Math.round(result.critical_probability * 360);
  const color = result.risk_level === "critical" ? "#c93535" : "#17845b";

  riskPercent.textContent = `${percent}%`;
  gaugeRing.style.background = `radial-gradient(circle at center, #fff 56%, transparent 57%), conic-gradient(${color} ${degrees}deg, #e3ecef 0deg)`;
  riskLabel.textContent = result.risk_level === "critical" ? "پرخطر / نیازمند توجه فوری" : "فعلا غیر بحرانی";
  riskAction.textContent = result.recommended_action;

  explanations.innerHTML = "";
  result.explanation.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    explanations.appendChild(li);
  });

  dataQuality.textContent = `${Math.round(result.data_completeness * 100)}%`;
  qualityBar.style.width = `${Math.round(result.data_completeness * 100)}%`;
  confidenceBand.textContent = bandLabel(result.confidence_band);
  missingFields.textContent = result.missing_recommended_fields.length
    ? result.missing_recommended_fields.join("، ")
    : "ورودی‌های کلیدی کامل هستند.";
}

async function submitForm(event) {
  event.preventDefault();
  riskLabel.textContent = "در حال ارزیابی";
  riskAction.textContent = "لطفا چند لحظه صبر کنید.";
  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(readPayload()),
    });
    if (!res.ok) throw new Error("prediction failed");
    updateResult(await res.json());
    setStatus(true);
  } catch {
    setStatus(false);
    riskLabel.textContent = "خطا در ارتباط";
    riskAction.textContent = "ابتدا API را اجرا کنید.";
  }
}

function drawSignal() {
  const canvas = document.querySelector("#signalCanvas");
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.floor(window.innerWidth * dpr);
  canvas.height = Math.floor(window.innerHeight * dpr);
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
  ctx.strokeStyle = "rgba(8, 127, 140, 0.22)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  const y = window.innerHeight * 0.18;
  for (let x = 0; x < window.innerWidth; x += 18) {
    const pulse = x % 180;
    const offset = pulse === 72 ? -42 : pulse === 90 ? 34 : Math.sin(x / 34) * 8;
    if (x === 0) ctx.moveTo(x, y + offset);
    else ctx.lineTo(x, y + offset);
  }
  ctx.stroke();
}

document.querySelectorAll("[data-scenario]").forEach((button) => {
  button.addEventListener("click", () => fillScenario(button.dataset.scenario));
});

document.querySelector("#clearBtn").addEventListener("click", () => {
  form.reset();
  riskPercent.textContent = "--";
  riskLabel.textContent = "در انتظار ورودی";
  riskAction.textContent = "مدل فقط نقش پشتیبان تصمیم دارد.";
  dataQuality.textContent = "--";
  qualityBar.style.width = "0%";
  confidenceBand.textContent = "آماده";
  missingFields.textContent = "--";
  explanations.innerHTML = "<li>پس از ارزیابی نمایش داده می‌شود.</li>";
});

form.addEventListener("submit", submitForm);
window.addEventListener("resize", drawSignal);
drawSignal();
checkApi();
