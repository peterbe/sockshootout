
var sock;
var initsock = function(callback) {
   sock = new SockJS('http://localhost:9999/echo');
   sock.onmessage = function(e) {
       //console.log('message', e.data);
       //log(e.data);
       if (master_count < max_master_count) {
         loop();
       } else {
         finish();
       }
   };
   sock.onclose = function() {
       console.log('close');
   };
   sock.onopen = function() {
       //log('opened');
       //console.log('open');
       //sock.send('test');
     callback();

   };
};


var loop = function() {
  master_count++;
  sock.send('' + master_count);

};
$('button').click(function() {
  initsock(function() {
    log('start!');
    t1 = new Date();
    loop();
  });
  return false;
});
