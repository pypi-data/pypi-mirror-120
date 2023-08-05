(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[70151],{43274:(e,t,r)=>{"use strict";r.d(t,{Sb:()=>i,BF:()=>n,Op:()=>o});const i=function(){try{(new Date).toLocaleDateString("i")}catch(e){return"RangeError"===e.name}return!1}(),n=function(){try{(new Date).toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}return!1}(),o=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()},44583:(e,t,r)=>{"use strict";r.d(t,{o0:()=>s,E8:()=>l});var i=r(68928),n=r(14516),o=r(43274),a=r(65810);const s=o.Op?(e,t)=>c(t).format(e):(e,t)=>(0,i.WU)(e,((0,a.y)(t)," A")),c=(0,n.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,a.y)(e)}))),l=o.Op?(e,t)=>u(t).format(e):(e,t)=>(0,i.WU)(e,((0,a.y)(t)," A")),u=(0,n.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",second:"2-digit",hour12:(0,a.y)(e)})));(0,n.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"numeric",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,a.y)(e)})))},65810:(e,t,r)=>{"use strict";r.d(t,{y:()=>o});var i=r(14516),n=r(66477);const o=(0,i.Z)((e=>{if(e.time_format===n.zt.language||e.time_format===n.zt.system){const t=e.time_format===n.zt.language?e.language:void 0,r=(new Date).toLocaleString(t);return r.includes("AM")||r.includes("PM")}return e.time_format===n.zt.am_pm}))},25516:(e,t,r)=>{"use strict";r.d(t,{i:()=>i});const i=e=>t=>({kind:"method",placement:"prototype",key:t.key,descriptor:{set(e){this[`__${String(t.key)}`]=e},get(){return this[`__${String(t.key)}`]},enumerable:!0,configurable:!0},finisher(r){const i=r.prototype.connectedCallback;r.prototype.connectedCallback=function(){if(i.call(this),this[t.key]){const r=this.renderRoot.querySelector(e);if(!r)return;r.scrollTop=this[t.key]}}}})},96151:(e,t,r)=>{"use strict";r.d(t,{T:()=>i,y:()=>n});const i=e=>{requestAnimationFrame((()=>setTimeout(e,0)))},n=()=>new Promise((e=>{i(e)}))},93748:(e,t,r)=>{"use strict";r.d(t,{Es:()=>n,SC:()=>o,cV:()=>s,Ip:()=>c,Pl:()=>l});var i=r(83849);const n=(e,t)=>{e.callService("automation","trigger",{entity_id:t,skip_condition:!0})},o=(e,t)=>e.callApi("DELETE",`config/automation/config/${t}`);let a;const s=(e,t)=>e.callApi("GET",`config/automation/config/${t}`),c=e=>{a=e,(0,i.c)("/config/automation/edit/new")},l=()=>{const e=a;return a=void 0,e}},56007:(e,t,r)=>{"use strict";r.d(t,{nZ:()=>i,lz:()=>n,V_:()=>o});const i="unavailable",n="unknown",o=[i,n]},83114:(e,t,r)=>{"use strict";r.r(t);r(22098),r(48932),r(25230),r(54444);var i=r(50424),n=r(55358),o=(r(42173),r(47181)),a=r(83849),s=(r(47150),r(36125),r(52039),r(67556),r(93748)),c=r(11654),l=r(22311),u=r(44583),d=r(14516);r(67065);function h(){h=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!m(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function p(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function k(e,t,r){return(k="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=w(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function w(e){return(w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var n=h();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(y(o.descriptor)||y(n.descriptor)){if(m(o)||m(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(m(o)){if(m(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}f(o,n)}else t.push(o)}return t}(a.d.map(p)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("ha-panel-aisttsauto")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",key:"_columns",value(){return(0,d.Z)(((e,t)=>{const r={toggle:{title:i.dy`&nbsp;&nbsp;&nbsp;&nbsp;<ha-svg-icon
              path=${"M1,11H3.17C3.58,9.83 4.69,9 6,9C6.65,9 7.25,9.21 7.74,9.56L14.44,4.87L15.58,6.5L8.89,11.2C8.96,11.45 9,11.72 9,12A3,3 0 0,1 6,15C4.69,15 3.58,14.17 3.17,13H1V11M23,11V13H20.83C20.42,14.17 19.31,15 18,15A3,3 0 0,1 15,12A3,3 0 0,1 18,9C19.31,9 20.42,9.83 20.83,11H23M6,11A1,1 0 0,0 5,12A1,1 0 0,0 6,13A1,1 0 0,0 7,12A1,1 0 0,0 6,11M18,11A1,1 0 0,0 17,12A1,1 0 0,0 18,13A1,1 0 0,0 19,12A1,1 0 0,0 18,11Z"}
            ></ha-svg-icon>`,type:"icon",template:(e,t)=>i.dy`
              <ha-checkbox
                .key=${t.id}
                .hass=${this.hass}
                @change=${this._handleRowCheckboxClick}
                .checked=${"on"===t.entity.state}
              >
              </ha-checkbox>
            `},name:{title:"Nazwa",sortable:!0,filterable:!0,direction:"asc",grows:!0}};return e||(r.last_triggered={sortable:!0,width:"20%",title:this.hass.localize("ui.card.automation.last_triggered"),template:e=>i.dy`
            ${e?(0,u.o0)(new Date(e),this.hass.locale):this.hass.localize("ui.components.relative_time.never")}
          `},r.trigger={title:i.dy`
            <mwc-button style="visibility: hidden">
              ${this.hass.localize("ui.card.automation.trigger")}
            </mwc-button>
          `,width:"20%",template:(e,t)=>i.dy`
            <mwc-button
              .automation=${t.entity}
              @click=${e=>this._runActions(e)}
            >
              URUCHOM
            </mwc-button>
          `}),this.hass.user.is_admin&&(r.info={title:"",type:"icon-button",template:(e,t)=>i.dy`
            <mwc-icon-button
              .automation=${t.entity}
              @click=${this._showInfo}
              label="Info"
            >
              <ha-svg-icon .path=${"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"}></ha-svg-icon>
            </mwc-icon-button>
          `},r.trace={title:"",type:"icon-button",template:(e,t)=>i.dy`
            <a
              href="/config/automation/trace/${t.entity.attributes.id}"
            >
              <mwc-icon-button label="Ślad">
                <ha-svg-icon .path=${"M13.5,8H12V13L16.28,15.54L17,14.33L13.5,12.25V8M13,3A9,9 0 0,0 4,12H1L4.96,16.03L9,12H6A7,7 0 0,1 13,5A7,7 0 0,1 20,12A7,7 0 0,1 13,19C11.07,19 9.32,18.21 8.06,16.94L6.64,18.36C8.27,20 10.5,21 13,21A9,9 0 0,0 22,12A9,9 0 0,0 13,3"}></ha-svg-icon>
              </mwc-icon-button>
            </a>
          `},r.edit={title:"",type:"icon-button",template:(e,t)=>i.dy`
            <a
              href="/config/automation/edit/${t.entity.attributes.id}"
            >
              <mwc-icon-button label="Edit">
                <ha-svg-icon path=${"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"}></ha-svg-icon>
              </mwc-icon-button>
            </a>
          `}),r}))}},{kind:"method",key:"firstUpdated",value:function(e){k(w(r.prototype),"firstUpdated",this).call(this,e)}},{kind:"method",key:"_get_automations",value:function(e){const t=[];return Object.values(this.hass.states).forEach((e=>{"automation"!==(0,l.N)(e)||e.entity_id.startsWith("automation.ais_")||t.push({id:e.entity_id,name:e.attributes.friendly_name,last_triggered:e.attributes.last_triggered,entity:e})})),t}},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-app-layout>
        <app-header slot="header" fixed>
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title>TTS Automatyczny</div>
            ${this.hass.user.is_admin?i.dy`<ha-icon-button
                  label="Dodaj"
                  icon="hass:plus"
                  @click=${this._createNew}
                ></ha-icon-button>`:i.dy``}
          </app-toolbar>
        </app-header>
        <ha-card class="content">
          <ha-data-table
            .columns=${this._columns(this.narrow,this.hass.locale)}
            .data=${this._get_automations(this.hass.states)}
            auto-height
            searchLabel="Szukaj"
            noDataText="Brak danych"
          ></ha-data-table>
        </ha-card>
      </ha-app-layout>
    `}},{kind:"method",key:"_showInfo",value:function(e){e.stopPropagation();const t=e.currentTarget.automation.entity_id;(0,o.B)(this,"hass-more-info",{entityId:t})}},{kind:"method",key:"_runActions",value:function(e){const t=e.currentTarget.automation.entity_id;(0,s.Es)(this.hass,t)}},{kind:"method",key:"_createNew",value:function(){(0,a.c)("/config/automation/edit/new")}},{kind:"method",key:"_handleRowCheckboxClick",value:function(e){const t=e.currentTarget.key,r=e.currentTarget.hass;let i="off";e.currentTarget.checked&&(i="on"),r.callService("ais_tts","change_auto_mode",{entity_id:t,change_to:i})}},{kind:"get",static:!0,key:"styles",value:function(){return[c.Qx,i.iv`
        ha-card.content {
          padding: 16px;
        }

        .has-header {
          padding-top: 0;
        }

        .checked span {
          color: var(--primary-color);
        }
        .content {
          padding-bottom: 32px;
          max-width: 94%;
          margin: 0 auto;
        }
      `]}}]}}),i.oi)}}]);
//# sourceMappingURL=08d02ffd.js.map