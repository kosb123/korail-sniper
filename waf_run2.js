// WAF runner v2: real XHR via node fetch, capture cookies + log the cdn/dyna URL.
const fs = require('fs');
const path = __dirname;
const dyna = fs.readFileSync(path + '\\dynaPath.txt', 'utf8');

const cookies = {};
function setCookie(str){
  const part = String(str).split(';')[0];
  const idx = part.indexOf('=');
  if (idx < 0) return;
  cookies[part.slice(0, idx).trim()] = part.slice(idx + 1).trim();
}

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36';
// Capture REAL node timers before we overwrite globals (payload calls window.setTimeout -> must not recurse).
const realSetTimeout = setTimeout, realSetInterval = setInterval, realClearTimeout = clearTimeout, realClearInterval = clearInterval;

class XHR {
  constructor(){ this.readyState=0; this.status=0; this.responseText=''; this.response=''; this.timeout=0;
    this.headers={}; this.onload=null; this.onerror=null; this.onabort=null; this.onreadystatechange=null; }
  open(method,url,async){ this._method=method; this._url=url; this.readyState=1; if(this.onreadystatechange)this.onreadystatechange(); }
  setRequestHeader(k,v){ this.headers[k]=v; }
  getAllResponseHeaders(){ return Object.entries(this.headers).map(([k,v])=>k+': '+v).join('\r\n'); }
  getResponseHeader(k){ return this.headers[k.toLowerCase()]||null; }
  abort(){}
  send(body){
    const self=this;
    console.error('XHR open', self._method, self._url, 'headers:', JSON.stringify(self.headers));
    self.readyState=2; if(self.onreadystatechange)self.onreadystatechange();
    (async()=>{
      try{
        const opt={ method:self._method, headers:{ 'User-Agent':UA, 'Origin':'https://www.korail.com','Referer':'https://www.korail.com/ticket', ...(self.headers||{}) } };
        if(self._method!=='GET' && self._method!=='HEAD' && body) opt.body=body;
        const res=await fetch(self._url, opt);
        const txt=await res.text();
        fs.writeFileSync(`${path}/cdn_payload_${(self._url.split('/').pop()||'x')}.js`, txt);
        console.error('XHR saved payload', self._url, 'len', txt.length);
        // parse set-cookie
        const sc=res.headers.getSetCookie? res.headers.getSetCookie() : (res.headers.get('set-cookie')?[res.headers.get('set-cookie')]:[]);
        sc.forEach(c=>setCookie(c));
        self.status=res.status; self.statusText=res.statusText; self.responseText=txt; self.response=txt; self.responseURL=self._url;
        self.readyState=4; if(self.onreadystatechange)self.onreadystatechange(); if(self.onload)self.onload();
      }catch(e){ self.readyState=4; if(self.onerror)self.onerror(e); }
    })();
  }
}

const document = {
  get cookie(){ return Object.entries(cookies).map(([k,v])=>k+'='+v).join('; '); },
  set cookie(v){ setCookie(v); },
  createElement:(t)=>({ style:{}, setAttribute(){}, appendChild(){}, removeChild(){}, addEventListener(){}, removeEventListener(){}, getContext:()=>({}), querySelector:()=>null, querySelectorAll:()=>[], children:[], classList:{add(){},remove(){},toggle(){},contains:()=>false}, dataset:{}, textContent:'', innerHTML:'', src:'', charset:'', readyState:0, onload:null }),
  head:{ appendChild(){}, removeChild(){}, querySelector:()=>null, querySelectorAll:()=>[] },
  body:{ appendChild(){}, removeChild(){}, querySelector:()=>null, querySelectorAll:()=>[], style:{} },
  querySelector:(s)=>({ style:{}, setAttribute(){}, appendChild(){}, removeChild(){}, addEventListener(){}, removeEventListener(){}, getContext:()=>({}), querySelector:()=>null, querySelectorAll:()=>[], classList:{add(){},remove(){},toggle(){},contains:()=>false}, dataset:{}, textContent:'', innerHTML:'', src:'', children:[] }),
  querySelectorAll:()=>[],
  getElementById:()=>null,
  createTextNode:()=>({}),
  addEventListener(){}, removeEventListener(){},
  scripts:[], location:{ href:'https://www.korail.com/ticket', protocol:'https:', host:'www.korail.com', hostname:'www.korail.com', pathname:'/ticket', search:'', hash:'' , origin:'https://www.korail.com'},
  readyState:'complete',
  title:'',
  referrer:'https://www.korail.com/ticket',
};
const navigatorObj={ userAgent:UA, language:'ko-KR', languages:['ko-KR','ko','en'], platform:'Win32', hardwareConcurrency:8, maxTouchPoints:0, onLine:true, vendor:'Google Inc.', cookieEnabled:true, appVersion:'5.0 (Windows NT 10.0; Win64; x64)', appName:'Netscape', appCodeName:'Mozilla', doNotTrack:null, connection:{ effectiveType:'4g', downlink:10, rtt:50, saveData:false } };

const timers=[];
const window={
  document, navigator:navigatorObj,
  setTimeout:(fn,ms,...a)=>{ return realSetTimeout(()=>{ try{fn(...a);}catch(e){console.error('setTimeout fn err',e.message);} }, ms==null?0:ms); },
  setInterval:(fn,ms)=>{ return realSetInterval(fn, ms==null?0:ms); }, clearTimeout:(id)=>realClearTimeout(id), clearInterval:(id)=>realClearInterval(id),
  addEventListener(){}, removeEventListener(){},
  getComputedStyle:()=>({ getPropertyValue:()=>'' }),
  requestAnimationFrame:(fn)=>{ return realSetTimeout(()=>{ try{fn(Date.now());}catch(e){console.error('rAF fn err',e.message);} }, 16); },
  cancelAnimationFrame:(id)=>realClearTimeout(id),
  localStorage:{ getItem:()=>null, setItem(){}, removeItem(){}, clear(){} },
  sessionStorage:{ getItem:()=>null, setItem(){}, removeItem(){}, clear(){} },
  screen:{ width:1920, height:1080, availWidth:1920, availHeight:1040, colorDepth:24, pixelDepth:24, orientation:{ type:'landscape-primary', angle:0 } },
  devicePixelRatio:1, innerWidth:1920, innerHeight:1040, outerWidth:1920, outerHeight:1080,
  pageXOffset:0, pageYOffset:0, scrollX:0, scrollY:0,
  location:document.location,
  history:{ pushState(){}, replaceState(){}, go(){}, back(){} , state:null, length:1},
  performance: (typeof performance!=='undefined'? performance : { now:()=>Date.now() }),
  XMLHttpRequest: XHR,
  Image:function(){ return { src:'', onload:null, onerror:null, width:0, height:0 }; },
  alert(){}, confirm:()=>true, prompt:()=>null, focus(){}, blur(){}, print(){},
  matchMedia:()=>({ matches:false, media:'', addListener(){}, removeListener(){}, addEventListener(){}, removeEventListener(){}, onchange:null, dispatchEvent:()=>false }),
  getSelection:()=>({ rangeCount:0, getRangeAt:()=>null, removeAllRanges(){}, collapse(){} }),
  btoa:(s)=>Buffer.from(s,'binary').toString('base64'),
  atob:(s)=>Buffer.from(s,'base64').toString('binary'),
  crypto:{ getRandomValues:(a)=>{ for(let i=0;i<a.length;i++)a[i]=Math.floor(Math.random()*256); return a; }, randomUUID:()=>require('crypto').randomUUID(), subtle:{} },
  Function, Promise, Math, Date, JSON, Symbol, RegExp, String, Number, Array, Object, Error, TypeError, parseInt, parseFloat, isNaN, console,
  URL, URLSearchParams, TextEncoder, TextDecoder, encodeURIComponent, decodeURIComponent,
};
window.window=window; window.self=window; window.top=window; window.parent=window; window.globalThis=window;
window.navigator=navigatorObj; window.document=document;

// The WAF payload runs inside host `new Function(...)` -> host global scope.
// Expose everything it may touch on the Node host globals.
let ok=0, fail=0;
for (const [k,v] of Object.entries({ window, document, navigator:navigatorObj, self:window, top:window, parent:window, location:document.location, history:window.history, XMLHttpRequest:XHR, fetch, setTimeout:window.setTimeout, setInterval:window.setInterval, localStorage:window.localStorage, sessionStorage:window.sessionStorage, screen:window.screen, performance:window.performance, matchMedia:window.matchMedia, getComputedStyle:window.getComputedStyle, btoa:window.btoa, atob:window.atob, crypto:window.crypto, Image:window.Image, alert:()=>{}, confirm:()=>true, prompt:()=>null, requestAnimationFrame:window.requestAnimationFrame, cancelAnimationFrame:window.cancelAnimationFrame, devicePixelRatio:1, innerWidth:1920, innerHeight:1040, outerWidth:1920, outerHeight:1080, pageXOffset:0, pageYOffset:0, scrollX:0, scrollY:0, addEventListener:()=>{}, removeEventListener:()=>{}, dispatchEvent:()=>true, focus:()=>{}, blur:()=>{}, open:()=>null, close:()=>{}, postMessage:()=>{}, getSelection:window.getSelection })) {
  try { Object.defineProperty(globalThis, k, { value:v, writable:true, configurable:true, enumerable:false }); ok++; }
  catch(e) { fail++; console.error('SET FAIL', k, e.message); try { globalThis[k]=v; ok++; } catch(_e){ console.error('SET FAIL2', k, _e.message); } }
}
console.error('LOOP done ok=',ok,'fail=',fail,'rAF after loop=', typeof globalThis.requestAnimationFrame, 'XHR after=', typeof globalThis.XMLHttpRequest);

const vm=require('vm');
console.error('DBG host globals: rAF=', typeof requestAnimationFrame, 'window=', typeof window, 'document=', typeof (typeof document!=='undefined'?document:null), 'XHR=', typeof XMLHttpRequest);
const sandbox=Object.assign({}, window, { window, self:window, top:window, parent:window, globalThis:window, document, navigator:navigatorObj,
  setTimeout:window.setTimeout, setInterval:window.setInterval, clearTimeout:window.clearTimeout, clearInterval:window.clearInterval,
  fetch, console, XMLHttpRequest:XHR });
const ctx=vm.createContext(sandbox);
console.error('CHK: window.requestAnimationFrame=', typeof window.requestAnimationFrame, 'sandbox.requestAnimationFrame=', typeof sandbox.requestAnimationFrame, 'ctx rAF=', vm.runInContext('typeof requestAnimationFrame', ctx), 'ctx window=', vm.runInContext('typeof window', ctx));

const t0=Date.now();
try{
  vm.runInContext(dyna, ctx, { filename:'dynaPath.js', timeout:8000 });
}catch(e){ console.error('VM top err', e.message, e.stack&&e.stack.split('\n').slice(0,3).join(' | ')); }

// Allow async XHR + inner new Function to settle
setTimeout(()=>{
  console.error('elapsed', Date.now()-t0, 'ms');
  console.error('COOKIES:', JSON.stringify(cookies, null, 1));
  fs.writeFileSync(path+'\\waf_cookies.json', JSON.stringify(cookies, null, 1));
  console.error('cookie count', Object.keys(cookies).length);
  process.exit(0);
}, 15000);
