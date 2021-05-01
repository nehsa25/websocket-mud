var socket;

$(document).ready(function () {
  var host = "208.52.52.157";
  var port = 81;
  var full_address = "ws://" + host + ":" + port + "/"

  // Focus on the command bar
  $("#command").focus();

  var input = document.getElementById("command");
  input.addEventListener("keyup", function(event) {
      if (event.keyCode === 13) {
          event.preventDefault();
          document.getElementById("submit_btn").click();
      }
  });

  console.log("Setting up websocket connection at " + full_address)
  // configure_websocket(host, port);
  socket = new WebSocket(full_address);

  //Connection opened
  socket.addEventListener('open', function(event) {
    console.log("Connected to server");
  });

  //Listen to messages
  socket.addEventListener('message', function(event) {    
    var data = JSON.parse(event.data);

    // get the previous html and trim as necessary
    msg = trimHtml();

    // process the command
    msg = processCommand(data, msg)

    // unescape
    unescape(msg);
      
    // set the new HTML
    //$("#messages").html(msg);
    document.getElementById('messages').innerHTML = msg;
    
    // place us at bottom of div
    scrollSmoothToBottom("messages");
  });
});

function processCommand(data, msg) {
  switch (data.type) {        
    case 'request_hostname':
      console.log("Inside request_hostname switch");
      var resp = '{"type": "hostname_answer", "host": "' + "webclient_" + new Date().getTime() + '"}'
      console.log("Server is requesting our name, sending back: " + resp);      
      socket.send(resp);
      break;
    case 'event': // check if there's an event # breeze, silence, rain
      if (data.message != "") {
        msg += "<br><span style=\"color: yellow;\">" + data.message + "</span>";
      }
      break;
    case 'info': // check if there's an info event      
      if (data.message != "") {
        msg += "<br><span style=\"color: darksalmon;\">" + data.message + "</span>";
      }
      break;
    case 'you_attack': // check if there's an info event      
      if (data.message != "") {
        msg += "<br><span style=\"color: #98FB98;\">" + data.message + "</span>";
      }
      break;
    case 'error': // check if there's an info event      
      if (data.message != "") {
        msg += "<br><span style=\"color: red;\">" + data.message + "</span>";
      }
      break;
    case 'attack': // check if there's an attack event
      if (data.message != "") {
        msg += "<br><span style=\"color: #7851a9;\">" + data.message + "</span>";
      }
      break;
    case 'health': // check if there's an health event
      if (data.message != "") {
        $('#health').html(data.message);
      }
      break;
    case 'room': // check if there's a room name
      if (data.name != "") {
        msg += "<br><span style=\"color: green; text-weight: bold;\">" + data.name + "</span>";
      }

      // check if there's a room descrption
      if (data.description != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">" + data.description + "</span>";
      }
      // check for monsters
      if (data.monsters != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">Monsters: </span><span style=\"color: red;\">" + data.monsters + "</span>";
      }

      // check for items
      if (data.items != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">You see </span><span style=\"color: green;\">" + data.items + "</span>";
      }

      // check for available exits
      if (data.exits != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">Available exits: </span><span style=\"color: green;\">" + data.exits + "</span><br class=\"break\">";
      }
      break;
    case 'get_clients':
      console.log("Inside get_clients switch");
      $("#users_connected").text(data.value + " users connected.");
      break;
    default:
      console.error("unsupported event", JSON.stringify(event));
      break;
    }

    return msg;
}

function trimHtml() {
  trim_length = 3000;
  break_msg = '<br class="break">';
  msg = $("#messages").html() + "";
  msg = msg.trim();
  console.log("HTML length: " + msg.length);
  
  if (msg.length > trim_length) {
    trim_point = 0;
    spans = msg.split(break_msg);
    for (var x = 0; x <= spans.length; x++) {
      // if we get below trim_length then we just need to go 1 back
      if (msg.lastIndexOf(spans[x]) > trim_length) {
        trim_point = msg.lastIndexOf(spans[x-1]);
        break;
      }
    }

    // let's do some trimming
    if (trim_point > 0) {
      msg = msg.substring(trim_point, msg.length);
    }
  }
  return msg;
}

function scrollSmoothToBottom(id) {
  var div = document.getElementById(id);
  $('#' + id).animate({
     scrollTop: div.scrollHeight - div.clientHeight
  }, 50);
}

function resetfocus() {
  $("#command").focus();
}

function isOpen(ws) { return ws.readyState === ws.OPEN }

function send_command() {
  var cmd = $('#command').val();
  
  if (isOpen(socket)) {
    var full_cmd = {
      "type": "cmd", 
      "cmd": cmd
    };
    console.log("Sending: " + cmd);
    console.log(full_cmd);
    socket.send(JSON.stringify(full_cmd));
    
    // clear command
    $("#command").val("");
  } else {
    console.log("Websocket is closed..");
  }  
}
