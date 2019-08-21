var express = require('express');
var app = express();
var yaml = require('js-yaml');
var fs = require('fs');
var port = process.env.PORT || 8000;

app.get('/get-badge', function(req, res) {
    var tool = req.query.tool;
    console.log(tool);
    try {
        var doc = yaml.safeLoad(fs.readFileSync('badge.yaml', 'utf-8'));
        if (tool in doc) {
            var url = doc[tool];
            res.redirect(url);
        } else {
            res.status(404).send('Tool not found');
        }
    } catch (e) {
        res.status(404).send("Something's wrong on our end.");
        console.log(e);
    }
});

app.listen(port);
console.log('Server started at https://localhost:' + port);