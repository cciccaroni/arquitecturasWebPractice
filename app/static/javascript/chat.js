function initializeSocket(){
    socket = io.connect('http://' + location.host + '/chat');

    socket.on('connect', function() {
        socket.emit('joined');
    });

    socket.on('uiTextMessage', function(data) {
        appendNewMessage($("<p text class='list-group-item-text'>" + data.msg + "</p>"), data.from);
    });

    socket.on('add-wavefile', function(data) {
        appendNewMessage($("<audio controls><source src='" + data.url + "'></audio>"), data.from);
    });

    socket.on('image', data => {
        var arrayBuffer = data.image;
        var bytes = new Uint8Array(arrayBuffer);
        var from = data.loggedUserName;
        appendNewMessage($("<img src='data:image/png;base64," + encode(bytes) + "' />"), data.from);
    });
}

function appendNewMessage(element, from){
    var newMessageElement = $("<a user class='list-group-item'>")
    newMessageElement.append($("<h4 name class='list-group-item-heading'>" + from + "</h4>"))
    newMessageElement.append(element)
    var isLoggedUserMessage = from == $("#loggedUserName").val();

    if (isLoggedUserMessage)
    {
        newMessageElement.addClass("loggedUserMessage");
    }

    $("#chat [messages]").append(newMessageElement);
    scrollDownChat();
}

function setUIEventHandlers(){
    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('textMessage', text, recipients, $("#conversationId").val(), $("#loggedUserName").val());
        }
    });

    $("#file").on("change", function (e) {
        var file = $(this)[0].files[0];
        var fileReader = new FileReader();
        if (file) {
            fileReader.readAsArrayBuffer(file);
            fileReader.onload = function () {
                var imageData = fileReader.result;
                socket.emit('imageMessage', imageData, recipients, $("#conversationId").val(), $("#loggedUserName").val());
            };
        }
    });
}
function encode (input) {
    var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var output = "";
    var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
    var i = 0;

    while (i < input.length) {
        chr1 = input[i++];
        chr2 = i < input.length ? input[i++] : Number.NaN; // Not sure if the index
        chr3 = i < input.length ? input[i++] : Number.NaN; // checks are needed here

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
            enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
            enc4 = 64;
        }
        output += keyStr.charAt(enc1) + keyStr.charAt(enc2) +
                  keyStr.charAt(enc3) + keyStr.charAt(enc4);
    }
    return output;
}

function scrollDownChat(){
    $("#chat").scrollTop($("#chat [messages]").height());
}


