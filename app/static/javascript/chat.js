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

    socket.on('uiImageMessage', data => {
        var from = data.loggedUserName;
        var imageElement = new Image();
        imageElement.src = data.imagePath;
        imageElement.style = "max-height: 240px; max-width: 240px;"
        imageElement.onload = function() { scrollDownChat(); }
        appendNewMessage(imageElement, data.from);
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

function sendAudio(byteArray){
    socket.emit('audioMessage', byteArray, recipients, $("#conversationId").val(), $("#loggedUserName").val());
}


function scrollDownChat(){
    $("#chat").scrollTop($("#chat [messages]").height());
}


const recordAudio = () => {
  return new Promise(resolve => {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);
        });

        const start = () => {
          mediaRecorder.start();
        };

        const stop = () => {
          return new Promise(resolve => {
            mediaRecorder.addEventListener("stop", () => {
              const audioBlob = new Blob(audioChunks);
              const audioUrl = URL.createObjectURL(audioBlob);
              const audio = new Audio(audioUrl);
              const play = () => {
                audio.play();
              };

              resolve({ audioBlob, audioUrl, play });
            });

            mediaRecorder.stop();
          });
        };

        resolve({ start, stop });
      });
  });
};





function recordAudio(){
const sleep = time => new Promise(resolve => setTimeout(resolve, time));

    (async () => {
          const recorder = await recordAudio();
          recorder.start();
          await sleep(3000);
          const audio = await recorder.stop();
          audio.play();
    })();
}
