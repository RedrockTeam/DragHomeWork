var express = require('express');
var router = express.Router();
var fs = require('fs');
var path = require('path');
var cache = [];


/* GET home page. */
router.get('/', function(req, res) {
    res.render('index', { title: '作业地址提交' });
	console.log(__dirname);
});

router.post('/list', function(req, res){
	var username = req.body.username;
	var github = req.body.github;

	cache.push(username + "??" + github);

	fs.writeFileSync(path.join(__dirname, '../data/data.py'), "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nresponsitories="  + JSON.stringify(cache) , {encoding: "utf-8", flag : "w"});

	res.end('提交成功');
});



module.exports = router;
