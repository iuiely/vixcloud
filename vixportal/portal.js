// portal.js
const express = require('express');
//创建web服务器
const portal = express();
//导入gzip包
const compression = require("compression")
//文件操作
const fs = require('fs');
const path = require('path');
const chalk = require('chalk')

//启用gzip中间件,在托管之前
portal.use(compression())
//托管静态资源
portal.use(express.static(path.resolve(__dirname, './portal')))

portal.get('/', function(req, res) {
    const html = fs.readFileSync(path.resolve(__dirname, './portal/index.html'), 'utf-8')
    res.send(html)
})

portal.get('/home', function(req, res) {
    const html = fs.readFileSync(path.resolve(__dirname, './portal/index.html'), 'utf-8')
    res.send(html)
})
//启动web服务器
portal.listen(4210, res => {
    console.log(chalk.yellow('Start Service On 4210'));
});

