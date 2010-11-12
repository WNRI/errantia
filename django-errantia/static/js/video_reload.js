var interval_id = -1;
var last_time = -1;
var v;
var check_interval = 1000;

function setint() {
  interval_id = setInterval(reload, check_interval);
}

function reload() {
  if (v.paused && v.currentSrc != "")
  {
    // Hinder race
    last_time = 0;
    return;
  }

  if (last_time > 0 && v.currentTime == last_time || v.currentSrc == "") {
    /* We're hanging, let's reload */
    v.load();
    last_time = -1;
    clearInterval(interval_id);

    /* If we've been running for 2 min, we're reasonably stable */
    if (v.currentTime > 120)
      check_interval = 1000;
    else if (check_interval == 4000)
      check_interval = 5000;
    else
      /* We're checking too often, let's check more seldom */
      check_interval += 1000;

    /* Start the reload-check-timer again */
    setTimeout(setint, check_interval);
  }

  last_time = v.currentTime;
}

function init_videoreload(video_tag) {
  v = document.getElementById(video_tag);

  /* Only set timeout if we've got html5 video support */
  if (!!v.canPlayType)
    setTimeout(setint, 5000);
}
