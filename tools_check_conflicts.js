// 用 Node 直接执行页面里的 CSV 装配逻辑，校验冲突表数据（与浏览器同一条代码路径）
const fs = require("fs");
const path = require("path");

const ROOT = process.argv[2] || ".";
const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];

const el = () => ({
  style: {}, classList: { add() {}, remove() {} }, dataset: {},
  setAttribute() {}, addEventListener() {}, textContent: "", innerHTML: "",
  appendChild() {}, querySelectorAll: () => [], querySelector: () => el(),
});
global.document = {
  getElementById: () => el(), querySelector: () => el(), querySelectorAll: () => [],
  body: el(), documentElement: el(), createElement: () => el(), addEventListener() {},
};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { search: "", href: "http://localhost/" };
global.fetch = (u) => Promise.resolve({
  ok: true, text: () => Promise.resolve(fs.readFileSync(path.join(ROOT, "data", u), "utf8")),
});

eval(js);

// 直接调用页面里的 assemble()（函数声明在 eval 后可见）
const texts = {};
CSV_FILES.forEach((n) => { texts[n] = fs.readFileSync(path.join(ROOT, "data", n), "utf8"); });
const PAYLOAD2 = assemble(texts);

setTimeout(() => {
  const PAYLOAD = PAYLOAD2;
  const rows = PAYLOAD.regions.cn.conflicts;
  console.log("冲突条数：", rows.length);
  let bad = 0;
  rows.forEach((r) => {
    const a = r.a.zh, b = r.b.zh;
    const broken = !a || !b || /[{}\[\]:]/.test(a) || /[{}\[\]:]/.test(b);
    if (broken) bad++;
    console.log((broken ? "  ✗ " : "  ✓ ") + r.code.padEnd(8) + " | " + String(a).slice(0, 40).padEnd(42) + " | " + String(b).slice(0, 40));
  });
  console.log("异常行：", bad);
  const fr = PAYLOAD.regions.fr.conflicts.slice(0, 4);
  console.log("\n法语区抽查：");
  fr.forEach((r) => console.log("  " + r.code.padEnd(8) + " | " + String(r.a.fr).slice(0, 46).padEnd(48) + " | " + String(r.b.fr).slice(0, 40)));
  const hk = PAYLOAD.regions.hk.conflicts.slice(0, 3);
  console.log("\n香港（繁体）抽查：");
  hk.forEach((r) => console.log("  " + r.code.padEnd(8) + " | " + String(r.a.zh).slice(0, 46).padEnd(48) + " | " + String(r.b.zh).slice(0, 40)));
}, 400);
