/*! For license information please see 0983cdaf.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[5214],{63207:(t,e,i)=>{"use strict";i(65660),i(15112);var n=i(9672),s=i(87156),r=i(50856),o=i(94604);(0,n.k)({_template:r.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:o.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,s.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,s.vz)(this.root).appendChild(this._img))}})},15112:(t,e,i)=>{"use strict";i.d(e,{P:()=>s});i(94604);var n=i(9672);class s{constructor(t){s[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}get value(){var t=this.type,e=this.key;if(t&&e)return s.types[t]&&s.types[t][e]}set value(t){var e=this.type,i=this.key;e&&i&&(e=s.types[e]=s.types[e]||{},null==t?delete e[i]:e[i]=t)}get list(){if(this.type){var t=s.types[this.type];return t?Object.keys(t).map((function(t){return r[this.type][t]}),this):[]}}byKey(t){return this.key=t,this.value}}s[" "]=function(){},s.types={};var r=s.types;(0,n.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,i){var n=new s({type:t,key:e});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new s({type:this.type,key:t}).value}})},98626:(t,e,i)=>{"use strict";i.d(e,{ZH:()=>u,MT:()=>r,U2:()=>c,RV:()=>s,t8:()=>h});var n=i(21354);function s(t){return new Promise(((e,i)=>{t.oncomplete=t.onsuccess=()=>e(t.result),t.onabort=t.onerror=()=>i(t.error)}))}function r(t,e){const i=(0,n.Z)().then((()=>{const i=indexedDB.open(t);return i.onupgradeneeded=()=>i.result.createObjectStore(e),s(i)}));return(t,n)=>i.then((i=>n(i.transaction(e,t).objectStore(e))))}let o;function a(){return o||(o=r("keyval-store","keyval")),o}function c(t,e=a()){return e("readonly",(e=>s(e.get(t))))}function h(t,e,i=a()){return i("readwrite",(i=>(i.put(e,t),s(i.transaction))))}function u(t=a()){return t("readwrite",(t=>(t.clear(),s(t.transaction))))}},76666:(t,e,i)=>{"use strict";i.d(e,{$:()=>n.$});var n=i(81471)},82816:(t,e,i)=>{"use strict";i.d(e,{o:()=>n.o});var n=i(49629)},21354:(t,e,i)=>{"use strict";i.d(e,{Z:()=>n});const n=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let t;return new Promise((e=>{const i=()=>indexedDB.databases().finally(e);t=setInterval(i,100),i()})).finally((()=>clearInterval(t)))}}}]);
//# sourceMappingURL=0983cdaf.js.map