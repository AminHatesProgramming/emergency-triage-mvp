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
  cardiac: {
    chief_complaint: "chestpain",
    age: 68,
    gender: "Male",
    arrivalmode: "Walk-in",
    heart_rate: 106,
    systolic_bp: 104,
    diastolic_bp: 64,
    respiratory_rate: 22,
    oxygen_saturation: 95,
    temperature: 36.8,
    previous_ed_visits: 1,
    previous_admissions: 1,
    previous_surgeries: 0,
    history_conditions: ["coronathero", "acutemi"],
  },
};

const translations = {
  "red flag: oxygen saturation below 90%": "پرچم قرمز: اکسیژن خون کمتر از ۹۰٪",
  "warning: oxygen saturation below normal triage range": "هشدار: اکسیژن خون پایین‌تر از محدوده طبیعی تریاژ",
  "red flag: systolic blood pressure below 90": "پرچم قرمز: فشار سیستولیک کمتر از ۹۰",
  "red flag: severely abnormal respiratory rate": "پرچم قرمز: نرخ تنفس به‌شدت غیرطبیعی",
  "red flag: severely abnormal heart rate": "پرچم قرمز: ضربان قلب به‌شدت غیرطبیعی",
  "red flag: extreme body temperature": "پرچم قرمز: دمای بدن در محدوده بحرانی",
  "red flag: chest pain with high-risk cardiac history": "پرچم قرمز: درد قفسه سینه همراه با سابقه قلبی پرخطر",
  "low oxygen saturation": "اشباع اکسیژن پایین",
  "elevated shock index": "شاخص شوک بالا",
  "abnormal respiratory rate": "نرخ تنفس غیرطبیعی",
  "elderly patient": "بیمار سالمند",
  "no single dominant risk factor identified": "عامل غالب مشخصی شناسایی نشد",
  "notify senior triage nurse or emergency physician": "اطلاع به پرستار ارشد تریاژ یا پزشک اورژانس",
  "repeat vital signs and keep patient in visible monitored area": "تکرار علائم حیاتی و نگهداری بیمار در محدوده قابل مشاهده",
  "continue standard triage pathway and document model output": "ادامه مسیر استاندارد تریاژ و ثبت خروجی مدل",
  "treat safety flags as clinical prompts, not automated diagnosis": "پرچم‌های ایمنی به‌عنوان هشدار بالینی تفسیر شوند، نه تشخیص خودکار",
  "collect the highest-value missing triage fields before final disposition": "پیش از تصمیم نهایی، فیلدهای کلیدی باقی‌مانده تکمیل شوند",
};

const fieldLabels = {
  "chief complaint": "شکایت اصلی",
  age: "سن",
  "heart rate": "ضربان قلب",
  "systolic blood pressure": "فشار سیستولیک",
  "diastolic blood pressure": "فشار دیاستولیک",
  "respiratory rate": "نرخ تنفس",
  "oxygen saturation": "اکسیژن خون",
  temperature: "دما",
};

const form = document.querySelector("#triageForm");
const apiStatus = document.querySelector("#apiStatus");
const installBtn = document.querySelector("#installBtn");
const riskCard = document.querySelector("#riskCard");
const riskPercent = document.querySelector("#riskPercent");
const riskLabel = document.querySelector("#riskLabel");
const riskAction = document.querySelector("#riskAction");
const triageBand = document.querySelector("#triageBand");
const gaugeRing = document.querySelector("#gaugeRing");
const explanations = document.querySelector("#explanations");
const safetyFlags = document.querySelector("#safetyFlags");
const nextActions = document.querySelector("#nextActions");
const dataQuality = document.querySelector("#dataQuality");
const modelProbability = document.querySelector("#modelProbability");
const qualityBar = document.querySelector("#qualityBar");
const confidenceBand = document.querySelector("#confidenceBand");
const missingFields = document.querySelector("#missingFields");
const feedbackForm = document.querySelector("#feedbackForm");
const feedbackCount = document.querySelector("#feedbackCount");
const feedbackStatus = document.querySelector("#feedbackStatus");
const exportFeedbackBtn = document.querySelector("#exportFeedbackBtn");
const feedbackProgressText = document.querySelector("#feedbackProgressText");
const feedbackProgressBar = document.querySelector("#feedbackProgressBar");
const feedbackTargetText = document.querySelector("#feedbackTargetText");
const feedbackTargetBar = document.querySelector("#feedbackTargetBar");
const copyCaseBtn = document.querySelector("#copyCaseBtn");
const printCaseBtn = document.querySelector("#printCaseBtn");
const caseSummaryBox = document.querySelector("#caseSummaryBox");
const caseSummaryText = document.querySelector("#caseSummaryText");

let deferredInstallPrompt = null;
let latestResult = null;
let latestPayload = null;
const FEEDBACK_STORAGE_KEY = "triageStakeholderFeedback";

function translate(text) {
  if (!text) return "";
  if (translations[text]) return translations[text];
  if (text.startsWith("chief complaint:")) {
    return `شکایت اصلی: ${text.replace("chief complaint:", "").trim()}`;
  }
  if (text.startsWith("known history:")) {
    return `سابقه ثبت‌شده: ${text.replace("known history:", "").trim()}`;
  }
  return text;
}

function renderList(element, items, emptyText) {
  element.innerHTML = "";
  const safeItems = items && items.length ? items : [emptyText];
  safeItems.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = translate(item);
    element.appendChild(li);
  });
}

function setStatus(ok) {
  const offline = !navigator.onLine;
  apiStatus.textContent = offline
    ? "آفلاین"
    : ok
      ? "سرویس آماده است"
      : "API در دسترس نیست";
  apiStatus.className = `status-pill ${offline ? "offline" : ok ? "ok" : "fail"}`;
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
  document.querySelector("#resultPanel").scrollIntoView({ behavior: "smooth", block: "start" });
}

function bandLabel(value) {
  if (value === "high") return "اعتماد بالا";
  if (value === "medium") return "اعتماد متوسط";
  return "داده محدود";
}

function bandPersian(value) {
  if (value.includes("ESI 1-2")) return "پیشنهاد اولویت ESI 1-2";
  return "مسیر استاندارد ESI 3-5";
}

function updateResult(result) {
  latestResult = result;
  latestPayload = readPayload();
  const percent = Math.round(result.critical_probability * 100);
  const rawPercent = Math.round(result.model_probability * 100);
  const degrees = Math.round(result.critical_probability * 360);
  const critical = result.risk_level === "critical";
  const color = critical ? "var(--red)" : "var(--green)";

  riskCard.classList.toggle("critical", critical);
  riskPercent.textContent = `${percent}%`;
  modelProbability.textContent = `${rawPercent}%`;
  gaugeRing.style.background = `radial-gradient(circle at center, #fff 55%, transparent 56%), conic-gradient(${color} ${degrees}deg, #dfe8eb 0deg)`;
  riskLabel.textContent = critical ? "پرخطر / نیازمند توجه فوری" : "فعلا غیر بحرانی";
  triageBand.textContent = bandPersian(result.triage_band || "");
  riskAction.textContent = critical ? "بازبینی سریع بالینی توصیه می‌شود." : "مسیر استاندارد تریاژ ادامه پیدا کند.";

  renderList(explanations, result.explanation, "عامل غالب مشخصی شناسایی نشد.");
  renderList(safetyFlags, result.safety_flags, "پرچم ایمنی فعالی وجود ندارد.");
  renderList(nextActions, result.next_best_actions, "ادامه مسیر استاندارد تریاژ.");

  dataQuality.textContent = `${Math.round(result.data_completeness * 100)}%`;
  qualityBar.style.width = `${Math.round(result.data_completeness * 100)}%`;
  confidenceBand.textContent = result.safety_override
    ? `${bandLabel(result.confidence_band)} + Safety`
    : bandLabel(result.confidence_band);
  missingFields.textContent = result.missing_recommended_fields.length
    ? result.missing_recommended_fields.map((field) => fieldLabels[field] || field).join("، ")
    : "ورودی‌های کلیدی کامل هستند.";
  updateCaseSummary();
}

async function submitForm(event) {
  event.preventDefault();
  riskLabel.textContent = "در حال ارزیابی";
  triageBand.textContent = "لطفا چند لحظه صبر کنید.";
  riskAction.textContent = "مدل و قواعد ایمنی همزمان بررسی می‌شوند.";
  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(readPayload()),
    });
    if (!res.ok) throw new Error("prediction failed");
    updateResult(await res.json());
    setStatus(true);
    document.querySelector("#resultPanel").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch {
    setStatus(false);
    riskLabel.textContent = "خطا در ارتباط";
    triageBand.textContent = "API را اجرا کنید یا اتصال را بررسی کنید.";
    riskAction.textContent = "نسخه آفلاین فرم را نگه می‌دارد، ولی پیش‌بینی نیازمند API است.";
  }
}

function resetResult() {
  form.reset();
  latestResult = null;
  latestPayload = null;
  riskCard.classList.remove("critical");
  riskPercent.textContent = "--";
  modelProbability.textContent = "--";
  riskLabel.textContent = "در انتظار ورودی";
  triageBand.textContent = "سطح پیشنهادی پس از ارزیابی نمایش داده می‌شود.";
  riskAction.textContent = "مدل فقط نقش پشتیبان تصمیم دارد.";
  dataQuality.textContent = "--";
  qualityBar.style.width = "0%";
  confidenceBand.textContent = "آماده";
  missingFields.textContent = "--";
  renderList(explanations, [], "پس از ارزیابی نمایش داده می‌شود.");
  renderList(safetyFlags, [], "موردی ثبت نشده است.");
  renderList(nextActions, [], "پس از ارزیابی نمایش داده می‌شود.");
  caseSummaryBox.hidden = true;
  caseSummaryText.textContent = "";
}

function getFeedbackEntries() {
  try {
    return JSON.parse(localStorage.getItem(FEEDBACK_STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

function saveFeedbackEntries(entries) {
  localStorage.setItem(FEEDBACK_STORAGE_KEY, JSON.stringify(entries));
  updateFeedbackCount();
}

function updateFeedbackCount() {
  const count = getFeedbackEntries().length;
  feedbackCount.textContent = `${count} ثبت`;
  updateFeedbackProgress(count, 5);
}

function updateFeedbackProgress(count, target) {
  const safeTarget = target || 5;
  const percent = Math.min(100, Math.round((count / safeTarget) * 100));
  feedbackProgressText.textContent = `${count} / ${safeTarget}`;
  feedbackTargetText.textContent = `${count} از ${safeTarget}`;
  feedbackProgressBar.style.width = `${percent}%`;
  feedbackTargetBar.style.width = `${percent}%`;
}

async function refreshFeedbackSummary() {
  try {
    const res = await fetch(`${API_BASE}/feedback-summary`);
    if (!res.ok) throw new Error("summary failed");
    const summary = await res.json();
    feedbackCount.textContent = `${summary.stored_count} ثبت`;
    updateFeedbackProgress(summary.stored_count, summary.target_count);
  } catch {
    updateFeedbackCount();
  }
}

async function submitFeedback(event) {
  event.preventDefault();
  const data = new FormData(feedbackForm);
  const entry = {
    recorded_at: new Date().toISOString(),
    stakeholder_type: data.get("stakeholder_type"),
    understandability: Number(data.get("understandability")),
    ui_clarity: Number(data.get("ui_clarity")),
    disclaimer_clarity: Number(data.get("disclaimer_clarity")),
    comment: String(data.get("comment") || "").trim(),
  };
  try {
    const res = await fetch(`${API_BASE}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entry),
    });
    if (!res.ok) throw new Error("feedback failed");
    const result = await res.json();
    feedbackCount.textContent = `${result.stored_count} ثبت`;
    updateFeedbackProgress(result.stored_count, 5);
    feedbackStatus.textContent = "بازخورد روی سرور ثبت شد و در CSV قابل خروجی گرفتن است.";
  } catch {
    const entries = getFeedbackEntries();
    entries.push(entry);
    saveFeedbackEntries(entries);
    feedbackStatus.textContent = "API در دسترس نبود؛ بازخورد محلی ذخیره شد و CSV مرورگری دارد.";
  }
  feedbackForm.reset();
}

function formatPercent(value) {
  if (typeof value !== "number") return "--";
  return `${Math.round(value * 100)}%`;
}

function updateCaseSummary() {
  if (!latestResult) return;
  const payload = latestPayload || {};
  const riskText = latestResult.risk_level === "critical" ? "پرخطر / نیازمند توجه فوری" : "فعلا غیر بحرانی";
  const summary = [
    "Emergency Triage Decision Support - Case Summary",
    `Version: ${latestResult.model_version} (${latestResult.operational_mode})`,
    `Risk: ${riskText}`,
    `Critical probability: ${formatPercent(latestResult.critical_probability)}`,
    `Raw model probability: ${formatPercent(latestResult.model_probability)}`,
    `Confidence: ${latestResult.confidence_band}`,
    `Data completeness: ${formatPercent(latestResult.data_completeness)}`,
    `Chief complaint: ${payload.chief_complaint || "not provided"}`,
    `Age: ${payload.age ?? "not provided"}`,
    `Vitals: HR ${payload.heart_rate ?? "-"}, BP ${payload.systolic_bp ?? "-"}/${payload.diastolic_bp ?? "-"}, RR ${payload.respiratory_rate ?? "-"}, SpO2 ${payload.oxygen_saturation ?? "-"}, Temp ${payload.temperature ?? "-"}`,
    `Safety flags: ${(latestResult.safety_flags || []).join(" | ") || "none"}`,
    `Next actions: ${(latestResult.next_best_actions || []).join(" | ")}`,
    "Disclaimer: decision-support only; not a replacement for clinical judgment.",
  ].join("\n");
  caseSummaryText.textContent = summary;
  caseSummaryBox.hidden = false;
}

async function copyCaseSummary() {
  if (!caseSummaryText.textContent) {
    feedbackStatus.textContent = "ابتدا یک بیمار را ارزیابی کنید.";
    return;
  }
  try {
    await navigator.clipboard.writeText(caseSummaryText.textContent);
    copyCaseBtn.textContent = "کپی شد";
    setTimeout(() => {
      copyCaseBtn.textContent = "کپی خلاصه";
    }, 1400);
  } catch {
    caseSummaryText.focus();
  }
}

function printCaseSummary() {
  if (!caseSummaryText.textContent) {
    feedbackStatus.textContent = "ابتدا یک بیمار را ارزیابی کنید.";
    return;
  }
  window.print();
}

function csvEscape(value) {
  return `"${String(value ?? "").replaceAll('"', '""')}"`;
}

function exportFeedbackCsv() {
  const entries = getFeedbackEntries();
  if (!entries.length) {
    feedbackStatus.textContent = "هنوز بازخوردی ثبت نشده است.";
    return;
  }
  const headers = [
    "recorded_at",
    "stakeholder_type",
    "understandability",
    "ui_clarity",
    "disclaimer_clarity",
    "comment",
  ];
  const rows = [
    headers.join(","),
    ...entries.map((entry) => headers.map((key) => csvEscape(entry[key])).join(",")),
  ];
  const blob = new Blob([`\ufeff${rows.join("\n")}`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "triage-stakeholder-feedback.csv";
  anchor.click();
  URL.revokeObjectURL(url);
  feedbackStatus.textContent = "فایل CSV بازخوردها آماده شد.";
}

async function exportFeedback() {
  try {
    const res = await fetch(`${API_BASE}/feedback-summary`);
    if (!res.ok) throw new Error("summary failed");
    const summary = await res.json();
    if (summary.stored_count > 0) {
      window.location.href = `${API_BASE}/feedback/export`;
      feedbackStatus.textContent = "خروجی CSV سروری در حال دانلود است.";
      return;
    }
  } catch {
    // Use the browser-local fallback below.
  }
  exportFeedbackCsv();
}

function drawSignal() {
  const canvas = document.querySelector("#signalCanvas");
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.floor(window.innerWidth * dpr);
  canvas.height = Math.floor(window.innerHeight * dpr);
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
  ctx.strokeStyle = "rgba(6, 78, 95, 0.18)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  const base = window.innerHeight * 0.16;
  for (let x = 0; x < window.innerWidth; x += 16) {
    const pulse = x % 176;
    const offset = pulse === 64 ? -46 : pulse === 80 ? 38 : Math.sin(x / 38) * 7;
    if (x === 0) ctx.moveTo(x, base + offset);
    else ctx.lineTo(x, base + offset);
  }
  ctx.stroke();
}

document.querySelectorAll("[data-scenario]").forEach((button) => {
  button.addEventListener("click", () => fillScenario(button.dataset.scenario));
});

document.querySelectorAll("[data-jump]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector(button.dataset.jump).scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

document.querySelector("#clearBtn").addEventListener("click", resetResult);
form.addEventListener("submit", submitForm);
feedbackForm.addEventListener("submit", submitFeedback);
exportFeedbackBtn.addEventListener("click", exportFeedback);
copyCaseBtn.addEventListener("click", copyCaseSummary);
printCaseBtn.addEventListener("click", printCaseSummary);
window.addEventListener("resize", drawSignal);
window.addEventListener("online", checkApi);
window.addEventListener("offline", () => setStatus(false));

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  installBtn.hidden = false;
});

installBtn.addEventListener("click", async () => {
  if (!deferredInstallPrompt) return;
  deferredInstallPrompt.prompt();
  await deferredInstallPrompt.userChoice;
  deferredInstallPrompt = null;
  installBtn.hidden = true;
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/static/sw.js").catch(() => {});
  });
}

drawSignal();
refreshFeedbackSummary();
checkApi();
