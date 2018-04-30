function update_sum() {
  var a = $("#add-a").val();
  var b = $("#add-b").val();
  $.ajax({
    url: "/api/sum/" + a + "/" + b,
    success: function(data) {
      $("#add-result").text(data.result);
    },
    error: function() {
      $("#add-result").text("(fail)");
    }
  });
}

var outbound_message = {
    'a': 123
    'b': 'Hello, world'
  };
  $.ajax({
    type: 'POST',
    url: '/api/some/resource',
    data: JSON.stringify(outbound_message),
    dataType: 'json',
    contentType: 'application/json; charset=utf-8',
    success: function(data) {
      $("#echo-result").text(data.txt);
    },
    error: function() {
      $("#echo-result").text("woops");
    }
  });

["#add-a", "#add-b"].forEach(function(item) {
  $(item).on("keyup", function(event) {
    update_sum();
  });
});
