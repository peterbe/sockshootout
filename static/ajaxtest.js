


var loop = function() {
  master_count++;
  $.get('/ajaxecho', {msg: '' + master_count}, function(r) {
    //log(r);
    if (master_count < max_master_count) {
      loop();
    } else {
      finish();
    }

  })
};

$('button').click(function() {
  log('start!')
  t1 = new Date();
  loop();
  return false;
});
