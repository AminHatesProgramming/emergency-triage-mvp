const API_BASE = window.location.protocol === "file:" ? "http://127.0.0.1:8000" : "";
const BROWSER_MODEL_URL = "static/model-v7.json";

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

const chiefComplaintLabels = {
  shortnessofbreath: "تنگی نفس",
  chestpain: "درد قفسه سینه",
  fever: "تب",
  abdominalpain: "درد شکم",
  headache: "سردرد",
  fall: "سقوط",
  weakness: "ضعف عمومی",
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
const copyCaseBtn = document.querySelector("#copyCaseBtn");
const printCaseBtn = document.querySelector("#printCaseBtn");
const caseSummaryBox = document.querySelector("#caseSummaryBox");
const caseSummaryText = document.querySelector("#caseSummaryText");
const mobileInstallBtn = document.querySelector("#mobileInstallBtn");
const installSheet = document.querySelector("#installSheet");
const closeInstallSheet = document.querySelector("#closeInstallSheet");
const installDoneBtn = document.querySelector("#installDoneBtn");
const installPromptBtn = document.querySelector("#installPromptBtn");
const installHelpText = document.querySelector("#installHelpText");

let deferredInstallPrompt = null;
let latestResult = null;
let latestPayload = null;
let browserModelPromise = null;
const FEEDBACK_STORAGE_KEY = "triageStakeholderFeedback";

function translate(text) {
  if (!text) return "";
  if (translations[text]) return translations[text];
  if (text.startsWith("chief complaint:")) {
    const complaint = text.replace("chief complaint:", "").trim();
    return `شکایت اصلی: ${chiefComplaintLabels[complaint] || complaint}`;
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

function setStatus(ok, mode = "api") {
  const offline = !navigator.onLine;
  if (mode === "browser") {
    apiStatus.textContent = "نسخه وب عمومی آماده است";
    apiStatus.className = "status-pill ok";
    return;
  }
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
    try {
      await loadBrowserModel();
      setStatus(true, "browser");
    } catch {
      setStatus(false);
    }
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

function asNumber(value) {
  if (value === null || value === undefined || value === "") return null;
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function isMissing(value) {
  return value === null || value === undefined || value === "" || Number.isNaN(value);
}

function normalizeArrivalMode(value) {
  const cleaned = String(value || "missing").toLowerCase().replace(/[^a-z0-9]+/g, "");
  return {
    ambulance: "ambulance",
    walkin: "Walk-in",
    wheelchair: "Wheelchair",
    car: "Car",
    police: "Police",
    publictransportation: "Public Transportation",
    other: "Other",
    missing: "missing",
  }[cleaned] || String(value || "missing");
}

function normalizeO2Device(value) {
  const number = asNumber(value);
  return number === null ? "missing" : Number(number).toFixed(1);
}

function normalizeChiefComplaint(value) {
  const cleaned = String(value || "").toLowerCase().replace(/[^a-z0-9]+/g, "");
  return cleaned ? `cc_${cleaned}` : "";
}

function loadBrowserModel() {
  if (!browserModelPromise) {
    browserModelPromise = fetch(BROWSER_MODEL_URL).then((response) => {
      if (!response.ok) throw new Error("browser model unavailable");
      return response.json();
    });
  }
  return browserModelPromise;
}

function buildBrowserFeatures(payload, model) {
  const values = {};
  const set = (name, value) => {
    values[name] = Number.isFinite(value) ? value : null;
  };

  const age = asNumber(payload.age);
  const hr = asNumber(payload.heart_rate);
  const sbp = asNumber(payload.systolic_bp);
  const dbp = asNumber(payload.diastolic_bp);
  const rr = asNumber(payload.respiratory_rate);
  const o2sat = asNumber(payload.oxygen_saturation);
  let temp = asNumber(payload.temperature);
  if (temp !== null && temp > 60) temp = (temp - 32) * 5 / 9;

  const numericVitals = {
    age,
    triage_vital_hr: hr,
    triage_vital_sbp: sbp,
    triage_vital_dbp: dbp,
    triage_vital_rr: rr,
    triage_vital_o2sat: o2sat,
    triage_vital_temp: temp,
  };

  Object.entries(numericVitals).forEach(([name, value]) => set(name, value));
  Object.entries(numericVitals).forEach(([name, value]) => {
    set(`${name}_missing`, isMissing(value) ? 1 : 0);
  });

  const vitalKeys = [
    "triage_vital_hr",
    "triage_vital_sbp",
    "triage_vital_dbp",
    "triage_vital_rr",
    "triage_vital_o2sat",
    "triage_vital_temp",
  ];
  const availableVitalCount = vitalKeys.filter((key) => !isMissing(numericVitals[key])).length;
  set("available_vital_count", availableVitalCount);
  set("has_blood_pressure", !isMissing(sbp) && !isMissing(dbp) ? 1 : 0);
  set("has_core_vitals", availableVitalCount >= 4 ? 1 : 0);

  set("shock_index", hr !== null && sbp ? hr / sbp : null);
  set("map", sbp !== null && dbp !== null ? (sbp + 2 * dbp) / 3 : null);
  set("pulse_pressure", sbp !== null && dbp !== null ? sbp - dbp : null);
  set("hr_rr_ratio", hr !== null && rr ? hr / rr : null);
  set("sbp_dbp_ratio", sbp !== null && dbp ? sbp / dbp : null);
  set("o2_hr_ratio", o2sat !== null && hr ? o2sat / hr : null);

  const flags = {
    hr_abnormal: hr !== null && (hr < 60 || hr > 100),
    sbp_abnormal: sbp !== null && (sbp < 90 || sbp > 180),
    rr_abnormal: rr !== null && (rr < 12 || rr > 20),
    o2_abnormal: o2sat !== null && o2sat < 94,
    temp_abnormal: temp !== null && (temp < 36 || temp > 38.5),
    map_abnormal: values.map !== null && (values.map < 70 || values.map > 110),
    shock_index_abnormal: values.shock_index !== null && values.shock_index > 1.0,
    hypoxia_severe: o2sat !== null && o2sat < 90,
    hypoxia_warning: o2sat !== null && o2sat >= 90 && o2sat < 94,
    hypotension_severe: sbp !== null && sbp < 90,
    hypertension_severe: sbp !== null && sbp >= 180,
    tachycardia_severe: hr !== null && hr >= 130,
    bradycardia_severe: hr !== null && hr < 45,
    tachypnea_severe: rr !== null && rr >= 30,
    bradypnea_severe: rr !== null && rr < 8,
    fever_high: temp !== null && temp >= 39,
    hypothermia: temp !== null && temp < 35,
  };
  Object.entries(flags).forEach(([name, active]) => set(name, active ? 1 : 0));
  set(
    "vital_severity_score",
    [
      "hr_abnormal",
      "sbp_abnormal",
      "rr_abnormal",
      "o2_abnormal",
      "temp_abnormal",
      "map_abnormal",
      "shock_index_abnormal",
    ].reduce((sum, name) => sum + values[name], 0),
  );
  set(
    "vital_red_flag_count",
    [
      "hypoxia_severe",
      "hypotension_severe",
      "tachycardia_severe",
      "bradycardia_severe",
      "tachypnea_severe",
      "bradypnea_severe",
      "fever_high",
      "hypothermia",
    ].reduce((sum, name) => sum + values[name], 0),
  );

  let ageGroup = null;
  if (age !== null && age > 0 && age <= 2) ageGroup = 0;
  else if (age !== null && age <= 12) ageGroup = 1;
  else if (age !== null && age <= 18) ageGroup = 2;
  else if (age !== null && age <= 65) ageGroup = 3;
  else if (age !== null && age <= 200) ageGroup = 4;
  set("age_group", ageGroup);
  set("is_elderly", age !== null && age >= 65 ? 1 : 0);
  set("is_very_elderly", age !== null && age >= 80 ? 1 : 0);
  set("is_pediatric", age !== null && age <= 12 ? 1 : 0);
  set("elderly_with_abnormal_vitals", age !== null && age >= 65 && values.vital_severity_score >= 2 ? 1 : 0);
  set("pediatric_with_abnormal_vitals", age !== null && age <= 12 && values.vital_severity_score >= 2 ? 1 : 0);
  set("shock_or_hypotension", values.shock_index_abnormal || values.hypotension_severe ? 1 : 0);
  set("hypoxia_or_tachypnea", values.o2_abnormal || values.tachypnea_severe ? 1 : 0);

  ["n_edvisits", "n_admissions", "n_surgeries"].forEach((featureName) => {
    const payloadKey = {
      n_edvisits: "previous_ed_visits",
      n_admissions: "previous_admissions",
      n_surgeries: "previous_surgeries",
    }[featureName];
    const raw = asNumber(payload[payloadKey]);
    const value = raw === null ? 0 : Math.max(raw, 0);
    set(featureName, value);
    set(`${featureName}_log1p`, Math.log1p(value));
    set(`${featureName}_present`, raw === null ? 0 : 1);
    set(`${featureName}_any`, value > 0 ? 1 : 0);
  });

  const metadata = model.feature_metadata || {};
  const categorical = metadata.categorical || { columns: [], categories: {} };
  const categoricalValues = {
    dep_name: "missing",
    gender: payload.gender || "missing",
    arrivalmode: normalizeArrivalMode(payload.arrivalmode || "Walk-in"),
    arrivalmonth: payload.arrivalmonth || "missing",
    arrivalday: payload.arrivalday || "missing",
    arrivalhour_bin: payload.arrivalhour_bin || "missing",
    previousdispo: payload.previousdispo || "No previous dispo",
    triage_vital_o2_device: normalizeO2Device(payload.oxygen_device || 0),
  };
  categorical.columns.forEach((column) => {
    (categorical.categories[column] || []).forEach((category) => {
      set(`${column}_${category}`, categoricalValues[column] === String(category) ? 1 : 0);
    });
  });

  const history = new Set((payload.history_conditions || []).map((item) => String(item).toLowerCase()));
  (metadata.history_features || []).forEach((featureName) => {
    set(featureName, history.has(featureName) ? 1 : 0);
  });
  const historyCount = (metadata.history_features || []).reduce((sum, name) => sum + (values[name] || 0), 0);
  set("history_condition_count", historyCount);
  set("history_condition_log1p", Math.log1p(historyCount));
  set("has_known_history", historyCount > 0 ? 1 : 0);
  const cardiopulmonary = [
    "acutemi",
    "asthma",
    "chfnonhp",
    "chrkidneydisease",
    "copd",
    "coronathero",
    "diabmelnoc",
    "diabmelwcm",
    "dysrhythmia",
    "htn",
    "pneumonia",
    "pulmhartdx",
    "tia",
  ];
  const cardiopulmonaryCount = cardiopulmonary.reduce((sum, name) => sum + (values[name] || 0), 0);
  set("cardiopulmonary_history_count", cardiopulmonaryCount);
  set("has_cardiopulmonary_history", cardiopulmonaryCount > 0 ? 1 : 0);

  const complaintFeature = normalizeChiefComplaint(payload.chief_complaint);
  (metadata.chief_complaint_features || []).forEach((featureName) => {
    set(featureName, complaintFeature === featureName ? 1 : 0);
  });
  const complaintKnown = (metadata.chief_complaint_features || []).some((name) => values[name] === 1);
  const highRiskTokens = ["chestpain", "shortness", "sob", "respiratory", "syncope", "seizure", "stroke", "weakness", "altered", "trauma", "fall", "fever"];
  const highRiskComplaintCount = (metadata.chief_complaint_features || []).reduce((sum, name) => {
    return sum + (values[name] === 1 && highRiskTokens.some((token) => name.includes(token)) ? 1 : 0);
  }, 0);
  set("complaint_known", complaintKnown ? 1 : 0);
  set("high_risk_complaint_count", highRiskComplaintCount);
  set("has_high_risk_complaint", highRiskComplaintCount > 0 ? 1 : 0);

  return model.feature_names.map((name, index) => {
    let value = values[name];
    if (!Number.isFinite(value)) value = model.imputer_statistics[index] || 0;
    const scale = model.scaler_scale[index] || 1;
    return value / scale;
  });
}

function evaluateTree(node, features) {
  let current = node;
  while (!Object.prototype.hasOwnProperty.call(current, "leaf")) {
    const featureIndex = Number(String(current.split).replace("f", ""));
    const value = features[featureIndex];
    const nextId = value < current.split_condition ? current.yes : current.no;
    current = current.children.find((child) => child.nodeid === nextId);
  }
  return current.leaf;
}

function sigmoid(value) {
  return 1 / (1 + Math.exp(-value));
}

function safetyFlagsForPayload(payload) {
  const flags = [];
  const o2sat = asNumber(payload.oxygen_saturation);
  const sbp = asNumber(payload.systolic_bp);
  const hr = asNumber(payload.heart_rate);
  const rr = asNumber(payload.respiratory_rate);
  const temp = asNumber(payload.temperature);
  const age = asNumber(payload.age);
  const complaint = String(payload.chief_complaint || "").toLowerCase();
  const history = new Set((payload.history_conditions || []).map((item) => String(item).toLowerCase()));

  if (o2sat !== null && o2sat < 90) flags.push("red flag: oxygen saturation below 90%");
  else if (o2sat !== null && o2sat < 94) flags.push("warning: oxygen saturation below normal triage range");
  if (sbp !== null && sbp < 90) flags.push("red flag: systolic blood pressure below 90");
  if (rr !== null && (rr < 8 || rr >= 30)) flags.push("red flag: severely abnormal respiratory rate");
  if (hr !== null && (hr < 45 || hr >= 130)) flags.push("red flag: severely abnormal heart rate");
  if (temp !== null && (temp < 35 || temp >= 40)) flags.push("red flag: extreme body temperature");
  if (
    complaint.includes("chestpain") &&
    age !== null &&
    age >= 50 &&
    ["coronathero", "acutemi", "dysrhythmia"].some((item) => history.has(item))
  ) {
    flags.push("red flag: chest pain with high-risk cardiac history");
  }
  return flags.slice(0, 4);
}

function explainPayload(payload, safetyFlags) {
  const reasons = [...safetyFlags.slice(0, 2)];
  const o2sat = asNumber(payload.oxygen_saturation);
  const sbp = asNumber(payload.systolic_bp);
  const hr = asNumber(payload.heart_rate);
  const rr = asNumber(payload.respiratory_rate);
  const age = asNumber(payload.age);
  if (o2sat !== null && o2sat < 94) reasons.push("low oxygen saturation");
  if (sbp && hr && hr / sbp > 1) reasons.push("elevated shock index");
  if (rr !== null && (rr < 12 || rr > 20)) reasons.push("abnormal respiratory rate");
  if (age !== null && age >= 65) reasons.push("elderly patient");
  if (payload.chief_complaint) reasons.push(`chief complaint: ${payload.chief_complaint}`);
  if (payload.history_conditions && payload.history_conditions.length) {
    reasons.push(`known history: ${payload.history_conditions.slice(0, 2).join(", ")}`);
  }
  return [...new Set(reasons)].slice(0, 4);
}

function dataQualityForPayload(payload) {
  const recommended = [
    ["chief_complaint", "chief complaint"],
    ["age", "age"],
    ["heart_rate", "heart rate"],
    ["systolic_bp", "systolic blood pressure"],
    ["diastolic_bp", "diastolic blood pressure"],
    ["respiratory_rate", "respiratory rate"],
    ["oxygen_saturation", "oxygen saturation"],
    ["temperature", "temperature"],
  ];
  const present = recommended.filter(([key]) => !isMissing(payload[key]));
  const missing = recommended.filter(([key]) => isMissing(payload[key])).map(([, label]) => label);
  const completeness = Math.round((present.length / recommended.length) * 100) / 100;
  const band = completeness >= 0.75 ? "high" : completeness >= 0.45 ? "medium" : "limited";
  return { completeness, missing, band };
}

function nextBestActionsForResult(isCritical, confidenceBand, safetyFlags, missingFields) {
  const actions = [];
  if (isCritical) {
    actions.push("notify senior triage nurse or emergency physician");
    actions.push("repeat vital signs and keep patient in visible monitored area");
  } else {
    actions.push("continue standard triage pathway and document model output");
  }
  if (safetyFlags.length) actions.push("treat safety flags as clinical prompts, not automated diagnosis");
  if (confidenceBand !== "high" && missingFields.length) {
    actions.push("collect the highest-value missing triage fields before final disposition");
  }
  return actions.slice(0, 4);
}

async function predictInBrowser(payload) {
  const model = await loadBrowserModel();
  const features = buildBrowserFeatures(payload, model);
  const rawScore = model.trees.reduce((sum, tree) => sum + evaluateTree(tree, features), 0);
  const modelProbability = sigmoid(rawScore);
  const threshold = Number(model.threshold);
  const safetyFlags = safetyFlagsForPayload(payload);
  const safetyOverride = safetyFlags.length > 0;
  const probability = safetyOverride ? Math.max(modelProbability, Math.min(0.99, threshold + 0.08)) : modelProbability;
  const isCritical = probability >= threshold;
  const quality = dataQualityForPayload(payload);

  return {
    model_version: model.version,
    operational_mode: "browser_v7_static_pwa",
    model_probability: modelProbability,
    critical_probability: probability,
    threshold,
    risk_level: isCritical ? "critical" : "non_critical",
    triage_band: isCritical ? "ESI 1-2 priority suggested" : "ESI 3-5 standard workflow",
    recommended_action: isCritical ? "Immediate clinical review recommended" : "Continue standard triage workflow",
    explanation: explainPayload(payload, safetyFlags),
    safety_flags: safetyFlags,
    next_best_actions: nextBestActionsForResult(isCritical, quality.band, safetyFlags, quality.missing),
    safety_override: safetyOverride,
    data_completeness: quality.completeness,
    confidence_band: quality.band,
    missing_recommended_fields: quality.missing,
    disclaimer: "Decision-support only; not a replacement for clinical judgment.",
  };
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
  const degrees = Math.round(result.critical_probability * 360);
  const critical = result.risk_level === "critical";
  const color = critical ? "var(--red)" : "var(--green)";

  riskCard.classList.toggle("critical", critical);
  riskPercent.textContent = `${percent}%`;
  modelProbability.textContent = critical ? "بازبینی فوری" : "پایش عادی";
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
    ? `${bandLabel(result.confidence_band)} + ایمنی فعال`
    : bandLabel(result.confidence_band);
  missingFields.textContent = result.missing_recommended_fields.length
    ? result.missing_recommended_fields.map((field) => fieldLabels[field] || field).join("، ")
    : "ورودی‌های کلیدی کامل هستند.";
  updateCaseSummary();
}

async function submitForm(event) {
  event.preventDefault();
  const payload = readPayload();
  riskLabel.textContent = "در حال ارزیابی";
  triageBand.textContent = "لطفا چند لحظه صبر کنید.";
  riskAction.textContent = "مدل و قواعد ایمنی همزمان بررسی می‌شوند.";
  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("prediction failed");
    updateResult(await res.json());
    setStatus(true);
    document.querySelector("#resultPanel").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch {
    try {
      updateResult(await predictInBrowser(payload));
      setStatus(true, "browser");
      document.querySelector("#resultPanel").scrollIntoView({ behavior: "smooth", block: "start" });
    } catch {
      setStatus(false);
      riskLabel.textContent = "خطا در ارتباط";
      triageBand.textContent = "API یا مدل مرورگر در دسترس نیست.";
      riskAction.textContent = "لطفا اتصال را بررسی کنید یا صفحه را دوباره بارگذاری کنید.";
    }
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
  feedbackCount.textContent = count ? `${count} بازخورد ثبت‌شده` : "آماده دریافت بازخورد";
}

async function refreshFeedbackSummary() {
  try {
    const res = await fetch(`${API_BASE}/feedback-summary`);
    if (!res.ok) throw new Error("summary failed");
    const summary = await res.json();
    feedbackCount.textContent = summary.stored_count
      ? `${summary.stored_count} بازخورد ثبت‌شده`
      : "آماده دریافت بازخورد";
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
    feedbackCount.textContent = `${result.stored_count} بازخورد ثبت‌شده`;
    feedbackStatus.textContent = "بازخورد ثبت شد. ممنون که به بهتر شدن نسخه آزمایشی کمک کردید.";
  } catch {
    const entries = getFeedbackEntries();
    entries.push(entry);
    saveFeedbackEntries(entries);
    feedbackStatus.textContent = "اتصال سرور برقرار نبود؛ بازخورد روی همین دستگاه ذخیره شد.";
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
  const complaint = fieldLabels["chief complaint"] || "شکایت اصلی";
  const complaintText = chiefComplaintLabels[payload.chief_complaint] || payload.chief_complaint || "ثبت نشده";
  const summary = [
    "خلاصه ارزیابی تریاژ",
    `وضعیت پیشنهادی: ${riskText}`,
    `درصد خطر: ${formatPercent(latestResult.critical_probability)}`,
    `اعتماد خروجی: ${bandLabel(latestResult.confidence_band)}`,
    `کامل بودن داده‌ها: ${formatPercent(latestResult.data_completeness)}`,
    `${complaint}: ${complaintText}`,
    `سن: ${payload.age ?? "ثبت نشده"}`,
    `علائم حیاتی: ضربان ${payload.heart_rate ?? "-"} | فشار ${payload.systolic_bp ?? "-"}/${payload.diastolic_bp ?? "-"} | تنفس ${payload.respiratory_rate ?? "-"} | اکسیژن ${payload.oxygen_saturation ?? "-"} | دما ${payload.temperature ?? "-"}`,
    `پرچم‌های ایمنی: ${(latestResult.safety_flags || []).map(translate).join(" | ") || "موردی فعال نیست"}`,
    `اقدام پیشنهادی: ${(latestResult.next_best_actions || []).map(translate).join(" | ")}`,
    "تذکر: این خروجی فقط پشتیبان تصمیم است و جایگزین قضاوت بالینی نمی‌شود.",
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

function isStandaloneMode() {
  return window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
}

function installHelpMessage() {
  if (isStandaloneMode()) {
    return "برنامه همین حالا در حالت نصب‌شده اجرا شده است.";
  }
  const ua = navigator.userAgent.toLowerCase();
  if (!window.isSecureContext && !["localhost", "127.0.0.1"].includes(window.location.hostname)) {
    return "برای نصب کامل PWA روی موبایل، صفحه باید از HTTPS باز شود. در حالت شبکه محلی، از گزینه Add to Home screen مرورگر استفاده کنید.";
  }
  if (deferredInstallPrompt) {
    return "مرورگر نصب مستقیم را پشتیبانی می‌کند. دکمه «نصب خودکار» را بزنید.";
  }
  if (/iphone|ipad|ipod/.test(ua)) {
    return "در iPhone از دکمه Share در Safari استفاده کنید و Add to Home Screen را بزنید.";
  }
  if (/android/.test(ua)) {
    return "در Chrome اندروید منوی سه‌نقطه را باز کنید و Add to Home screen یا Install app را انتخاب کنید.";
  }
  return "اگر مرورگر شما نصب مستقیم را نشان نمی‌دهد، از منوی مرورگر گزینه Install app یا Add to Home screen را انتخاب کنید.";
}

function openInstallSheet() {
  installHelpText.textContent = installHelpMessage();
  installPromptBtn.hidden = !deferredInstallPrompt || isStandaloneMode();
  installSheet.hidden = false;
  document.body.classList.add("modal-open");
}

function closeInstallDialog() {
  installSheet.hidden = true;
  document.body.classList.remove("modal-open");
}

async function runInstallPrompt() {
  if (!deferredInstallPrompt) {
    openInstallSheet();
    return;
  }
  deferredInstallPrompt.prompt();
  const choice = await deferredInstallPrompt.userChoice;
  deferredInstallPrompt = null;
  installPromptBtn.hidden = true;
  if (choice.outcome === "accepted") {
    installBtn.textContent = "نصب شد";
    if (mobileInstallBtn) mobileInstallBtn.textContent = "نصب شد";
    closeInstallDialog();
  } else {
    installHelpText.textContent = installHelpMessage();
  }
}

function handleInstallClick() {
  if (deferredInstallPrompt) {
    runInstallPrompt();
    return;
  }
  openInstallSheet();
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
copyCaseBtn.addEventListener("click", copyCaseSummary);
printCaseBtn.addEventListener("click", printCaseSummary);
installBtn.addEventListener("click", handleInstallClick);
if (mobileInstallBtn) mobileInstallBtn.addEventListener("click", handleInstallClick);
installPromptBtn.addEventListener("click", runInstallPrompt);
closeInstallSheet.addEventListener("click", closeInstallDialog);
installDoneBtn.addEventListener("click", closeInstallDialog);
installSheet.addEventListener("click", (event) => {
  if (event.target === installSheet) closeInstallDialog();
});
window.addEventListener("resize", drawSignal);
window.addEventListener("online", checkApi);
window.addEventListener("offline", () => setStatus(false));

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  installBtn.textContent = "نصب برنامه";
  if (mobileInstallBtn) mobileInstallBtn.textContent = "نصب";
});

window.addEventListener("appinstalled", () => {
  deferredInstallPrompt = null;
  installBtn.textContent = "نصب شد";
  if (mobileInstallBtn) mobileInstallBtn.textContent = "نصب شد";
  closeInstallDialog();
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js").catch(() => {});
  });
}

if (isStandaloneMode()) {
  installBtn.textContent = "نصب شد";
  if (mobileInstallBtn) mobileInstallBtn.textContent = "نصب شد";
}

drawSignal();
refreshFeedbackSummary();
checkApi();
