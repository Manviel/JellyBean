$(function() {
  $(".js-upload-photos").click(function() {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function(e, data) {
      if (data.result.is_valid) {
        $("#gallery").prepend("<img class='avatar' src='" + data.result.url + "'>")
      }
    }
  });
});
