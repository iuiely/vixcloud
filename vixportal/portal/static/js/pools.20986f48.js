(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["pools"],{"0c6d":function(e,t,n){"use strict";n.d(t,"c",(function(){return s})),n.d(t,"a",(function(){return r})),n.d(t,"b",(function(){return i}));var o=n("bc3a"),a=n.n(o);function s(e){var t=a.a.create({baseURL:window.url.ssourl,timeout:5e3});return t(e)}function r(e){var t=a.a.create({baseURL:window.url.coreurl,timeout:5e3});return t(e)}function i(e){var t=a.a.create({baseURL:window.url.vneturl,timeout:5e3});return t(e)}},"1da1":function(e,t,n){"use strict";function o(e,t,n,o,a,s,r){try{var i=e[s](r),c=i.value}catch(l){return void n(l)}i.done?t(c):Promise.resolve(c).then(o,a)}function a(e){return function(){var t=this,n=arguments;return new Promise((function(a,s){var r=e.apply(t,n);function i(e){o(r,a,s,i,c,"next",e)}function c(e){o(r,a,s,i,c,"throw",e)}i(void 0)}))}}n.d(t,"a",(function(){return a}))},"42c4":function(e,t,n){"use strict";n.r(t);var o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"container"},[n("div",{staticStyle:{"margin-bottom":"10px"}},[n("el-button",{attrs:{type:"primary",icon:"el-icon-plus"},on:{click:function(t){e.AddZoneForm=!0}}},[e._v("创建区域")]),n("el-dialog",{attrs:{title:"增加资源区域",visible:e.AddZoneForm,width:"30%","close-on-click-modal":!1,center:""},on:{close:e.AddZoneDialogClose,"update:visible":function(t){e.AddZoneForm=t}}},[n("el-form",{ref:"AddZoneRef",attrs:{model:e.Add_Zone,rules:e.AddZoneRules,"label-width":"120px","label-position":"left"}},[n("el-form-item",{attrs:{label:"区域名称",prop:"zone"}},[n("el-input",{staticStyle:{width:"240px"},attrs:{placeholder:"区域名称","auto-complete":"off"},model:{value:e.Add_Zone.zone,callback:function(t){e.$set(e.Add_Zone,"zone",t)},expression:"Add_Zone.zone"}})],1),n("el-form-item",{attrs:{label:"区域描述",prop:"desc"}},[n("el-input",{staticStyle:{width:"240px"},attrs:{placeholder:"区域描述","auto-complete":"off"},model:{value:e.Add_Zone.desc,callback:function(t){e.$set(e.Add_Zone,"desc",t)},expression:"Add_Zone.desc"}})],1)],1),n("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{attrs:{type:"primary"},on:{click:e.CreateZone}},[e._v("确 定")]),n("el-button",{on:{click:function(t){e.AddZoneForm=!1}}},[e._v("取 消")])],1)],1)],1),n("el-table",{ref:"multipleTable",staticClass:"table",attrs:{data:e.ZonesData,"header-cell-class-name":"table-header"}},[e.show?n("el-table-column",{attrs:{prop:"id",label:"ID",width:"100",align:"center"}}):e._e(),n("el-table-column",{attrs:{prop:"zone",label:"区域名称",align:"center"}}),n("el-table-column",{attrs:{prop:"nodes",label:"宿主节点",align:"center",width:"100px"}}),n("el-table-column",{attrs:{prop:"mode",label:"存储类型",align:"center"}}),n("el-table-column",{attrs:{prop:"state",label:"使用状态",align:"center",width:"150px"},scopedSlots:e._u([{key:"default",fn:function(t){return[1===t.row.state?n("span",{staticStyle:{color:"#37B328"}},[e._v("启用")]):n("span",{staticStyle:{color:"red"}},[e._v("禁用")])]}}])}),n("el-table-column",{attrs:{label:"操作",align:"center",width:"400px",fixed:"right"},scopedSlots:e._u([{key:"default",fn:function(t){return[1===t.row.state?n("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"禁用",placement:"top-start"}},[n("el-button",{staticStyle:{color:"red"},attrs:{circle:""},on:{click:function(n){return e.Disable(t.row)}}},[n("i",{staticClass:"el-icon-lock"})])],1):n("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"启用",placement:"top-start"}},[n("el-button",{staticStyle:{color:"#37B328"},attrs:{circle:""},on:{click:function(n){return e.Enable(t.row)}}},[n("b-icon",{attrs:{icon:"unlock"}})],1)],1),n("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"宿主节点列表",placement:"top-start"}},[n("el-button",{attrs:{circle:""},on:{click:function(n){return e.NodeList(t.row.zone)}}},[n("b-icon",{attrs:{icon:"laptop"}})],1)],1),n("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"网络设备列表",placement:"top-start"}},[n("el-button",{attrs:{circle:""},on:{click:function(n){return e.NetDevList(t.row.zone)}}},[n("b-icon",{attrs:{icon:"shuffle"}})],1)],1),n("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"设置存储池",placement:"top-start"}},[n("el-button",{attrs:{icon:"el-icon-coin",circle:""},on:{click:function(n){return e.ListPool(t.row.id,t.row.zone)}}})],1),n("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"删除资源区域",placement:"top-start"}},[n("el-button",{attrs:{type:"danger",icon:"el-icon-delete",circle:""},on:{click:function(n){return e.ZoneDel(t.row)}}})],1)]}}])})],1),n("div",{staticClass:"block",staticStyle:{height:"70px"}},[n("el-pagination",{attrs:{"page-sizes":[10,20],"page-size":e.page.pageSize,layout:"total, sizes, prev, pager, next",total:e.page.totalRecords},on:{"size-change":e.sizeChange,"current-change":e.currentChange}})],1)],1)},a=[],s=(n("96cf"),n("1da1")),r=n("0c6d"),i=sessionStorage.getItem("user_info"),c=JSON.parse(i),l={data:function(){return{show:!1,ZonesData:[],Pools:[],AddZoneForm:!1,Add_Zone:{zone:"",desc:""},AddZoneRules:{zone:[{required:!0,message:"请输入区域资源池名称",trigger:"blur"}],desc:[{required:!0,message:"请输入区域资源池描述",trigger:"blur"}]},page:{pageSize:10,totalRecords:0,totalPages:0,pageNum:0,pagelimit:0}}},mounted:function(){this.getZones()},methods:{AddZoneDialogClose:function(){void 0!==this.$refs.AddZoneRef&&this.$refs.AddZoneRef.resetFields()},getZones:function(){var e=this;this.ZonesData=[];var t=this.page,n=t.pageNum,o=t.pageSize,a=t.pagelimit;a=n*o,Object(r["a"])({url:"/zones?skip="+a+"&limit="+o,method:"get",headers:{authorization:c.token_type+" "+c.access_token}}).then((function(t){e.page.totalRecords=t.data.count,e.ZonesData=t.data.data}))},sizeChange:function(e){this.page.pageSize=e,this.getPools()},currentChange:function(e){this.page.pageNum=e-1,this.getPools()},CreateZone:function(){var e=this;this.$refs.AddZoneRef.validate(function(){var t=Object(s["a"])(regeneratorRuntime.mark((function t(n){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(n){t.next=3;break}return e.$message.error("请输入资源资源名称和资源资源描述"),t.abrupt("return",!1);case 3:Object(r["a"])({url:"/zone",method:"post",data:e.Add_Zone,headers:{authorization:c.token_type+" "+c.access_token}}).then((function(t){200===t.data.code?(e.$message.success("增加资源资源"+t.data.data[0].zone+"成功"),e.AddZoneForm=!1,e.$refs.AddZoneRef.resetFields(),e.getZones()):e.$message.error("增加资源资源失败,错误代码 "+t.data.message)}));case 4:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}())},Enable:function(e){var t=this;if(1!==e.state){var n={id:e.id,state:1};this.$confirm("确认启用资源区域"+e.zone+", 是否继续?","提示",{type:"warning"}).then((function(){Object(r["a"])({url:"/setzonestate",method:"post",data:n,headers:{authorization:c.token_type+" "+c.access_token}}).then((function(e){200===e.data.code?(t.$message.success("启用资源区域"+e.data.data[0].zone+"成功"),t.getZones()):t.$message.error("启用资源区域失败,错误  "+e.data.message)}))})).catch((function(){}))}},Disable:function(e){var t=this;if(1===e.state){var n={id:e.id,state:2};this.$confirm("确认禁用区域"+e.zone+", 是否继续?","提示",{type:"warning"}).then((function(){Object(r["a"])({url:"/setzonestate",method:"post",data:n,headers:{authorization:c.token_type+" "+c.access_token}}).then((function(e){200===e.data.code?(t.$message.success("禁用资源区域"+e.data.data[0].zone+"成功"),t.getZones()):t.$message.error("禁用资源区域失败,错误  "+e.data.message)}))})).catch((function(){}))}},ListPool:function(e,t){this.$router.push({path:"/pools",query:{zone:t,id:e}})},NodeList:function(e){var t=e;this.$router.push({path:"/computes",query:{zone:t}})},NetDevList:function(e){var t=e;this.$router.push({path:"/netdevices",query:{zone:t}})},ZoneDel:function(e){var t=this;this.$confirm("此操作将永久删除资源区域 "+e.zone+", 是否继续?","提示",{type:"warning"}).then((function(){Object(r["a"])({url:"/deletezone/"+e.id,method:"post",headers:{authorization:c.token_type+" "+c.access_token}}).then((function(e){200===e.data.code?(t.$message.success("删除资源区域"+e.data.data[0].zone+"成功"),t.getZones()):t.$message.error("删除资源区域失败,原因 "+e.data.message)}))})).catch((function(){}))}}},u=l,d=(n("d85a"),n("2877")),p=Object(d["a"])(u,o,a,!1,null,"51d970be",null);t["default"]=p.exports},b495:function(e,t,n){},d85a:function(e,t,n){"use strict";n("b495")}}]);