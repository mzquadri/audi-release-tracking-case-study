/**
 * Rasterise every figure, so a change can be looked at before it is committed.
 *
 *   node tools/preview.mjs
 *
 * Writes docs/figures/.preview-<name>-<theme>.png, which .gitignore keeps out
 * of the repository: the SVGs are the deliverable and a PNG of one is a
 * working file.
 */
import { chromium } from "playwright";
import { readFile, readdir } from "node:fs/promises";
import { join } from "node:path";

const DIR = new URL("../docs/figures/", import.meta.url).pathname
  .replace(/^\/([A-Za-z]:)/, "$1");

const files = (await readdir(DIR)).filter((f) => f.endsWith(".svg"));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 700 } });

for (const f of files) {
  const svg = await readFile(join(DIR, f), "utf-8");
  await page.setContent(`<body style="margin:0">${svg}</body>`);
  const out = join(DIR, `.preview-${f.replace(/\.svg$/, "")}.png`);
  await page.locator("svg").screenshot({ path: out });
  console.log(`  ${out}`);
}

await browser.close();
