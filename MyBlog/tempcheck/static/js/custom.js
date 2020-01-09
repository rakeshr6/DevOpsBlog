
// Get the form fields and hidden div
var checkbox = $(".trigger");
var hidden = $(".hidden_fields");
// var populate = $
// ("#populate");

// hidden.hide();
// checkbox.change(function() {
//   if (checkbox.is(':checked')) {
//     hidden.show();
//   } else {
//     hidden.hide();
//
//   }

hidden.hide();

checkbox.change(function () {
  if (checkbox.is(":checked")){
    hidden.show();
  }
  else{
    hidden.hide();
  }
});
