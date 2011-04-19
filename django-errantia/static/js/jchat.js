var chat_room_id = undefined;
var chat_name = undefined;
var last_received = 0;

var chat_conn;

/**
 * Initialize chat:
 * - Set the room id
 * - Generate the html elements (chat box, forms & inputs, etc)
 * - Sync with server
 * @param chat_room_id the id of the chatroom
 * @param html_el_id the id of the html element where the chat html should be placed
 * @return
 */
function init_chat(chat_id, html_el_id)
{
    chat_room_id = chat_id;

    conf.ws.subscribe('errantia-chat:' + chat_room_id);
    conf.ws.onSubscribed = function(ch_name, subscription)
    {
        if (ch_name == 'errantia-chat:' + chat_room_id)
        {
	    chat_conn = subscription;
	    chat_conn.onPublish = got_msg;

            for (var a in chat_conn.history) {
                if (chat_conn.history[a][0] != "PUBLISH")
                    continue;
                got_msg(chat_conn.history[a][1]);
            }
        }
        $("#chat").delay(1000).removeClass('hide');
        console.log("Kopla til " + ch_name);
    }
    layout_and_bind(html_el_id);
    sync_messages();
}

var img_dir = "/static/img/";

/**
 * Asks the server which was the last message sent to the room, and stores it's id.
 * This is used so that when joining the user does not request the full list of
 * messages, just the ones sent after he logged in. 
 * @return
 */
function sync_messages() {
    $.ajax({
        type: 'POST',
        data: {id:window.chat_room_id},
        url:'/chat/sync/',
        dataType: 'json',
        success: function (json) {
            last_received = json.last_message_id - 10;
            if (last_received < 0)
                last_received = 0;
        }        
    });
}

/**
 * Generate the Chat box's HTML and bind the ajax events
 * @param target_div_id the id of the html element where the chat will be placed 
 */
function layout_and_bind(html_el_id) {
        // layout stuff
        var html = '<div id="chat-messages-container">'+
        '<div id="chat-messages"> </div>'+
        '<div id="chat-last"> </div>'+
        '</div>'+
        '<form id="chat-form">'+
        '<input name="message" type="text" class="message" placeholder="Skriv tekst her" />'+
        '<input type="submit" value="Send"/>'+
        '</form>';
        
        $("#"+html_el_id).append(html);
        
        // event stuff
        $("#chat-form").submit( function () {
            if (chat_name == null || chat_name == undefined) {
                jPrompt("Enter a nickname", "", "Chat", function(n){
                    if (!n) return;
                    window.chat_name = n;
                    chat_join();
                    send_msg();
                });
            }
            else
                send_msg();

            return false;
    });

};

function send_msg() {
            var $inputs = $("#chat-form").children('input');
            var values = {};
            
            $inputs.each(function(i,el) { 
                values[el.name] = $(el).val();
            });
            values['chat_room_id'] = window.chat_room_id;
            values['name'] = window.chat_name;

            $.ajax({
                data: values,
                dataType: 'json',
                type: 'post',
                url: '/chat/send/'
            });
            $('#chat-form .message').val('');
}

/**
 * Gets the list of messages from the server and appends the messages to the chatbox
 */
function got_msg(frame)
{
    var m = frame.payload;
    var scroll = false;

    // first check if we are at the bottom of the div, if we are, we shall scroll once the content is added
    var $containter = $("#chat-messages-container");
    if ($containter.scrollTop() == $containter.attr("scrollHeight") - $containter.height())
        scroll = true;

    // add message
    if (m.type == 's')
        $('#chat-messages').append('<div class="system">' + replace_emoticons(m.message) + '</div>');
    else if (m.type == 'm')
    {
        if (m.message.substr(0, 1) === '/') {
            /* Command */
            if (m.message.substr(0, 7) == '/banner') {
                text = m.message.substr(8, m.message.length);
                if (text) {
                    $("#info").html(text);
                    $("#info").css("display", "block");
                }
                else
                    $("#info").css("display", "none");
            }
            else if (m.message.substr(0, 6) == '/topic') {
                text = m.message.substr(7, m.message.length);
                if (text) {
                    $("h1.chat-topic").html(text);
                    $("h1.chat-topic").removeClass("hide").show();
                }
                else
                    $("h1.chat-topic").toggle();
            }
        }
        else
        {
            datetime = m.timestamp.replace(" ", "T").substr(0, 16) + "+02:00";
            time = m.timestamp.substr(11,5);
            $('#chat-messages').append('<div class="message"><time datetime="'+datetime+'">'+time+'</time> <cite class="author">'+m.author+'</cite>'+replace_emoticons(m.message) + '</div>');
        }
    }
/*    else if (m.type == 'j')
        $('#chat-messages').append('<div class="join">'+m.author+' has joined</div>');
    else if (m.type == 'l')
        $('#chat-messages').append('<div class="leave">'+m.author+' has left</div>');*/

    last_received = m.id;
    
    // scroll to bottom
    if (scroll)
        $("#chat-messages-container").animate({ scrollTop: $("#chat-messages-container").attr("scrollHeight") }, 500);
}

/**
 * Tells the chat app that we are joining
 */
function chat_join() {
    $.ajax({
        async: false,
        type: 'POST',
        data: {chat_room_id:window.chat_room_id, name:window.chat_name},
        url:'/chat/join/',
    });

    $(window).unload(function(){chat_leave()});
}

/**
 * Tells the chat app that we are leaving
 */
function chat_leave() {
    $.ajax({
        async: false,
        type: 'POST',
        data: {chat_room_id:window.chat_room_id, name:window.chat_name},
        url:'/chat/leave/',
    });
}

// attach join and leave events
//$(window).load(function(){chat_join()});
//$(window).unload(function(){chat_leave()});

// emoticons
var emoticons = {                 
    '>:D' : 'emoticon_evilgrin.png',
    ':D' : 'emoticon_grin.png',
    '=D' : 'emoticon_happy.png',
    ':\\)' : 'emoticon_smile.png',
    ':O' : 'emoticon_surprised.png',
    ':P' : 'emoticon_tongue.png',
    ':\\(' : 'emoticon_unhappy.png',
    ':3' : 'emoticon_waii.png',
    ';\\)' : 'emoticon_wink.png',
    '\\(ball\\)' : 'sport_soccer.png'
}

/**
 * Regular expression maddness!!!
 * Replace the above strings for their img counterpart
 */
function replace_emoticons(text) {
    $.each(emoticons, function(char, img) {
        re = new RegExp(char,'g');
        // replace the following at will
        text = text.replace(re, '<img src="'+img_dir+img+'" />');
    });
    return text;
}
