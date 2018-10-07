$(function () {
  $(".js-create").click(function () {
    $.ajax({
      url: '/boards/create/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-board").modal("show");
      },
      success: function (data) {
        $("#modal-board .modal-content").html(data.html);
      }
    });
  });

  $("#modal-board").on("submit", ".js-create-form", function() {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#board-table tbody").html(data.list);
          $("#modal-board").modal("hide");
        }
        else {
          $("#modal-board .modal-content").html(data.html);
        }
      }
    });
    return false;
  });
});
