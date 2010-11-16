var slides;
var slide_now = undefined;

var conf = {}

var conn;
var slide_sub;
var conf_sub;

function init_slides(conf_slug) {
    conf.slug = conf_slug;
    get_slides();

    conn = hookbox.connect('http://velmont.hosted.hookbox.org/');
    conn.subscribe('errantia-slides');
    conn.subscribe('errantia-chat');
    conn.subscribe('errantia-talk');

    conn.onSubscribed = function(ch_name, subscription) {
        if (ch_name == "errantia-slides")
        {
            slide_conn = subscription;
            slide_conn.onPublish = function(frame) {
                slides[slides.length] = $.parseJSON(frame.payload);
                update_slide_info();
            }
        }
        else if (ch_name == "errantia-talk")
        {
            conf_sub = subscription;
            conf_sub.onPublish = function(frame) {
                conf = $.parseJSON(frame.payload);
                update_talk_info();
            }
        }

        console.log("Kopla til " + ch_name);
    }

    var html = '<div id="slide-info" style="color: #fff; background: rgba(0,0,0,0.5); padding: 2px 5px; position: absolute; bottom: 0; left: 0;"></div>';
    $("#slides").append(html);
    $("#slides").attr("style", "");

    $("#slide-info").append($("<span class='btn back'>&larr; </span>").click(prev_slide));
    $("#slide-info").append('<span id="slide-status" style="">-</span></div>');
    $("#slide-info").append($("<span class='btn fwd'> &rarr;</span>").click(next_slide));

    $("#slide-active").click(next_slide);
}

function get_slides() {
    $.ajax({
        type: 'GET',
        url: '/api/slide/' + conf.slug + '/',
        dataType: 'json',
        success: function (json) {
            slides = json;
            if(slides[0] && slide_now == undefined)
                slide_now=0;
            update_slide_info();
        }
    });
}

function update_slide_info() {
    if (slide_now == undefined)
        return;

    $("#slide-status")[0].innerHTML = (slide_now + 1) + "/" + slides.length;

    if (slide_now == slides.length - 1)
        $("#slides .fwd").addClass("disabled");
    else
        $("#slides .fwd").removeClass("disabled");

    if (slide_now == 0)
        $("#slides .back").addClass("disabled");
    else
        $("#slides .back").removeClass("disabled");

    slides[slides.length-1];

    $("#slide-active")[0].src = "/static/" + slides[slide_now].slide;
}

function update_talk_info() {
    $(".talk-title").each(function (){
        this.innerHTML = conf.talk.title;
    });
}

function next_slide() {
    if (slide_now == undefined)
        return;

    if (slide_now >= slides.length - 1)
        return;

    slide_now += 1;
    update_slide_info();
}

function prev_slide() {
    if (slide_now == undefined)
        return;

    if (slide_now == 0)
        return;

    slide_now -= 1;
    update_slide_info();
}

