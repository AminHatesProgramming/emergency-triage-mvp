const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({
    executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    headless: true,
  });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("console", (msg) => {
    const text = msg.text();
    const expectedStaticMiss =
      text.includes("404 (File not found)") ||
      text.includes("501 (Unsupported method");
    if (msg.type() === "error" && !expectedStaticMiss) errors.push(text);
  });

  await page.goto("http://127.0.0.1:8765/", { waitUntil: "networkidle" });
  await page.click('[data-scenario="critical"]');
  await page.click('button[type="submit"][form="triageForm"], #triageForm button[type="submit"]');
  await page.waitForFunction(() => {
    const text = document.querySelector("#riskPercent")?.textContent || "";
    return text.includes("%") && !text.includes("--");
  }, { timeout: 15000 });

  const result = await page.evaluate(() => ({
    status: document.querySelector("#apiStatus")?.textContent,
    risk: document.querySelector("#riskLabel")?.textContent,
    percent: document.querySelector("#riskPercent")?.textContent,
    confidence: document.querySelector("#confidenceBand")?.textContent,
  }));
  await browser.close();

  if (errors.length) {
    throw new Error(`Browser errors: ${errors.join(" | ")}`);
  }
  console.log(JSON.stringify(result, null, 2));
})();
