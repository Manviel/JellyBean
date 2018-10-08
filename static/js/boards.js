$(function () {
  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-board").modal("show");
      },
      success: function (data) {
        $("#modal-board .modal-content").html(data.html);
      }
    });
  };

  var saveForm = function() {
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
  };

  $(".js-create").click(loadForm);
  $("#modal-board").on("submit", ".js-create-form", saveForm);

  $("#board-table").on("click", ".js-update", loadForm);
  $("#modal-board").on("submit", ".js-update-form", saveForm);

  $("#board-table").on("click", ".js-delete", loadForm);
  $("#modal-board").on("submit", ".js-delete-form", saveForm);
});
