
var express = require('express')
var app = express()

app.get('/', function(req,res) {
    res.send('Service name is ' + process.env.SERVICE_NAME);
});

app.listen(8080, ()=> console.log('listening on 8080'))