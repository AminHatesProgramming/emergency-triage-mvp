const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const targetUrl = process.env.PWA_URL || "http://127.0.0.1:8765/";
const reportPath = process.env.ANDROID_UI_REPORT || "reports/model/android_wrapper_ui_v1.json";
const screenshotDir = process.env.SCREENSHOT_DIR || "docs/market/screenshots";

function chromeExecutable() {
  return [
    process.env.CHROME_EXECUTABLE,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    chromium.executablePath(),
  ].find((candidate) => candidate && fs.existsSync(candidate));
}

async function main() {
  const executablePath = chromeExecutable();
  if (!executablePath) throw new Error("No Chromium-compatible browser was found.");

  const browser = await chromium.launch({ headless: true, executablePath });
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    userAgent:
      "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 Chrome/138 Mobile Safari/537.36 EmdadyarAndroid/1.0",
  });

  try {
    const page = await context.newPage();
    await page.goto(targetUrl, { waitUntil: "networkidle" });
    await page.locator("#acceptSafetyNotice").click({ timeout: 3000 }).catch(() => {});
    await page.waitForTimeout(350);

    const state = await page.evaluate(() => {
      const isVisible = (selector) => {
        const element = document.querySelector(selector);
        return Boolean(element && getComputedStyle(element).display !== "none" && !element.hidden);
      };
      const labels = (selector) =>
        [...document.querySelectorAll(selector)].map((element) => element.textContent.trim());

      return {
        androidClass: document.documentElement.classList.contains("android-wrapper"),
        installHeaderVisible: isVisible("#installBtn"),
        installGuideVisible: isVisible("#installHelpBtn"),
        obsoleteMobileInstallExists: Boolean(document.querySelector("#mobileInstallBtn")),
        mobileTabs: labels(".mobile-tabs button"),
        actionBar: labels(".mobile-action-bar button"),
        guideExists: Boolean(document.querySelector("#userGuide")),
        emptyResultCompact: document.querySelector("#resultPanel")?.classList.contains("is-empty"),
        runtimeErrors: window.__EMDADYAR_RUNTIME_ERRORS__ || [],
      };
    });

    const checks = {
      nativeModeDetected: state.androidClass,
      installControlsHidden: !state.installHeaderVisible && !state.installGuideVisible,
      obsoleteInstallRemoved: !state.obsoleteMobileInstallExists,
      mobileTabsCorrect: JSON.stringify(state.mobileTabs) === JSON.stringify(["سناریو", "نتیجه", "راهنما"]),
      actionBarCorrect: JSON.stringify(state.actionBar) === JSON.stringify(["ارزیابی", "نتیجه", "راهنما"]),
      guideAvailable: state.guideExists,
      compactEmptyResult: state.emptyResultCompact,
      noRuntimeErrors: state.runtimeErrors.length === 0,
    };

    fs.mkdirSync(screenshotDir, { recursive: true });
    await page.screenshot({
      path: path.join(screenshotDir, "emdadyar-mobile-android-wrapper.png"),
      fullPage: false,
    });

    await page.locator('[data-jump="#userGuide"]').first().click();
    await page.waitForTimeout(450);
    await page.screenshot({
      path: path.join(screenshotDir, "emdadyar-mobile-guide.png"),
      fullPage: false,
    });

    const report = {
      generated_at: new Date().toISOString(),
      target_url: targetUrl,
      test_mode: "headless Android-wrapper UI emulation; not a physical-device installation test",
      state,
      checks,
      passed: Object.values(checks).every(Boolean),
    };
    fs.mkdirSync(path.dirname(reportPath), { recursive: true });
    fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
    console.log(JSON.stringify(report, null, 2));
    if (!report.passed) process.exitCode = 1;
  } finally {
    await context.close();
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
