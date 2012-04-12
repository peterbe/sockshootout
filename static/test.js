var master_count = 0;

   var log = function(data) {
     pre.text(data);
//       pre.append($('<span>').text(data));
       //pre.append($('<br>'));

   };
   var pre = $('pre');

var sock;
var initsock = function(callback) {
   sock = new SockJS('http://localhost:9999/echo');
   sock.onmessage = function(e) {
       //console.log('message', e.data);
       log(e.data);
       if (master_count < 100) {
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

var t1, t2;
var finish = function() {
  t2 = new Date();
  pre.text('Finished!');
  pre.text((t2-t1) /1000 + ' seconds');

};

var loop = function() {
  master_count++;
  sock.send('' + master_count);

};
$('button').click(function() {
  initsock(function() {
    t1 = new Date();
    loop();
  });
  return false;
});
