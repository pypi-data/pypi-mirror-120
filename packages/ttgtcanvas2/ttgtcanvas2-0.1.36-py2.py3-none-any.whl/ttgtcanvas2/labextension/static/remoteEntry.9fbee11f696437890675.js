var _JUPYTERLAB;(()=>{"use strict";var e,r,t,n,a,o,i,u,c,l,s,f,d,p,h,v,b,g,m={1151:(e,r,t)=>{var n={"./index":()=>Promise.all([t.e(809),t.e(367),t.e(568)]).then((()=>()=>t(1568))),"./extension":()=>Promise.all([t.e(809),t.e(367),t.e(480)]).then((()=>()=>t(4480)))},a=(e,r)=>(t.R=r,r=t.o(n,e)?n[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),o=(e,r)=>{if(t.S){var n=t.S.default,a="default";if(n&&n!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[a]=e,t.I(a,r)}};t.d(r,{get:()=>a,init:()=>o})}},y={};function w(e){var r=y[e];if(void 0!==r)return r.exports;var t=y[e]={id:e,exports:{}};return m[e].call(t.exports,t,t.exports,w),t.exports}w.m=m,w.c=y,w.d=(e,r)=>{for(var t in r)w.o(r,t)&&!w.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},w.f={},w.e=e=>Promise.all(Object.keys(w.f).reduce(((r,t)=>(w.f[t](e,r),r)),[])),w.u=e=>e+"."+{25:"d367fef17dd84519eacf",367:"952f96696b30c27c755c",404:"ca7fcb5417faddcd67b8",480:"b09f25ce5d7b160e96d9",568:"80dc735b568e30d3fa67",809:"dcf2ef30a8ed6cdbf3f5"}[e]+".js?v="+{25:"d367fef17dd84519eacf",367:"952f96696b30c27c755c",404:"ca7fcb5417faddcd67b8",480:"b09f25ce5d7b160e96d9",568:"80dc735b568e30d3fa67",809:"dcf2ef30a8ed6cdbf3f5"}[e],w.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),w.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="ttgtcanvas2:",w.l=(t,n,a,o)=>{if(e[t])e[t].push(n);else{var i,u;if(void 0!==a)for(var c=document.getElementsByTagName("script"),l=0;l<c.length;l++){var s=c[l];if(s.getAttribute("src")==t||s.getAttribute("data-webpack")==r+a){i=s;break}}i||(u=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,w.nc&&i.setAttribute("nonce",w.nc),i.setAttribute("data-webpack",r+a),i.src=t),e[t]=[n];var f=(r,n)=>{i.onerror=i.onload=null,clearTimeout(d);var a=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),a&&a.forEach((e=>e(n))),r)return r(n)},d=setTimeout(f.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=f.bind(null,i.onerror),i.onload=f.bind(null,i.onload),u&&document.head.appendChild(i)}},w.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{w.S={};var e={},r={};w.I=(t,n)=>{n||(n=[]);var a=r[t];if(a||(a=r[t]={}),!(n.indexOf(a)>=0)){if(n.push(a),e[t])return e[t];w.o(w.S,t)||(w.S[t]={});var o=w.S[t],i="ttgtcanvas2",u=(e,r,t,n)=>{var a=o[e]=o[e]||{},u=a[r];(!u||!u.loaded&&(!n!=!u.eager?n:i>u.from))&&(a[r]={get:t,from:i,eager:!!n})},c=[];switch(t){case"default":u("konva","8.0.2",(()=>w.e(25).then((()=>()=>w(25))))),u("p-queue","7.1.0",(()=>w.e(404).then((()=>()=>w(404))))),u("ttgtcanvas2","0.1.3",(()=>Promise.all([w.e(809),w.e(367),w.e(568)]).then((()=>()=>w(1568)))))}return e[t]=c.length?Promise.all(c).then((()=>e[t]=1)):1}}})(),(()=>{var e;w.g.importScripts&&(e=w.g.location+"");var r=w.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");t.length&&(e=t[t.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),w.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),n=t[1]?r(t[1]):[];return t[2]&&(n.length++,n.push.apply(n,r(t[2]))),t[3]&&(n.push([]),n.push.apply(n,r(t[3]))),n},n=(e,r)=>{e=t(e),r=t(r);for(var n=0;;){if(n>=e.length)return n<r.length&&"u"!=(typeof r[n])[0];var a=e[n],o=(typeof a)[0];if(n>=r.length)return"u"==o;var i=r[n],u=(typeof i)[0];if(o!=u)return"o"==o&&"n"==u||"s"==u||"u"==o;if("o"!=o&&"u"!=o&&a!=i)return a<i;n++}},a=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var n=1,o=1;o<e.length;o++)n--,t+="u"==(typeof(u=e[o]))[0]?"-":(n>0?".":"")+(n=2,u);return t}var i=[];for(o=1;o<e.length;o++){var u=e[o];i.push(0===u?"not("+c()+")":1===u?"("+c()+" || "+c()+")":2===u?i.pop()+" "+i.pop():a(u))}return c();function c(){return i.pop().replace(/^\((.+)\)$/,"$1")}},o=(e,r)=>{if(0 in e){r=t(r);var n=e[0],a=n<0;a&&(n=-n-1);for(var i=0,u=1,c=!0;;u++,i++){var l,s,f=u<e.length?(typeof e[u])[0]:"";if(i>=r.length||"o"==(s=(typeof(l=r[i]))[0]))return!c||("u"==f?u>n&&!a:""==f!=a);if("u"==s){if(!c||"u"!=f)return!1}else if(c)if(f==s)if(u<=n){if(l!=e[u])return!1}else{if(a?l>e[u]:l<e[u])return!1;l!=e[u]&&(c=!1)}else if("s"!=f&&"n"!=f){if(a||u<=n)return!1;c=!1,u--}else{if(u<=n||s<f!=a)return!1;c=!1}else"s"!=f&&"n"!=f&&(c=!1,u--)}}var d=[],p=d.pop.bind(d);for(i=1;i<e.length;i++){var h=e[i];d.push(1==h?p()|p():2==h?p()&p():h?o(h,r):!p())}return!!p()},i=(e,r)=>{var t=w.S[e];if(!t||!w.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},u=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&n(e,r)?r:e),0)},c=(e,r,t)=>"Unsatisfied version "+r+" of shared singleton module "+e+" (required "+a(t)+")",l=(e,r,t,n)=>{var a=u(e,t);return o(n,a)||"undefined"!=typeof console&&console.warn&&console.warn(c(t,a,n)),f(e[t][a])},s=(e,r,t)=>{var a=e[r];return(r=Object.keys(a).reduce(((e,r)=>!o(t,r)||e&&!n(e,r)?e:r),0))&&a[r]},f=e=>(e.loaded=1,e.get()),p=(d=e=>function(r,t,n,a){var o=w.I(r);return o&&o.then?o.then(e.bind(e,r,w.S[r],t,n,a)):e(r,w.S[r],t,n,a)})(((e,r,t,n)=>(i(e,t),l(r,0,t,n)))),h=d(((e,r,t,n,a)=>{var o=r&&w.o(r,t)&&s(r,t,n);return o?f(o):a()})),v={},b={2565:()=>p("default","@jupyter-widgets/base",[,[1,4,0,0],[1,3,0,0],[1,2,0,0],[1,1,1,10],1,1,1]),8995:()=>h("default","konva",[1,8,0,2],(()=>w.e(25).then((()=>()=>w(25))))),9269:()=>h("default","p-queue",[1,7,1,0],(()=>w.e(404).then((()=>()=>w(404)))))},g={367:[2565,8995,9269]},w.f.consumes=(e,r)=>{w.o(g,e)&&g[e].forEach((e=>{if(w.o(v,e))return r.push(v[e]);var t=r=>{v[e]=0,w.m[e]=t=>{delete w.c[e],t.exports=r()}},n=r=>{delete v[e],w.m[e]=t=>{throw delete w.c[e],r}};try{var a=b[e]();a.then?r.push(v[e]=a.then(t).catch(n)):t(a)}catch(e){n(e)}}))},(()=>{var e={826:0};w.f.j=(r,t)=>{var n=w.o(e,r)?e[r]:void 0;if(0!==n)if(n)t.push(n[2]);else{var a=new Promise(((t,a)=>n=e[r]=[t,a]));t.push(n[2]=a);var o=w.p+w.u(r),i=new Error;w.l(o,(t=>{if(w.o(e,r)&&(0!==(n=e[r])&&(e[r]=void 0),n)){var a=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+a+": "+o+")",i.name="ChunkLoadError",i.type=a,i.request=o,n[1](i)}}),"chunk-"+r,r)}};var r=(r,t)=>{var n,a,[o,i,u]=t,c=0;for(n in i)w.o(i,n)&&(w.m[n]=i[n]);for(u&&u(w),r&&r(t);c<o.length;c++)a=o[c],w.o(e,a)&&e[a]&&e[a][0](),e[o[c]]=0},t=self.webpackChunkttgtcanvas2=self.webpackChunkttgtcanvas2||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})();var S=w(1151);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB).ttgtcanvas2=S})();