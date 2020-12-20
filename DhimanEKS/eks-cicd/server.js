var express = require('express')
var app = express()

app.get('/', function(req,res) {
    res.send('Hello from the Web app!');
});

app.listen(8080, ()=> console.log('listening on 8080'))
