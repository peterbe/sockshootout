var master_count = 0;
var max_master_count;

var log = function(data) {
  //     pre.text(data);
  pre.append($('<span>').text(data));
  pre.append($('<br>'));
};
var pre = $('pre');


var t1, t2;
var finish = function() {
  t2 = new Date();
  //pre.text('Finished!');
  log('Finished');
  var secs = ((t2-t1) /1000);
  var speed = max_master_count / secs
  log(master_count + ' iterations in ' + secs + ' seconds meaning ' + speed + ' messages/second');
  master_count = 0;

};
