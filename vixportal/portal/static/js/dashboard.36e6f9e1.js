(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["dashboard"],{"0c6d":function(t,e,i){"use strict";i.d(e,"c",(function(){return o})),i.d(e,"a",(function(){return n})),i.d(e,"b",(function(){return r}));var a=i("bc3a"),s=i.n(a);function o(t){var e=s.a.create({baseURL:window.url.ssourl,timeout:5e3});return e(t)}function n(t){var e=s.a.create({baseURL:window.url.coreurl,timeout:5e3});return e(t)}function r(t){var e=s.a.create({baseURL:window.url.vneturl,timeout:5e3});return e(t)}},"2c8a":function(t,e,i){!function(e,i){t.exports=i()}(0,(function(){"use strict";function t(t,e){for(var i=0;i<e.length;i++){var a=e[i];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(t,a.key,a)}}function e(t){return function(t){if(Array.isArray(t)){for(var e=0,i=new Array(t.length);e<t.length;e++)i[e]=t[e];return i}}(t)||function(t){if(Symbol.iterator in Object(t)||"[object Arguments]"===Object.prototype.toString.call(t))return Array.from(t)}(t)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance")}()}var i=window.devicePixelRatio||1,a=10*i,s=a/2;return function(){function o(t,e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,o),this.canvas=function(t){var e=document.getElementById(t),a=e.parentNode.clientWidth,s=e.parentNode.clientHeight;return e.style.width=a+"px",e.style.height=s+"px",e.width=a*i,e.height=s*i,e}(t),this.ctx=this.canvas.getContext("2d"),this.type="bar",this.showValue=!0,this.showGrid=!0,this.topPadding=60*i,this.leftPadding=50*i,this.rightPadding=10*i,this.bottomPadding=50*i,this.yEqual=5,this.yLength=0,this.xLength=0,this.ySpace=0,this.xRorate=0,this.yRorate=0,this.xRotate=0,this.yRotate=0,this.bgColor="#fff",this.axisColor="#666",this.gridColor="#eee",this.title={text:"",color:"#666",position:"top",font:"bold "+18*i+"px Arial",top:a,bottom:s},this.legend={display:!0,position:"top",color:"#666",font:14*i+"px Arial",top:45*i,bottom:15*i,textWidth:0},this.radius=100*i,this.innerRadius=60*i,this.colorList=["#4A90E2","#F5A623","#ff5858","#5e64ff","#2AC766","#743ee2","#b554ff","#199475"],this.init(e)}return function(e,i,a){i&&t(e.prototype,i),a&&t(e,a)}(o,[{key:"init",value:function(t){if(t.title=Object.assign({},this.title,t.title),t.legend=Object.assign({},this.legend,t.legend),Object.assign(this,t),!t.labels||!t.labels.length)throw new Error("缺少主要参数labels");if(!t.datasets||!t.datasets.length)throw new Error("缺少主要参数datasets");this.drawBackground(),"bar"===this.type||"line"===this.type?this.renderBarChart():this.renderPieChart(),this.drawLegend()}},{key:"renderBarChart",value:function(){this.yLength=Math.floor((this.canvas.height-this.topPadding-this.bottomPadding-a)/this.yEqual),this.xLength=Math.floor((this.canvas.width-this.leftPadding-this.rightPadding-a)/this.labels.length),this.ySpace=function(t,i){var a=t.map((function(t){return t.data.reduce((function(t,e){return e<t?t:e}))})),s=Math.ceil(Math.max.apply(Math,e(a))/i),o=s.toString().length-1;return o=2<o?2:o,Math.ceil(s/Math.pow(10,o))*Math.pow(10,o)}(this.datasets,this.yEqual),this.drawXAxis(),this.drawYAxis(),this.drawBarContent()}},{key:"drawBarContent",value:function(){var t=this.ctx,e=this.datasets.length;t.beginPath();for(var o=0;o<e;o++){t.font=this.legend.font,this.legend.textWidth+=Math.ceil(t.measureText(this.datasets[o].label).width),t.fillStyle=t.strokeStyle=this.datasets[o].fillColor||this.colorList[o];for(var n=this.datasets[o].data,r=0;r<n.length;r++)if(!(r>this.labels.length-1)){var l=this.xLength/(e+1),h=this.yLength/this.ySpace,c=this.leftPadding+this.xLength*r+l*(o+.5),d=c+l,f=this.canvas.height-this.bottomPadding,g=f-n[r]*h;if("bar"===this.type)t.fillRect(c,g,d-c,f-g),this.drawValue(n[r],c+l/2,g-s);else if("line"===this.type){var u=this.leftPadding+this.xLength*(r+.5);t.beginPath(),t.arc(u,g,3*i,0,2*Math.PI,!0),t.fill(),0!==r&&(t.beginPath(),t.strokeStyle=this.datasets[o].fillColor||this.colorList[o],t.lineWidth=2*i,t.moveTo(u-this.xLength,f-n[r-1]*h),t.lineTo(u,g),t.stroke(),t.lineWidth=1*i),this.drawValue(n[r],u,g-a)}}}t.stroke()}},{key:"renderPieChart",value:function(){for(var t=this.ctx,e=this.labels.length,i=this.datasets[0],a=i.data,s=a.reduce((function(t,e){return t+e})),o=-Math.PI/2,n=this.canvas.width/2,r=this.canvas.height/2,l=0;l<e;l++){t.font=this.legend.font,this.legend.textWidth+=Math.ceil(t.measureText(this.labels[l]).width),t.beginPath(),t.strokeStyle=t.fillStyle=i.colorList&&i.colorList[l]||this.colorList[l],t.moveTo(n,r);var h=o,c=o+=a[l]/s*2*Math.PI;t.arc(n,r,this.radius,h,c),t.closePath(),t.fill();var d=(h+c)/2;this.drawPieValue(a[l],d)}"ring"===this.type&&(t.beginPath(),t.fillStyle=this.bgColor,t.arc(n,r,this.innerRadius,0,2*Math.PI),t.closePath(),t.fill())}},{key:"drawValue",value:function(t,e,a){var s=this.ctx;this.showValue&&(s.textBaseline="middle",s.font=12*i+"px Arial",s.textAlign="center",s.fillText(t,e,a))}},{key:"drawPieValue",value:function(t,e){var i=this.ctx;if(this.showValue){var s=this.canvas.width/2,o=this.canvas.height/2,n=Math.ceil(Math.abs(this.radius*Math.cos(e))),r=Math.floor(Math.abs(this.radius*Math.sin(e)));i.textBaseline="middle",this.showValue&&(e<=0?(i.textAlign="left",i.moveTo(s+n,o-r),i.lineTo(s+n+a,o-r-a),i.moveTo(s+n+a,o-r-a),i.lineTo(s+n+3*a,o-r-a),i.stroke(),i.fillText(t,s+n+3.5*a,o-r-a)):0<e&&e<=Math.PI/2?(i.textAlign="left",i.moveTo(s+n,o+r),i.lineTo(s+n+a,o+r+a),i.moveTo(s+n+a,o+r+a),i.lineTo(s+n+3*a,o+r+a),i.stroke(),i.fillText(t,s+n+3.5*a,o+r+a)):e>Math.PI/2&&e<Math.PI?(i.textAlign="right",i.moveTo(s-n,o+r),i.lineTo(s-n-a,o+r+a),i.moveTo(s-n-a,o+r+a),i.lineTo(s-n-3*a,o+r+a),i.stroke(),i.fillText(t,s-n-3.5*a,o+r+a)):(i.textAlign="right",i.moveTo(s-n,o-r),i.lineTo(s-n-a,o-r-a),i.moveTo(s-n-a,o-r-a),i.lineTo(s-n-3*a,o-r-a),i.stroke(),i.fillText(t,s-n-3.5*a,o-r-a)))}}},{key:"drawBackground",value:function(){this.ctx.fillStyle=this.bgColor,this.ctx.fillRect(0,0,this.canvas.width,this.canvas.height),this.drawTitle()}},{key:"drawTitle",value:function(){var t=this.title;if(t.text){var e=this.ctx;e.beginPath(),e.font=t.font,e.textAlign="center",e.fillStyle=t.color,"top"===t.position?(e.textBaseline="top",e.fillText(t.text,this.canvas.width/2,t.top)):(e.textBaseline="bottom",e.fillText(t.text,this.canvas.width/2,this.canvas.height-t.bottom))}}},{key:"drawXAxis",value:function(){var t=this.ctx,e=this.canvas.height-this.bottomPadding+.5;t.beginPath(),t.strokeStyle=this.axisColor,t.moveTo(this.leftPadding,e),t.lineTo(this.canvas.width-this.rightPadding,e),t.stroke(),this.drawXPoint()}},{key:"drawXPoint",value:function(){var t=this.ctx;t.beginPath(),t.font=12*i+"px Microsoft YaHei",t.textAlign=this.xRorate||this.xRotate?"right":"center",t.textBaseline="top",t.fillStyle=this.axisColor;for(var e=0;e<this.labels.length;e++){var o=this.labels[e],n=this.leftPadding+this.xLength*(e+1)+.5,r=this.canvas.height-this.bottomPadding;this.showGrid?(t.strokeStyle=this.gridColor,t.moveTo(n,r),t.lineTo(n,this.topPadding+a)):(t.moveTo(n,r),t.lineTo(n,r-s)),t.stroke(),t.save(),t.translate(n-this.xLength/2,r+s),this.xRorate?t.rotate(-this.xRorate*Math.PI/180):t.rotate(-this.xRotate*Math.PI/180),t.fillText(o,0,0),t.restore()}}},{key:"drawYAxis",value:function(){var t=this.ctx;t.beginPath(),t.strokeStyle=this.axisColor,t.moveTo(this.leftPadding-.5,this.canvas.height-this.bottomPadding+.5),t.lineTo(this.leftPadding-.5,this.topPadding+.5),t.stroke(),this.drawYPoint()}},{key:"drawYPoint",value:function(){var t=this.ctx;t.font=12*i+"px Microsoft YaHei",t.textAlign="right",t.textBaseline="middle",t.beginPath();for(var e=0;e<this.yEqual;e++){var o=this.leftPadding,n=this.canvas.height-this.bottomPadding-this.yLength*(e+1)+.5;this.showGrid?(t.strokeStyle=this.gridColor,t.moveTo(o,n),t.lineTo(this.canvas.width-this.rightPadding-a,n)):(t.strokeStyle=this.axisColor,t.moveTo(o-s,n),t.lineTo(o,n)),t.stroke(),t.save(),t.fillStyle=this.axisColor,t.translate(o-a,n),this.yRorate?t.rotate(-this.yRorate*Math.PI/180):t.rotate(-this.yRotate*Math.PI/180),t.fillText(this.ySpace*(e+1),0,0),t.restore()}}},{key:"drawLegend",value:function(){var t=this.legend;if(t.display){var e=this.ctx,i="pie"===this.type||"ring"===this.type;e.beginPath(),e.font=t.font,e.textAlign="left",e.textBaseline="middle";for(var o=i?this.labels.length:this.datasets.length,n=(this.canvas.width-(this.legend.textWidth+(5*o-2)*a))/2,r=0,l=0;l<o;l++){var h=i?this.datasets[0]:this.datasets[l],c=(i?this.labels[l]:h.label)||"";e.fillStyle=h.colorList&&h.colorList[l]||h.fillColor||this.colorList[l],"top"===t.position?(this.drawLegendIcon(n+5*a*l+r,t.top-s,2*a,a),e.fillStyle=t.color,e.fillText(c,n+(5*l+3)*a+r,t.top)):"bottom"===t.position?(this.drawLegendIcon(n+5*a*l+r,this.canvas.height-t.bottom-s,2*a,a),e.fillStyle=t.color,e.fillText(c,n+(5*l+3)*a+r,this.canvas.height-t.bottom)):(e.fillRect(a,t.top+2*a*l,2*a,a),e.fillStyle=t.color,e.fillText(c,4*a,t.top+2*a*l+.5*a)),r+=Math.ceil(e.measureText(c).width)}}}},{key:"drawLegendIcon",value:function(t,e,o,n){var r=this.ctx;"line"===this.type?(r.beginPath(),r.strokeStyle=r.fillStyle,r.lineWidth=2*i,r.moveTo(t,e+s),r.lineTo(t+2*a,e+s),r.stroke(),r.lineWidth=1*i,r.arc(t+a,e+s,3*i,0,2*Math.PI,!0),r.fill()):r.fillRect(t,e,o,n)}}]),o}()}))},"7ed4":function(t,e,i){"use strict";var a=i("2b0e"),s=new a["default"];e["a"]=s},"96d8":function(t,e,i){},c988:function(t,e,i){"use strict";i("96d8")},e2ad:function(t,e,i){"use strict";i.r(e);var a=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"container"},[i("div",{staticStyle:{"margin-bottom":"15px","text-align":"center"}},[i("el-select",{staticStyle:{"text-align":"center"},attrs:{placeholder:"选择计算资源池"},on:{focus:t.getZoneData,change:t.Zoneboard},model:{value:t.value,callback:function(e){t.value=e},expression:"value"}},[i("el-option",{key:"all",attrs:{label:"所有区域",value:"all"}}),t._l(t.ZonesData,(function(t){return i("el-option",{key:t.id,attrs:{label:t.zone,value:t.id}})}))],2)],1),i("el-row",{attrs:{gutter:20}},[i("el-col",{attrs:{span:24}},[i("el-row",{staticClass:"mgb20",attrs:{gutter:20}},[i("el-col",{attrs:{span:6}},[i("el-card",{attrs:{shadow:"hover","body-style":{padding:"0px"}}},[i("div",{staticClass:"grid-content grid-con-1"},[i("i",{staticClass:"el-icon-cloudy grid-con-icon"}),i("div",{staticClass:"grid-cont-right"},[i("div",{staticClass:"setfontsize"},[t._v("云主机")]),i("div",{staticClass:"grid-num"},[t._v(t._s(t.vmtotal))])])])])],1),i("el-col",{attrs:{span:6}},[i("el-card",{attrs:{shadow:"hover","body-style":{padding:"0px"}}},[i("div",{staticClass:"grid-content grid-con-2"},[i("i",{staticClass:"hdd-network grid-con-icon"},[i("b-icon",{attrs:{icon:"hdd-network"}})],1),i("div",{staticClass:"grid-cont-right"},[i("div",{staticClass:"setfontsize"},[t._v("虚拟网络")]),i("div",{staticClass:"grid-num"},[t._v(t._s(t.networktotal))])])])])],1),i("el-col",{attrs:{span:6}},[i("el-card",{attrs:{shadow:"hover","body-style":{padding:"0px"}}},[i("div",{staticClass:"grid-content grid-con-3"},[i("i",{staticClass:"el-icon-coin grid-con-icon"}),i("div",{staticClass:"grid-cont-right"},[i("div",{staticClass:"setfontsize"},[t._v("数据硬盘")]),i("div",{staticClass:"grid-num"},[t._v(t._s(t.voltotal))])])])])],1),i("el-col",{attrs:{span:6}},[i("el-card",{attrs:{shadow:"hover","body-style":{padding:"0px"}}},[i("div",{staticClass:"grid-content grid-con-4"},[i("i",{staticClass:"el-icon-cpu grid-con-icon"}),i("div",{staticClass:"grid-cont-right"},[i("div",{staticClass:"setfontsize"},[t._v("计算资源")]),i("div",{staticClass:"grid-num"},[t._v(t._s(t.nodetotal))])])])])],1),i("el-col",{attrs:{span:6}},[i("el-card",{attrs:{shadow:"hover","body-style":{padding:"0px"}}},[i("div",{staticClass:"grid-content grid-con-5"},[i("i",{staticClass:"el-icon-files grid-con-icon"}),i("div",{staticClass:"grid-cont-right"},[i("div",{staticClass:"setfontsize"},[t._v("磁盘镜像")]),i("div",{staticClass:"grid-num"},[t._v(t._s(t.imagetotal))])])])])],1)],1)],1)],1),i("el-row",{attrs:{gutter:20}},[i("el-col",{attrs:{span:12}},[i("el-card",{attrs:{shadow:"hover"}},[i("schart",{ref:"bar",staticClass:"schart",attrs:{canvasId:"cpu",options:t.cpustatistics}})],1)],1),i("el-col",{attrs:{span:12}},[i("el-card",{attrs:{shadow:"hover"}},[i("schart",{ref:"bar",staticClass:"schart",attrs:{canvasId:"mem",options:t.memstatistics}})],1)],1)],1),i("el-row",{attrs:{gutter:20}},[i("el-col",{attrs:{span:12}},[i("el-card",{attrs:{shadow:"hover"}},[i("schart",{ref:"bar",staticClass:"schart",attrs:{canvasId:"localdisksize",options:t.localdiskstatistics}})],1)],1),i("el-col",{attrs:{span:12}},[i("el-card",{attrs:{shadow:"hover"}},[i("schart",{ref:"bar",staticClass:"schart",attrs:{canvasId:"rbddisksize",options:t.rbddiskstatistics}})],1)],1)],1)],1)},s=[],o=(i("ac6a"),i("7f7f"),function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",[i("canvas",{attrs:{id:t.canvasId}})])}),n=[];i("8e6e"),i("456d");function r(t,e,i){return e in t?Object.defineProperty(t,e,{value:i,enumerable:!0,configurable:!0,writable:!0}):t[e]=i,t}var l=i("2c8a"),h=i.n(l);function c(t,e){var i=Object.keys(t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(t);e&&(a=a.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),i.push.apply(i,a)}return i}function d(t){for(var e=1;e<arguments.length;e++){var i=null!=arguments[e]?arguments[e]:{};e%2?c(Object(i),!0).forEach((function(e){r(t,e,i[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(i)):c(Object(i)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(i,e))}))}return t}var f={props:{canvasId:{type:String,default:"",required:!0},options:{type:Object,required:!0}},mounted:function(){this.renderChart()},methods:{renderChart:function(){if(this.checkOptions()){var t=d({},this.options);new h.a(this.canvasId,t)}},checkOptions:function(){var t=this.options;return!(!t.datasets||!t.datasets.length)&&!(!t.labels||!t.labels.length)}},watch:{options:{handler:function(t,e){this.renderChart()},deep:!0}}},g=f,u=i("2877"),v=Object(u["a"])(g,o,n,!1,null,null,null),b=v.exports,p=(i("7ed4"),i("0c6d")),y=sessionStorage.getItem("user_info"),m=JSON.parse(y),x={name:"dashboard",data:function(){return{value:"all",ZonesData:[],name:m.username,Datas:"",nodetotal:"",imagetotal:"1",voltotal:"1",vmtotal:"1",networktotal:"1",cpustatistics:{},memstatistics:{},localdiskstatistics:{},rbddiskstatistics:{}}},components:{Schart:b},computed:{role:function(){return"admin"===this.name?"超级管理员":"普通用户"}},mounted:function(){this.Zoneboard("all")},methods:{changeDate:function(){var t=(new Date).getTime();this.data.forEach((function(e,i){var a=new Date(t-864e5*(6-i));e.name="".concat(a.getFullYear(),"/").concat(a.getMonth()+1,"/").concat(a.getDate())}))},getZoneData:function(){var t=this;this.ZonesData=[],Object(p["a"])({url:"/zonelist",method:"get",headers:{authorization:m.token_type+" "+m.access_token}}).then((function(e){t.ZonesData=e.data}))},Zoneboard:function(t){var e=this;this.Datas=[],this.networktotal="",this.nodetotal="",this.imagetotal="",this.voltotal="",this.vmtotal="",this.cpustatistics,this.memstatistics,this.localdiskstatistics,Object(p["b"])({url:"/vnetotal/"+t,method:"get",headers:{authorization:m.token_type+" "+m.access_token}}).then((function(t){e.networktotal=t.data})),Object(p["a"])({url:"/statistic/"+t,method:"get",headers:{authorization:m.token_type+" "+m.access_token}}).then((function(t){e.Datas=t.data,e.nodetotal=t.data.node,e.imagetotal=t.data.img,e.voltotal=t.data.vol,e.vmtotal=t.data.vm,e.cpustatistics={type:"bar",title:{text:"CPU统计信息",bottom:10},legend:{},bgColor:"#fbfbfb",labels:["总计","","已分配","","未分配"],datasets:[{label:"CPU(单位:颗)",fillColor:"rgba(30,144,255)",data:t.data.cpu}]},e.memstatistics={type:"bar",title:{text:"MEM统计信息",bottom:10},bgColor:"#fbfbfb",labels:["总计","","已分配","","未分配"],datasets:[{label:"MEM(单位:GB)",fillColor:"rgba(102,205,170)",data:t.data.mem}]},e.localdiskstatistics={type:"bar",title:{text:"本地存储统计信息",bottom:10},bgColor:"#fbfbfb",labels:["总计","已分配","未分配"],datasets:[{label:"OS存储池(单位:GB)",fillColor:"rgba(25,25,112)",data:t.data.los},{label:"DATA存储池(单位:GB)",fillColor:"rgba(60,179,113)",data:t.data.ldata}]},e.rbddiskstatistics={type:"bar",title:{text:"CEPH存储统计信息",bottom:10},bgColor:"#fbfbfb",labels:["总计","已分配","未分配"],datasets:[{label:"OS存储池(单位:GB)",fillColor:"rgba(25,25,112)",data:t.data.ros},{label:"DATA存储池(单位:GB)",fillColor:"rgba(60,179,113)",data:t.data.rdata}]}}))}}},w=x,P=(i("c988"),Object(u["a"])(w,a,s,!1,null,"b6bef08c",null));e["default"]=P.exports}}]);