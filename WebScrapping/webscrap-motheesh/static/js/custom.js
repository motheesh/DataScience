$(document).ready(function () {
  $("#basic").hide();
  $("#spinner").hide();
});
function handleSelect() {
  action_val = $("#assignment").val();
  if (action_val == "basic") {
    $("#basic").show();
    $("#adv").hide();
  } else {
    $("#basic").hide();
    $("#adv").show();
  }
}
function HandleSearch2() {
  var search = $("#searchKey").val();
  var no = $("#numberofreviews").val();
  $("#spinner").show();
  $.get(
    "/getallreviews",
    { keyword: search, numberofreview: no },
    function (result) {
      //$.get("/search", {"keyword":search},  function(result){
      $("#div1").html(result);
      $("#spinner").hide();
    }
  );
}

function HandleSearch() {
  var search = $("#keyword").val();
  $.get(
    "/getallreviews",
    { keyword: search, numberofreview: 10 },
    function (result) {
      //$.get("/search", {"keyword":search},  function(result){
      $("#div1").html(result);
    }
  );
}
