// 用 Node 跑页面里的渲染逻辑，核对页脚（更新日期/下载链接/检查更新按钮/联系方式）
const fs = require("fs");
const path = require("path");

const ROOT = process.argv[2] || ".";
const file = process.argv[3] || "施工图材料代码多语对照表.html";
const html = fs.readFileSync(path.join(ROOT, file), "utf8");
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];

const store = {};
const el = (id) => ({
  id, style: {}, dataset: {}, classList: { add() {}, remove() {} },
  setAttribute() {}, getAttribute: () => "dark", addEventListener() {}, appendChild() {},
  querySelectorAll: () => [], querySelector: () => el(),
  set innerHTML(v) { store[id] = v; },
  set textContent(v) { store[id + ":text"] = String(v); },
  get innerHTML() { return store[id] || ""; },
  textContent: "", value: "",
});
global.document = {
  getElementById: (id) => el(id),
  querySelector: (sel) => el(String(sel).replace(/^#/, "")),
  querySelectorAll: () => [],
  body: el("body"), documentElement: el("html"), createElement: () => el("tmp"), addEventListener() {},
};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { search: "", href: "http://localhost/", hostname: "localhost" };
global.fetch = (u) => {
  const name = String(u).replace(/^.*data\//, "");
  try { return Promise.resolve({ ok: true, status: 200, url: u,
    text: () => Promise.resolve(fs.readFileSync(path.join(ROOT, "data", name), "utf8")) }); }
  catch (e) { return Promise.resolve({ ok: false, status: 404, url: u, text: () => Promise.resolve("") }); }
};
global.confirm = () => false;

eval(js);

setTimeout(() => {
  console.log("bootErr:", String(store["bootErr:text"] || store["bootErr"] || "(无)"));
  try { console.log("PAYLOAD 已装配:", typeof PAYLOAD !== "undefined" && PAYLOAD ? "是，地区数 " + PAYLOAD.regionOrder.length : "否"); }
  catch(e){ console.log("PAYLOAD 读取失败:", e.message); }
  console.log("已写入的节点:", Object.keys(store).join(", "));
  console.log("=== 页脚渲染结果 ===");
  console.log("更新日期行 :", String(store["footDate"] || "").replace(/<[^>]+>/g, ""));
  console.log("  含下载链接:", /<a href="[^"]*releases[^"]*"[^>]*>/.test(store["footDate"] || ""));
  console.log("  链接地址  :", (String(store["footDate"] || "").match(/href="([^"]+)"/) || [])[1]);
  console.log("检查更新行 :", String(store["footUpdate"] || "").replace(/<[^>]+>/g, " "));
  console.log("  按钮存在  :", /update-btn/.test(store["footUpdate"] || ""));
  console.log("联系方式行:", String(store["footContact"] || "").replace(/<[^>]+>/g, " "));
  console.log("  仓库链接 :", (String(store["footContact"] || "").match(/href="([^"]+)"/) || [])[1]);
  console.log("  邮箱链接 :", (String(store["footContact"] || "").match(/mailto:[^"]+/) || [])[0]);
}, 600);
