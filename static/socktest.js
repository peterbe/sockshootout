SockJS.prototype.send_json = function(data) {
  this.send(JSON.stringify(data));
};



var loop = (function() {
  var data_function;
  var sock;
  var initsock = function(callback) {
    sock = new SockJS('http://' + location.hostname + ':9999/echo');

    sock.onmessage = function(e) {
      master_count = e.data.count;
      if (master_count < max_master_count) {
        sock.send_json(data_function())
      } else {
        finish();
        sock.close();
      }
    };
    sock.onclose = function() {
      //console.log('closed');
    };
    sock.onopen = function() {
      //log('opened');
      //console.log('open');
      //sock.send('test');
      if (sock.readyState !== SockJS.OPEN) {
        throw "Connection NOT open";
      }
      callback();
    };
  };

  return {
     start: function(df) {
       data_function = df;
       initsock(function() {
         sock.send_json(data_function());
       });
     },
    close: function() {
       sock.close();
     }
  }
})();


$('button').click(function() {
  max_master_count = parseInt($('#iterations').val());
  log('start!');
  t1 = new Date();
  loop.start(function() {
    //master_count++;
    return {count: master_count};
  });

  return false;
});
