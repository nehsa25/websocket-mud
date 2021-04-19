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
    case 'event':
      // check if there's an event
      if (data.event != "") {
        msg += "<br><br><span style=\"color: yellow;\">" + data.event + "</span><br>";
      }
      break;
      case 'info':
        // check if there's an event
        if (data.info != "") {
          msg += "<br><br><span style=\"color: darksalmon;\">" + data.info + "</span><br>";
        }
        break;
      case 'attack':
        // check if there's an event
        if (data.attack != "") {
          msg += "<br><span style=\"color: red;\">" + data.attack + "</span>";
        }
        break;
      case 'health':
        // check if there's an event
        if (data.health != "") {
          msg += "<br><span style=\"color: white;\">" + data.health + "</span>";
        }
        break;
    case 'room':
      // check if there's a room name
      if (data.name != "") {
        msg += "<br><span style=\"color: yellow;\">" + data.name + "</span>";
      }

      // check if there's a room descrption
      if (data.description != "") {
        msg += "<br><span style=\"color: antiquewhite;\">" + data.description + "</span>";
      }
      // check for monsters
      if (data.monsters != "") {
        msg += "<br><span style=\"color: antiquewhite;\">Monsters: </span><span style=\"color: red;\">" + data.monsters + "</span>";
      }

      // check for items
      if (data.items != "") {
        msg += "<br><span style=\"color: antiquewhite;\">You see </span><span style=\"color: green;\">" + data.items + "</span>";
      }

      // check for available exits
      if (data.exits != "") {
        msg += "<br><span style=\"color: antiquewhite;\">Available exits: </span><span style=\"color: green;\">" + data.exits + "</span>";
      }
      break
    case 'get_clients':
      console.log("Inside get_clients switch");
      $("#users_connected").text(data.value + " users connected.");
    default:
      console.error("unsupported event", JSON.stringify(event));
    }

    return msg;
}

function trimHtml() {
  msg = $("#messages").html() + "";
  console.log("HTML length: " + msg.length);
  // if (msg.length > 2000) {
  //   lines = msg.split('<br>');
  //   new_msg = "";
  //   for (var x = lines.length; x >= lines.length; x--) {
  //     new_msg
  //   }
  //   start_len = msg_len - 2000;
  //   msg = msg.substring(start_len, msg_len);
  //   console.log("Trimed html from " + msg.length.toString() + " to " + start_len.toString());
  // }
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
