const APP_CONFIG = window.TRIAGE_APP_CONFIG || {};
const API_BASE = String(APP_CONFIG.API_BASE_URL || "").trim().replace(/\/+$/, "");
const BROWSER_MODEL_URL = APP_CONFIG.BROWSER_MODEL_URL || "static/model-v7.json";
const TRY_SAME_ORIGIN_API = APP_CONFIG.TRY_SAME_ORIGIN_API ?? "auto";
const IS_ANDROID_WRAPPER = window.location.hostname === "appassets.androidplatform.net";

if (IS_ANDROID_WRAPPER) document.documentElement.classList.add("android-wrapper");

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
  "immediate: oxygen saturation below 90%": "رسیدگی فوری: اکسیژن خون کمتر از ۹۰٪",
  "urgent: oxygen saturation below normal triage range": "بررسی سریع: اکسیژن خون پایین‌تر از محدوده طبیعی",
  "immediate: adult systolic blood pressure at or below 90": "رسیدگی فوری: فشار سیستولیک بزرگسال ۹۰ یا کمتر",
  "urgent: adult systolic blood pressure between 91 and 100": "بررسی سریع: فشار سیستولیک بزرگسال بین ۹۱ تا ۱۰۰",
  "urgent: adult systolic blood pressure at or above 220": "بررسی سریع: فشار سیستولیک بزرگسال ۲۲۰ یا بیشتر",
  "immediate: pediatric systolic blood pressure below age-adjusted threshold": "رسیدگی فوری: فشار سیستولیک کودک پایین‌تر از حد متناسب با سن است",
  "immediate: severely abnormal adult respiratory rate": "رسیدگی فوری: نرخ تنفس بزرگسال به‌شدت غیرطبیعی",
  "urgent: adult respiratory rate outside the stable range": "بررسی سریع: نرخ تنفس بزرگسال خارج از محدوده پایدار است",
  "immediate: adult heart rate at or above 150/min": "رسیدگی فوری: ضربان قلب بزرگسال ۱۵۰ یا بیشتر در دقیقه",
  "urgent: adult heart rate between 130 and 149/min": "بررسی سریع: ضربان قلب بزرگسال بین ۱۳۰ تا ۱۴۹ در دقیقه",
  "immediate: adult heart rate below 40/min": "رسیدگی فوری: ضربان قلب بزرگسال کمتر از ۴۰ در دقیقه",
  "urgent: adult heart rate between 40 and 50/min": "بررسی سریع: ضربان قلب بزرگسال بین ۴۰ تا ۵۰ در دقیقه",
  "urgent: adult heart rate between 111 and 129/min": "بررسی سریع: ضربان قلب بزرگسال بین ۱۱۱ تا ۱۲۹ در دقیقه",
  "immediate: infant heart rate at or above 220/min": "رسیدگی فوری: ضربان قلب شیرخوار ۲۲۰ یا بیشتر در دقیقه",
  "urgent: infant heart rate above age-adjusted review threshold": "بررسی سریع: ضربان قلب شیرخوار بالاتر از حد متناسب با سن است",
  "immediate: markedly low infant heart rate": "رسیدگی فوری: ضربان قلب شیرخوار به‌طور قابل توجهی پایین است",
  "immediate: child heart rate at or above 180/min": "رسیدگی فوری: ضربان قلب کودک ۱۸۰ یا بیشتر در دقیقه",
  "urgent: child heart rate above age-adjusted review threshold": "بررسی سریع: ضربان قلب کودک بالاتر از حد متناسب با سن است",
  "immediate: markedly low child heart rate": "رسیدگی فوری: ضربان قلب کودک به‌طور قابل توجهی پایین است",
  "immediate: severely abnormal child respiratory rate": "رسیدگی فوری: نرخ تنفس کودک به‌شدت غیرطبیعی است",
  "urgent: child respiratory rate above age-adjusted review threshold": "بررسی سریع: نرخ تنفس کودک بالاتر از حد متناسب با سن است",
  "immediate: fever in an infant younger than 3 months": "رسیدگی فوری: تب در شیرخوار کمتر از سه ماه",
  "urgent: high fever in an infant aged 3 to 6 months": "بررسی سریع: تب بالا در شیرخوار سه تا شش ماه",
  "immediate: extreme body temperature": "رسیدگی فوری: دمای بدن در محدوده بحرانی",
  "urgent: body temperature outside the stable range": "بررسی سریع: دمای بدن خارج از محدوده پایدار است",
  "immediate: markedly elevated shock index": "رسیدگی فوری: شاخص شوک به‌طور قابل توجهی بالاست",
  "urgent: elevated shock index": "بررسی سریع: شاخص شوک بالاست",
  "immediate: combined adult vital-sign score is high": "رسیدگی فوری: ترکیب چند علامت حیاتی بزرگسال پرخطر است",
  "urgent: combined adult vital-sign score requires rapid review": "بررسی سریع: ترکیب علائم حیاتی بزرگسال نیازمند بازبینی سریع است",
  "immediate: multiple age-adjusted pediatric vital signs are abnormal": "رسیدگی فوری: چند علامت حیاتی کودک نسبت به سن غیرطبیعی است",
  "immediate: chest pain with high-risk cardiac history": "رسیدگی فوری: درد قفسه سینه همراه با سابقه قلبی پرخطر",
  "verify measurement: oxygen saturation is outside the expected triage input range": "اندازه‌گیری اکسیژن خون بسیار دور از محدوده معمول است؛ حسگر و عدد دوباره بررسی شود",
  "verify measurement: systolic blood pressure is outside the expected triage input range": "فشار سیستولیک بسیار دور از محدوده معمول است؛ اندازه‌گیری دوباره بررسی شود",
  "verify measurement: diastolic blood pressure is outside the expected triage input range": "فشار دیاستولیک بسیار دور از محدوده معمول است؛ اندازه‌گیری دوباره بررسی شود",
  "verify measurement: systolic/diastolic blood pressure relationship is outside the expected triage input range": "رابطه فشار سیستولیک و دیاستولیک ناسازگار است؛ کاف و اندازه‌گیری دوباره بررسی شود",
  "verify measurement: respiratory rate is outside the expected triage input range": "نرخ تنفس بسیار دور از محدوده معمول است؛ شمارش دوباره انجام شود",
  "verify measurement: heart rate is outside the expected triage input range": "ضربان قلب بسیار دور از محدوده معمول است؛ حسگر و عدد دوباره بررسی شود",
  "verify measurement: body temperature is outside the expected triage input range": "دمای بدن بسیار دور از محدوده معمول است؛ اندازه‌گیری دوباره بررسی شود",
  "low oxygen saturation": "اشباع اکسیژن پایین",
  "elevated shock index": "شاخص شوک بالا",
  "abnormal respiratory rate": "نرخ تنفس غیرطبیعی",
  "elderly patient": "بیمار سالمند",
  "no single dominant risk factor identified": "عامل غالب مشخصی شناسایی نشد",
  "notify senior triage nurse or emergency physician": "اطلاع فوری به پرستار ارشد یا پزشک اورژانس",
  "repeat vital signs and keep patient in visible monitored area": "تکرار علائم حیاتی و نگهداری بیمار در محدوده قابل مشاهده",
  "request rapid review by the responsible triage clinician": "درخواست بررسی سریع توسط مسئول تریاژ",
  "repeat the abnormal vital sign without delaying clinical review": "تکرار علامت غیرطبیعی بدون به‌تأخیرانداختن بررسی بالینی",
  "continue standard triage pathway and document model output": "ادامه مسیر معمول ارزیابی و ثبت خروجی",
  "verify the outlying measurement and sensor placement immediately": "بررسی فوری عدد پرت، وضعیت حسگر و تکرار اندازه‌گیری",
  "treat safety flags as clinical prompts, not automated diagnosis": "این هشدارها نشانه کمکی هستند، نه تشخیص خودکار",
  "collect the highest-value missing triage fields before final disposition": "در صورت امکان، اطلاعات کلیدی باقی‌مانده تکمیل شود",
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
const appMessage = document.querySelector("#appMessage");
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
const installHelpBtn = document.querySelector("#installHelpBtn");
const safetyNotice = document.querySelector("#safetyNotice");
const acceptSafetyNotice = document.querySelector("#acceptSafetyNotice");

let deferredInstallPrompt = null;
let latestResult = null;
let latestPayload = null;
let browserModelPromise = null;

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
    apiStatus.textContent = "آماده";
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
  if (!shouldTryApi()) {
    try {
      await loadBrowserModel();
      setStatus(true, "browser");
    } catch {
      setStatus(false);
    }
    return;
  }
  try {
    const res = await fetch(apiUrl("/health"));
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

function hasMinimumTriageSignal(payload) {
  const vitalFields = [
    "heart_rate",
    "systolic_bp",
    "diastolic_bp",
    "respiratory_rate",
    "oxygen_saturation",
    "temperature",
  ];
  const hasComplaint = Boolean(String(payload.chief_complaint || "").trim());
  const hasVital = vitalFields.some((field) => payload[field] !== undefined && payload[field] !== null);
  return hasComplaint || hasVital;
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

function normalizeChiefComplaint(value, age = null) {
  const cleaned = String(value || "").toLowerCase().replace(/[^a-z0-9]+/g, "");
  if (cleaned === "fall" && age !== null && age >= 65) return "cc_fall>65";
  const aliases = {
    fever: "cc_fever-9weeksto74years",
    headache: "cc_headache-newonsetornewsymptoms",
    headachenewonsetornewsymptoms: "cc_headache-newonsetornewsymptoms",
  };
  if (aliases[cleaned]) return aliases[cleaned];
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

function shouldTryApi() {
  if (API_BASE) return true;
  if (TRY_SAME_ORIGIN_API === true) return true;
  if (TRY_SAME_ORIGIN_API === false) return false;
  return window.location.port === "8000";
}

function apiUrl(path) {
  return API_BASE ? `${API_BASE}${path}` : path;
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
    const value = raw === null ? null : Math.max(raw, 0);
    set(featureName, value);
    set(`${featureName}_log1p`, value === null ? null : Math.log1p(value));
    set(`${featureName}_present`, raw === null ? 0 : 1);
    set(`${featureName}_any`, value !== null && value > 0 ? 1 : 0);
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

  const complaintFeature = normalizeChiefComplaint(payload.chief_complaint, age);
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
    // XGBoost evaluates float32 feature values; matching that precision keeps
    // browser tree paths identical to the Python predictor around split points.
    return Math.fround(value / scale);
  });
}

function evaluateTree(node, features) {
  let current = node;
  while (!Object.prototype.hasOwnProperty.call(current, "leaf")) {
    const featureIndex = Number(String(current.split).replace("f", ""));
    const value = features[featureIndex];
    const nextId = value < Math.fround(current.split_condition) ? current.yes : current.no;
    current = current.children.find((child) => child.nodeid === nextId);
  }
  return current.leaf;
}

function sigmoid(value) {
  return 1 / (1 + Math.exp(-value));
}

function operatingProfileForPayload(payload, defaultThreshold) {
  const hasComplaint = String(payload.chief_complaint || "").trim().length > 0;
  const hasHeartRate = asNumber(payload.heart_rate) !== null;
  const hasOxygen = asNumber(payload.oxygen_saturation) !== null;
  const otherVitalsAbsent = [
    payload.systolic_bp,
    payload.diastolic_bp,
    payload.respiratory_rate,
    payload.temperature,
  ].every((value) => asNumber(value) === null);
  if (hasComplaint && hasHeartRate && hasOxygen && otherVitalsAbsent) {
    if (asNumber(payload.age) === null) {
      return { name: "validated_sparse_3", threshold: 0.16415970027446747 };
    }
    return { name: "validated_sparse_4", threshold: 0.1881568878889084 };
  }
  return { name: "full_v7_default", threshold: Number(defaultThreshold) };
}

function safetyAssessmentForPayload(payload) {
  const flags = [];
  const measurementWarnings = [];
  let severity = "none";
  const o2sat = asNumber(payload.oxygen_saturation);
  const sbp = asNumber(payload.systolic_bp);
  const dbp = asNumber(payload.diastolic_bp);
  const hr = asNumber(payload.heart_rate);
  const rr = asNumber(payload.respiratory_rate);
  const temp = asNumber(payload.temperature);
  const age = asNumber(payload.age);
  const complaint = String(payload.chief_complaint || "").toLowerCase();
  const history = new Set((payload.history_conditions || []).map((item) => String(item).toLowerCase()));
  const oxygenDevice = asNumber(payload.oxygen_device);
  let safetyPoints = 0;
  let safetyDomains = 0;

  const rank = { none: 0, urgent: 1, immediate: 2 };
  const addFlag = (message, level) => {
    flags.push(message);
    if (rank[level] > rank[severity]) severity = level;
  };
  const addMeasurementWarning = (field) => {
    measurementWarnings.push(`verify measurement: ${field} is outside the expected triage input range`);
  };
  const addPoints = (points) => {
    if (points > 0) {
      safetyPoints += points;
      safetyDomains += 1;
    }
  };

  if (o2sat !== null && o2sat < 90) addFlag("immediate: oxygen saturation below 90%", "immediate");
  else if (o2sat !== null && o2sat < 94) addFlag("urgent: oxygen saturation below normal triage range", "urgent");
  if (o2sat !== null) addPoints(o2sat <= 91 ? 3 : o2sat <= 93 ? 2 : o2sat <= 95 ? 1 : 0);
  if (oxygenDevice !== null && oxygenDevice > 0) safetyPoints += 2;
  if (o2sat !== null && o2sat < 50) addMeasurementWarning("oxygen saturation");

  const isAdultOrUnknown = age === null || age >= 16;
  if (sbp !== null && isAdultOrUnknown && sbp <= 90) {
    addFlag("immediate: adult systolic blood pressure at or below 90", "immediate");
  } else if (sbp !== null && isAdultOrUnknown && sbp <= 100) {
    addFlag("urgent: adult systolic blood pressure between 91 and 100", "urgent");
  } else if (sbp !== null && isAdultOrUnknown && sbp >= 220) {
    addFlag("urgent: adult systolic blood pressure at or above 220", "urgent");
  }
  if (sbp !== null && isAdultOrUnknown) {
    addPoints(sbp <= 90 || sbp >= 220 ? 3 : sbp <= 100 ? 2 : sbp <= 110 ? 1 : 0);
  }
  if (sbp !== null && (sbp < 40 || sbp > 260)) addMeasurementWarning("systolic blood pressure");
  if (dbp !== null && (dbp < 20 || dbp > 160)) addMeasurementWarning("diastolic blood pressure");
  if (sbp !== null && dbp !== null && (dbp >= sbp || sbp - dbp < 10)) {
    addMeasurementWarning("systolic/diastolic blood pressure relationship");
  }

  if (sbp !== null && age !== null && age < 16) {
    const pediatricHypotensionThreshold = age < 1 ? 70 : age <= 10 ? 70 + 2 * age : 90;
    if (sbp < pediatricHypotensionThreshold) {
      addFlag("immediate: pediatric systolic blood pressure below age-adjusted threshold", "immediate");
      addPoints(3);
    }
  }

  if (rr !== null && isAdultOrUnknown && (rr <= 8 || rr >= 30)) {
    addFlag("immediate: severely abnormal adult respiratory rate", "immediate");
  } else if (rr !== null && isAdultOrUnknown && ((rr >= 9 && rr <= 11) || (rr >= 21 && rr <= 29))) {
    addFlag("urgent: adult respiratory rate outside the stable range", "urgent");
  }
  if (rr !== null && isAdultOrUnknown) {
    addPoints(rr <= 8 || rr >= 25 ? 3 : rr >= 21 ? 2 : rr <= 11 ? 1 : 0);
  }
  if (rr !== null && (rr < 3 || rr > 70)) addMeasurementWarning("respiratory rate");

  if (hr !== null) {
    if (isAdultOrUnknown) {
      if (hr >= 150) addFlag("immediate: adult heart rate at or above 150/min", "immediate");
      else if (hr >= 130) addFlag("urgent: adult heart rate between 130 and 149/min", "urgent");
      if (hr < 40) addFlag("immediate: adult heart rate below 40/min", "immediate");
      else if (hr <= 50) addFlag("urgent: adult heart rate between 40 and 50/min", "urgent");
      else if (hr >= 111 && hr < 130) addFlag("urgent: adult heart rate between 111 and 129/min", "urgent");
      addPoints(hr <= 40 || hr >= 131 ? 3 : hr >= 111 ? 2 : hr <= 50 || hr >= 91 ? 1 : 0);
    } else if (age < 1) {
      if (hr >= 220) addFlag("immediate: infant heart rate at or above 220/min", "immediate");
      else if (hr >= 150) addFlag("urgent: infant heart rate above age-adjusted review threshold", "urgent");
      if (hr < 80) addFlag("immediate: markedly low infant heart rate", "immediate");
      addPoints(hr >= 160 || hr < 80 ? 3 : hr >= 150 ? 2 : 0);
    } else {
      if (hr >= 180) addFlag("immediate: child heart rate at or above 180/min", "immediate");
      else {
        let moderateHr;
        let highHr;
        if (age < 3) [moderateHr, highHr] = [140, 150];
        else if (age < 5) [moderateHr, highHr] = [130, 140];
        else if (age < 6) [moderateHr, highHr] = [120, 130];
        else if (age < 8) [moderateHr, highHr] = [110, 120];
        else if (age < 12) [moderateHr, highHr] = [105, 115];
        else [moderateHr, highHr] = [111, 131];
        if (hr >= moderateHr) addFlag("urgent: child heart rate above age-adjusted review threshold", "urgent");
        addPoints(hr >= highHr ? 3 : hr >= moderateHr ? 2 : 0);
      }
      if (hr < 60) {
        addFlag("immediate: markedly low child heart rate", "immediate");
        addPoints(3);
      }
    }
    if (hr < 20 || hr > 250) addMeasurementWarning("heart rate");
  }

  if (rr !== null && age !== null && age < 16) {
    let moderateRr;
    let highRr;
    let immediateRr;
    if (age < 1) [moderateRr, highRr, immediateRr] = [50, 60, 70];
    else if (age < 3) [moderateRr, highRr, immediateRr] = [40, 50, 60];
    else if (age < 5) [moderateRr, highRr, immediateRr] = [35, 40, 60];
    else if (age < 6) [moderateRr, highRr, immediateRr] = [24, 29, 50];
    else if (age < 8) [moderateRr, highRr, immediateRr] = [24, 27, 50];
    else if (age < 12) [moderateRr, highRr, immediateRr] = [22, 25, 45];
    else [moderateRr, highRr, immediateRr] = [21, 25, 40];
    if (rr >= immediateRr || rr <= 8) {
      addFlag("immediate: severely abnormal child respiratory rate", "immediate");
    } else if (rr >= moderateRr) {
      addFlag("urgent: child respiratory rate above age-adjusted review threshold", "urgent");
    }
    addPoints(rr >= highRr || rr <= 8 ? 3 : rr >= moderateRr ? 2 : 0);
  }

  if (temp !== null && age !== null && age < 0.25 && temp >= 38) {
    addFlag("immediate: fever in an infant younger than 3 months", "immediate");
  } else if (temp !== null && age !== null && age < 0.5 && temp >= 39) {
    addFlag("urgent: high fever in an infant aged 3 to 6 months", "urgent");
  }
  if (temp !== null && (temp <= 35 || temp >= 40)) addFlag("immediate: extreme body temperature", "immediate");
  else if (temp !== null && (temp < 36 || temp >= 39.1)) addFlag("urgent: body temperature outside the stable range", "urgent");
  if (temp !== null) addPoints(temp <= 35 ? 3 : temp >= 39.1 ? 2 : temp < 36 || temp > 38 ? 1 : 0);
  if (temp !== null && (temp < 30 || temp > 43)) addMeasurementWarning("body temperature");

  if (isAdultOrUnknown && hr !== null && sbp !== null && sbp > 0) {
    const shockIndex = hr / sbp;
    if (shockIndex >= 1.2) addFlag("immediate: markedly elevated shock index", "immediate");
    else if (shockIndex >= 1.0) addFlag("urgent: elevated shock index", "urgent");
  }

  if (isAdultOrUnknown && safetyDomains >= 2) {
    if (safetyPoints >= 7) addFlag("immediate: combined adult vital-sign score is high", "immediate");
    else if (safetyPoints >= 5) addFlag("urgent: combined adult vital-sign score requires rapid review", "urgent");
  } else if (!isAdultOrUnknown && safetyDomains >= 2 && safetyPoints >= 6) {
    addFlag("immediate: multiple age-adjusted pediatric vital signs are abnormal", "immediate");
  }
  if (
    complaint.includes("chestpain") &&
    age !== null &&
    age >= 50 &&
    ["coronathero", "acutemi", "dysrhythmia"].some((item) => history.has(item))
  ) {
    addFlag("immediate: chest pain with high-risk cardiac history", "immediate");
  }
  return {
    severity,
    flags: [...new Set(flags)].slice(0, 5),
    measurementWarnings: [...new Set(measurementWarnings)].slice(0, 3),
    outOfDistribution: measurementWarnings.length > 0,
  };
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

function nextBestActionsForResult(riskLevel, confidenceBand, safetyFlags, measurementWarnings, missingFields) {
  const actions = [];
  if (riskLevel === "critical") {
    actions.push("notify senior triage nurse or emergency physician");
    actions.push("repeat vital signs and keep patient in visible monitored area");
  } else if (riskLevel === "urgent") {
    actions.push("request rapid review by the responsible triage clinician");
    actions.push("repeat the abnormal vital sign without delaying clinical review");
  } else {
    actions.push("continue standard triage pathway and document model output");
  }
  if (measurementWarnings.length) actions.push("verify the outlying measurement and sensor placement immediately");
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
  const operatingProfile = operatingProfileForPayload(payload, model.threshold);
  const threshold = operatingProfile.threshold;
  const safety = safetyAssessmentForPayload(payload);
  const safetyFlags = safety.flags;
  const safetyOverride = safety.severity !== "none";
  const modelIsCritical = modelProbability >= threshold;
  const riskLevel = modelIsCritical || safety.severity === "immediate"
    ? "critical"
    : safety.severity === "urgent"
      ? "urgent"
      : "non_critical";
  const assessmentBasis = modelIsCritical && safetyOverride
    ? "model_and_safety_rule"
    : safetyOverride
      ? "safety_rule"
      : "model";
  const quality = dataQualityForPayload(payload);

  return {
    model_version: model.version,
    operational_mode: "browser_v7_static_pwa",
    operating_profile: operatingProfile.name,
    model_probability: modelProbability,
    critical_probability: modelProbability,
    threshold,
    risk_level: riskLevel,
    triage_band: riskLevel === "critical"
      ? "priority_1_immediate_review"
      : riskLevel === "urgent"
        ? "priority_2_rapid_review"
        : "standard_triage_review",
    recommended_action: riskLevel === "critical"
      ? "Immediate clinical review recommended"
      : riskLevel === "urgent"
        ? "Rapid clinical review recommended"
        : "Continue standard triage workflow",
    explanation: explainPayload(payload, safetyFlags),
    safety_flags: safetyFlags,
    next_best_actions: nextBestActionsForResult(
      riskLevel,
      quality.band,
      safetyFlags,
      safety.measurementWarnings,
      quality.missing,
    ),
    safety_override: safetyOverride,
    safety_severity: safety.severity,
    assessment_basis: assessmentBasis,
    safety_rule_version: "2026.07.2",
    measurement_warnings: safety.measurementWarnings,
    out_of_distribution: safety.outOfDistribution,
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
  if (value === "high") return "اطمینان بالا";
  if (value === "medium") return "اطمینان متوسط";
  return "داده محدود";
}

function bandPersian(value) {
  if (value === "priority_1_immediate_review" || value.includes("ESI 1-2")) return "اولویت یک: بررسی فوری";
  if (value === "priority_2_rapid_review") return "اولویت دو: بررسی سریع";
  return "مسیر معمول ارزیابی";
}

function updateResult(result) {
  latestResult = result;
  latestPayload = readPayload();
  const modelEstimate = Number(result.model_probability ?? result.critical_probability ?? 0);
  const percent = Math.round(modelEstimate * 100);
  const critical = result.risk_level === "critical";
  const urgent = result.risk_level === "urgent";
  const color = critical ? "var(--red)" : urgent ? "var(--amber)" : "var(--green)";
  const degrees = critical ? 360 : urgent ? 300 : Math.round(modelEstimate * 360);

  riskCard.classList.toggle("critical", critical);
  riskCard.classList.toggle("urgent", urgent);
  riskPercent.textContent = critical ? "فوری" : urgent ? "سریع" : `${percent}%`;
  modelProbability.textContent = `${percent}%`;
  gaugeRing.style.background = `radial-gradient(circle at center, #fff 55%, transparent 56%), conic-gradient(${color} ${degrees}deg, #dfe8eb 0deg)`;
  riskLabel.textContent = critical
    ? "رسیدگی فوری لازم است"
    : urgent
      ? "بررسی سریع لازم است"
      : "در حال حاضر نشانه بحرانی واضح دیده نشد";
  triageBand.textContent = bandPersian(result.triage_band || "");
  riskAction.textContent = critical
    ? "بیمار بدون تأخیر به مسئول تریاژ یا پزشک اورژانس ارجاع شود؛ علائم حیاتی نیز دوباره اندازه‌گیری شود."
    : urgent
      ? "علامت غیرطبیعی دوباره اندازه‌گیری و بیمار سریع‌تر توسط مسئول تریاژ بررسی شود."
      : "ارزیابی معمول ادامه پیدا کند و در صورت تغییر علائم دوباره بررسی شود.";

  renderList(explanations, result.explanation, "عامل غالب مشخصی شناسایی نشد.");
  renderList(safetyFlags, result.safety_flags, "هشدار مهمی ثبت نشده است.");
  if (result.measurement_warnings && result.measurement_warnings.length) {
    result.measurement_warnings.forEach((warning) => {
      const li = document.createElement("li");
      li.textContent = translate(warning);
      safetyFlags.appendChild(li);
    });
  }
  renderList(nextActions, result.next_best_actions, "ادامه مسیر معمول ارزیابی.");

  dataQuality.textContent = `${Math.round(result.data_completeness * 100)}%`;
  qualityBar.style.width = `${Math.round(result.data_completeness * 100)}%`;
  confidenceBand.textContent = result.safety_override
    ? `${bandLabel(result.confidence_band)} + قانون ایمنی فعال`
    : bandLabel(result.confidence_band);
  missingFields.textContent = result.missing_recommended_fields.length
    ? result.missing_recommended_fields.map((field) => fieldLabels[field] || field).join("، ")
    : "اطلاعات کلیدی کامل هستند.";
  updateCaseSummary();
}

async function submitForm(event) {
  event.preventDefault();
  const payload = readPayload();
  if (!hasMinimumTriageSignal(payload)) {
    riskLabel.textContent = "اطلاعات کافی نیست";
    triageBand.textContent = "حداقل شکایت اصلی یا یکی از علائم حیاتی را وارد کنید.";
    riskAction.textContent = "ارزیابی بدون نشانه بالینی می‌تواند برداشت نادرست ایجاد کند.";
    renderList(explanations, [], "هنوز نشانه‌ای برای ارزیابی وارد نشده است.");
    renderList(safetyFlags, [], "هشداری قابل ارزیابی نیست.");
    renderList(nextActions, [], "شکایت اصلی یا یک علامت حیاتی ثبت شود.");
    dataQuality.textContent = "0%";
    qualityBar.style.width = "0%";
    confidenceBand.textContent = "اطلاعات ناکافی";
    missingFields.textContent = "شکایت اصلی، ضربان قلب، فشار خون، تنفس، اکسیژن یا دما";
    document.querySelector("#resultPanel").scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (!shouldTryApi()) {
    try {
      updateResult(await predictInBrowser(payload));
      setStatus(true, "browser");
      document.querySelector("#resultPanel").scrollIntoView({ behavior: "smooth", block: "start" });
    } catch {
      setStatus(false);
      riskLabel.textContent = "خطا در ارتباط";
      triageBand.textContent = "مدل مرورگر در دسترس نیست.";
      riskAction.textContent = "لطفا اتصال را بررسی کنید یا صفحه را دوباره بارگذاری کنید.";
    }
    return;
  }
  riskLabel.textContent = "در حال بررسی اطلاعات";
  triageBand.textContent = "لطفا چند لحظه صبر کنید.";
  riskAction.textContent = "امدادیار اطلاعات واردشده را بررسی می‌کند.";
  try {
    const res = await fetch(apiUrl("/predict"), {
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
  riskCard.classList.remove("critical", "urgent");
  riskPercent.textContent = "--";
  modelProbability.textContent = "--";
  riskLabel.textContent = "در انتظار اطلاعات بیمار";
  triageBand.textContent = "پس از ارزیابی، نتیجه ساده و قابل فهم نمایش داده می‌شود.";
  riskAction.textContent = "امدادیار فقط پشتیبان تصمیم است و جایگزین نظر کادر درمان نمی‌شود.";
  dataQuality.textContent = "--";
  qualityBar.style.width = "0%";
  confidenceBand.textContent = "آماده";
  missingFields.textContent = "--";
  renderList(explanations, [], "پس از ارزیابی نمایش داده می‌شود.");
  renderList(safetyFlags, [], "هشدار مهمی ثبت نشده است.");
  renderList(nextActions, [], "پس از ارزیابی نمایش داده می‌شود.");
  caseSummaryBox.hidden = true;
  caseSummaryText.textContent = "";
}

function setAppMessage(text) {
  if (appMessage) appMessage.textContent = text;
}

function formatPercent(value) {
  if (typeof value !== "number") return "--";
  return `${Math.round(value * 100)}%`;
}

function updateCaseSummary() {
  if (!latestResult) return;
  const payload = latestPayload || {};
  const riskText = latestResult.risk_level === "critical"
    ? "رسیدگی فوری لازم است"
    : latestResult.risk_level === "urgent"
      ? "بررسی سریع لازم است"
      : "در حال حاضر نشانه بحرانی واضح دیده نشد";
  const assessmentBasis = {
    model: "برآورد مدل",
    safety_rule: "قانون ایمنی علائم حیاتی",
    model_and_safety_rule: "مدل و قانون ایمنی علائم حیاتی",
  }[latestResult.assessment_basis] || "برآورد مدل";
  const complaint = fieldLabels["chief complaint"] || "شکایت اصلی";
  const complaintText = chiefComplaintLabels[payload.chief_complaint] || payload.chief_complaint || "ثبت نشده";
  const summary = [
    "خلاصه ارزیابی امدادیار",
    `وضعیت پیشنهادی: ${riskText}`,
    `برآورد آماری مدل: ${formatPercent(latestResult.model_probability ?? latestResult.critical_probability)}`,
    `مبنای اولویت: ${assessmentBasis}`,
    `اعتماد خروجی: ${bandLabel(latestResult.confidence_band)}`,
    `کامل بودن داده‌ها: ${formatPercent(latestResult.data_completeness)}`,
    `${complaint}: ${complaintText}`,
    `سن: ${payload.age ?? "ثبت نشده"}`,
    `علائم حیاتی: ضربان ${payload.heart_rate ?? "-"} | فشار ${payload.systolic_bp ?? "-"}/${payload.diastolic_bp ?? "-"} | تنفس ${payload.respiratory_rate ?? "-"} | اکسیژن ${payload.oxygen_saturation ?? "-"} | دما ${payload.temperature ?? "-"}`,
    `هشدارهای مهم: ${(latestResult.safety_flags || []).map(translate).join(" | ") || "هشدار مهمی فعال نیست"}`,
    `کنترل اندازه‌گیری: ${(latestResult.measurement_warnings || []).map(translate).join(" | ") || "نیازی به تکرار به‌علت عدد پرت ثبت نشده است"}`,
    `اقدام پیشنهادی: ${(latestResult.next_best_actions || []).map(translate).join(" | ")}`,
    "تذکر: این خروجی فقط پشتیبان تصمیم است و جایگزین قضاوت بالینی نمی‌شود.",
  ].join("\n");
  caseSummaryText.textContent = summary;
  caseSummaryBox.hidden = false;
}

async function copyCaseSummary() {
  if (!caseSummaryText.textContent) {
    setAppMessage("ابتدا یک بیمار را ارزیابی کنید.");
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
    setAppMessage("ابتدا یک بیمار را ارزیابی کنید.");
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
  if (!window.isSecureContext) {
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

function acknowledgeSafetyNotice() {
  try {
    localStorage.setItem("emdadyar-safety-notice-v1", "accepted");
  } catch {
    // The notice still closes when storage is unavailable.
  }
  safetyNotice.hidden = true;
  document.body.classList.remove("modal-open");
}

function showSafetyNoticeIfNeeded() {
  let accepted = false;
  try {
    accepted = localStorage.getItem("emdadyar-safety-notice-v1") === "accepted";
  } catch {
    accepted = false;
  }
  if (!accepted) {
    safetyNotice.hidden = false;
    document.body.classList.add("modal-open");
  }
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
copyCaseBtn.addEventListener("click", copyCaseSummary);
printCaseBtn.addEventListener("click", printCaseSummary);
installBtn.addEventListener("click", handleInstallClick);
if (mobileInstallBtn) mobileInstallBtn.addEventListener("click", handleInstallClick);
if (installHelpBtn) installHelpBtn.addEventListener("click", handleInstallClick);
installPromptBtn.addEventListener("click", runInstallPrompt);
closeInstallSheet.addEventListener("click", closeInstallDialog);
installDoneBtn.addEventListener("click", closeInstallDialog);
acceptSafetyNotice.addEventListener("click", acknowledgeSafetyNotice);
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

if ("serviceWorker" in navigator && !IS_ANDROID_WRAPPER) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js").catch(() => {});
  });
}

if (IS_ANDROID_WRAPPER) {
  installBtn.hidden = true;
  if (mobileInstallBtn) mobileInstallBtn.hidden = true;
} else if (isStandaloneMode()) {
  installBtn.textContent = "نصب شد";
  if (mobileInstallBtn) mobileInstallBtn.textContent = "نصب شد";
}

drawSignal();
checkApi();
showSafetyNoticeIfNeeded();
