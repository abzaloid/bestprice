function popupwindow(item_name, item_price, item_description, item_image) {
    new Messi(item_description + "<br/> <img src='"+item_image+"' width='150' height='150' style='margin:auto;'/><hr/>Цена " + item_price + "тг. ", {title: item_name, modal: true} );
}
function removeItem(class_name, _id, item_name_safe) {
    var last_quantity = $("." + class_name + " > .td2").text();
    $("."+class_name).slideUp(800, function() {
        $("."+class_name).remove();
    });

    cur = "Добавить"
    $(".addtocart"+_id).text(cur);
    $(".plus"+_id).hide();
    $(".minus"+_id).hide();

    $.ajax({
       type: "POST",
       url: "/delitem",
       dataType: 'json',
       data: JSON.stringify({"item": item_name_safe, "last_quantity" : last_quantity})
     })
    .always(function (data) {
       if (data["status"] == 0) {
         alert("Войдите в систему, чтобы совершить покупку");
       } else {
           var qnt = parseInt(data["number"]);
           $(".itemCount").text(qnt.toString());
           for (var key in data) {
             if (key.indexOf("0123456789")) {
               $(".my_store" + key).text(data[key].toString() + "тг");
             }
           }
        }
      });                             
}

$(document).ready(function(){
  $(".subcategory").click(function(){
    var _id = $(this).attr('class').match(/\d+/)[0];
    if (!$(this).hasClass("active")) {
      $(this).addClass("active");
      window.location.replace("/all-subcategory/" + _id);
    } else {
      $(this).removeClass("active");
      window.location.replace("/all-subcategory-except/" + _id);
    }
  });

  $("#shopping_list").click(function(){
    if ($(this).parent().children().length == 1)
      $(this).parent().append("<div id='shop_list'><ul><li><textarea style='height: 150px;'></textarea></li><li><button class='btn btn-default' type='button'>Найти</button></li></ul></div>");
  });

});

