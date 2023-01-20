var express = require('express')
var app = express()
var http = require('http').createServer(app)
var io = require('socket.io')(http)

// You should create a public directory in your project folder and
// place all your static files there and the below app.use() will
// serve all files and sub-directories contained within it.
app.use('', express.static(__dirname));

app.get('/', (request, response) => {
    console.log("Got an HTTP request")
    response.sendFile(__dirname + '/index.html')
})

io.on("connection", (socketclient) => {
    console.log("A new Socket.io client is connected. ID= " + socketclient.id);

    // Event Listeners
    socketclient.on("login", (username, password) => {
        console.log("Debug>Got username=" +
            username +
            ";password=" +
            password);
        if (DataLayer.checklogin(username, password)) {
            // authenticated
            socketclient.authenticated = true;
            socketclient.emit("authenticated");
            // Username and welcome
            socketclient.username = username;
            var welcomemessage = username +
                " has joined the chat!";
            console.log(welcomemessage);
            SendToAuthenticatedClient("welcome", welcomemessage);
            //io.emit("welcome", welcomemessage);
        }
    });

    // Code for the chat Listener
    socketclient.on("chat", (message) => {
        // if not authenticated return nothing
        if (!socketclient.authenticated) {
            console.log("Unauthenticated client sent a chat. Supress!");
            return;
        }
        // else continue with chat
        var chatmessage = socketclient.username + " says " + message;
        console.log('From client: ', chatmessage);
        SendToAuthenticatedClient("chat", chatmessage);

    })
});

const port = process.env.PORT || 8080
var server = http.listen(port, () => {
        console.log(`App listening on port ${server.address().port}`)
    })
    // added in the data layer
var DataLayer = {
    info: 'Data Layer Implementation for Messenger',
    checklogin(username, password) {
        // for testing only
        console.log("checklogin: " +
            username +
            "/" +
            password);
        console.log("Just for testing -- return true");
        return true;
    }
}

// function to authenticate user
// ... data unpacks variable list and expand
async function SendToAuthenticatedClient(type, ...data) {
    var sockets = await io.fetchSockets();
    for (var socketId in sockets) {
        var socketclient = sockets[socketId];
        if (socketclient.authenticated) {
            socketclient.emit(type, ...data);
            var logmsg = "Sending [" +
                type +
                "] to " +
                socketclient.username +
                " with ID=" +
                socketId;
            console.log(logmsg);
        }
    }
}