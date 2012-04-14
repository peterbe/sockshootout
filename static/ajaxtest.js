var loop = (function() {
  var data_function;

  var go = function() {
    $.getJSON('/ajaxecho', data_function(), function(r) {
      //log(r);
      master_count = r.count;
      if (master_count < max_master_count) {
        go();
      } else {
        finish();
      }
    });
  };

  return {
     start: function(df) {
       data_function = df;
       go();
     }
  }

})();
$('button').click(function() {
  max_master_count = parseInt($('#iterations').val());
  log('start!')
  t1 = new Date();
  loop.start(function() {
    return {count: master_count};
  });
  return false;
});
