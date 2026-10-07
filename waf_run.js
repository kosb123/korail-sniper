// Run korail WAF (dynaPath.do) JS in a minimal window/document shim and capture cookies.
const fs = require('fs');
const path = __dirname;
let dyna = fs.readFileSync(path + '\\dynaPath.txt', 'utf8');
// strip trailing });})(); wrappers so we can provide our own globals
// Build sandbox
const cookies = {};
function setCookie(str){
  const parts = str.split(';')[0];
  const idx = parts.indexOf('=');
  const name = parts.slice(0, idx).trim();
  let val = parts.slice(idx+1).trim();
  cookies[name] = val;
}
const document = {
  get cookie(){ return Object.entries(cookies).map(([k,v])=>k+'='+v).join('; '); },
  set cookie(v){ setCookie(v); },
  createElement: (t)=>({ style:{}, setAttribute(){}, appendChild(){}, addEventListener(){}, getContext:()=>({}) , querySelector:()=>null, children:[] }),
  head: { appendChild(){}, querySelector:()=>null },
  body: { appendChild(){}, querySelector:()=>null },
  querySelector: (s)=>({ style:{}, setAttribute(){}, addEventListener(){}, getContext:()=>({}), classList:{add(){},remove(){},toggle(){}}, dataset:{} }),
  querySelectorAll: ()=>[],
  getElementById: ()=>null,
  addEventListener(){},
  removeEventListener(){},
  scripts: [],
  location: { href:'https://www.korail.com/ticket', protocol:'https:', host:'www.korail.com', pathname:'/ticket' },
  navigator: { userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', language:'ko-KR' },
  readyState:'complete',
};
const timers = [];
const window = {
  document,
  setTimeout:(fn,ms)=>{ try{ fn(); }catch(e){} return 0; },
  setInterval:()=>0,
  clearTimeout(){}, clearInterval(){},
  navigator: document.navigator,
  location: document.location,
  addEventListener(){}, removeEventListener(){},
  getComputedStyle:()=>({}),
  localStorage:{ getItem:()=>null, setItem(){}, removeItem(){} },
  screen:{ width:1920, height:1080, availWidth:1920, availHeight:1040 },
  devicePixelRatio:1,
  requestAnimationFrame:(fn)=>{ try{fn();}catch(e){} return 0; },
  performance: { now: ()=>Date.now() },
  Date, JSON, Math, Symbol, Function, Promise, RegExp, String, Number, Array, Object,
};
window.window = window;
window.globalThis = window;
// expose common globals the obfuscated code may reference
const sandbox = { window, document, navigator:document.navigator, setTimeout:window.setTimeout, setInterval:window.setInterval, clearTimeout:window.clearTimeout, setInterval:window.setInterval, Symbol, Function, Promise, Math, Date, JSON, console, XMLHttpRequest:undefined, navigator:document.navigator, self:window, top:window, parent:window, history:{ pushState(){}, replaceState(){}, go(){} }, alert(){}, confirm:()=>true };
global.window = window; global.document = document; global.navigator = document.navigator;

const vm = require('vm');
const ctx = vm.createContext(sandbox);
try {
  vm.runInContext(dyna, ctx, { filename:'dynaPath.js', timeout:5000 });
} catch(e){ console.error('VM ERR', e.message); }
// also flush any synchronous timers already fired; the script uses setTimeout(A, 0xa) then a recursive retry
// Give a little real time for any setTimeout that we ran synchronously already (we ran fn immediately)
console.error('COOKIES:', JSON.stringify(cookies));
fs.writeFileSync(path + '\\waf_cookies.json', JSON.stringify(cookies, null, 1));
process.exit(0);
