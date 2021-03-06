$(document).ready(() => {
  $("[user]").click(function() {
      location.href = "chat/" + $(this).attr("user_id");
  });

  $("[group]").click(function() {
      location.href = "chat/group/" + $(this).attr("group_id");
  });

  $('#myTabs a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
  })
});



function initializeSocket(){
    socket = io.connect('https://' + location.host + '/chat');

    socket.on('connect', function() {
        socket.emit('joined');
    });

    socket.on('newUser', function(data) {
      const elementId = "user_" + data.id;
      let newUser = `
        <a user id="${elementId}" user_id="${data.id}" class="item list-group-item border_item" title="${data.platformName}">
            <span unread_count="0" class="badge badge-primary badge-pill"></span>
            <h4 name class="list-group-item-heading">${data.name}</h4>
            <p last_received class="list-group-item-text"></p>
            <img src='' class="list-image">
            <audio id="${data.id}_audio" style="display:none;" controls>
                <source audio_source src="">
            </audio>
        </a>
      `
      $('#contactList').append(newUser)
      $(`#${elementId}`).click(function() {
        location.href = "chat/" + $(this).attr("user_id");
      });

    });

    socket.on('uiTextMessage', function(data) {
          var elementId;
          if(data.group_id){
            elementId = "group_" + data.group_id;
          }
          else{
            elementId = "user_" + data.user_id;
          }

          //update text
          $("#" + elementId + " [last_received]").text(data.msg);

          //update unread count
          updateUnreadCount(elementId);
          updateFrom(elementId, data.group_id, data.from);

          //hide audio and image
          $("#" + elementId + " [image]").attr("src", "");
          $("#" + elementId + " img").hide();
          $("#" + elementId + " audio").hide();
          console.log(data);
    });

    socket.on('uiAudioMessage', function(data) {
          var elementId;
          if(data.group_id){
            elementId = "group_" + data.group_id;
          }
          else{
            elementId = "user_" + data.user_id;
          }

          //update audio
          $("#" + elementId + " audio").show();
          $("#" + elementId + " [audio_source]").attr("src", data.audioPath);
          var audio = document.getElementById(elementId + '_audio')
          audio.load();

          updateUnreadCount(elementId)
          updateFrom(elementId, data.group_id, data.from);


          //hide image and text
          $("#" + elementId + " [last_received]").text("");
          $("#" + elementId + " [image]").attr("src", "");
          $("#" + elementId + " img").hide();
          console.log(data);
    });

    socket.on('uiImageMessage', data => {
          var elementId;
          if(data.group_id){
            elementId = "group_" + data.group_id;
          }
          else{
            elementId = "user_" + data.user_id;
          }

          //update image
          $("#" + elementId + " img").attr("src", data.imagePath);
          $("#" + elementId + " img").show();

          updateUnreadCount(elementId);
          updateFrom(elementId, data.group_id, data.from);

          //hide text and audio
          $("#" + elementId + " audio").hide();
          $("#" + elementId + " [last_received]").text("");
          console.log(data);
    });
}

function updateUnreadCount(elementId){
    var unread = $("#" + elementId + " [unread_count]").attr("unread_count");
    $("#" + elementId + " [unread_count]").attr("unread_count", parseInt(unread) + 1);
    $("#" + elementId + " [unread_count]").text(parseInt(unread) + 1);
}

function updateFrom(elementId, groupId, from){
    if(groupId){
        $("#" + elementId + " [last_received_from]").text(from + ": ");
    }
}


function getFromText(data){
    var fromText = data.from;
    if(data.group != null){
        fromText = data.from + ' del grupo *' + data.group + '*';
    }
    return fromText;
}

function getQueryVariable(variable) {
    let query = window.location.search.substring(1);
    let vars = query.split('&');
    for (let i = 0; i < vars.length; i++) {
        let pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    console.log('Query variable %s not found', variable);
}
