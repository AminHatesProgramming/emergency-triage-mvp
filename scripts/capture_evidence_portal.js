const { chromium } = require("playwright");
const path = require("path");
const { pathToFileURL } = require("url");

const root = path.resolve(__dirname, "..");
const pagePath = path.join(root, "docs", "evidence-portal", "index.html");
const outDir = path.join(root, "poster-assets");
const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

async function captureLocator(page, selector, name) {
  const locator = page.locator(selector);
  await locator.scrollIntoViewIfNeeded();
  await locator.screenshot({
    path: path.join(outDir, name),
    animations: "disabled",
  });
}

(async () => {
  const browser = await chromium.launch({
    executablePath: chromePath,
    headless: true,
  });

  const page = await browser.newPage({
    viewport: { width: 1680, height: 1200 },
    deviceScaleFactor: 1,
  });

  await page.goto(pathToFileURL(pagePath).href, { waitUntil: "networkidle" });
  await page.screenshot({
    path: path.join(outDir, "evidence-portal-overview.png"),
    fullPage: true,
    animations: "disabled",
  });

  await captureLocator(page, "#work-management-evidence", "agile-board-evidence.png");
  await captureLocator(page, "#knowledge-management-evidence", "knowledge-base-evidence.png");

  await browser.close();
  console.log("Captured evidence portal poster assets.");
})();
