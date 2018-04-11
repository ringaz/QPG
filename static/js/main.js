$(function () {


  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-question").modal("show");
      },
      success: function (data) {
        $("#modal-question .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#question-table tbody").html(data.html_question_list);
          $("#modal-question").modal("hide");
        }
        else {
          $("#modal-question .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create question
  $(".js-create-question").click(loadForm);
  $("#modal-question").on("submit", ".js-question-create-form", saveForm);

  // Update question
  $("#question-table").on("click", ".js-update-question", loadForm);
  $("#modal-question").on("submit", ".js-question-update-form", saveForm);

  // Delete question
  $("#question-table").on("click", ".js-delete-question", loadForm);
  $("#modal-question").on("submit", ".js-question-delete-form", saveForm);



   /************ QPGenarator ************/







  /************ End QPGenarator ************/

});
