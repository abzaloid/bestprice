var item_store_dict = {}, item_price_dict = {};

function _update(name, store, price){
  if (!item_store_dict[name])
    item_store_dict[name] = [];
  if (!item_price_dict[name])
    item_price_dict[name] = [];
  
  item_store_dict[name].push(store);
  item_price_dict[name].push(price);
}

function popupwindow(item_name, item_price, item_description, item_image) {
    var my_table = "<table class='table table-hover'><tbody><tr>";
    for (var i = 0; i < item_store_dict[item_name].length; i++) {
      my_table+="<th>"+ item_store_dict[item_name][i] +"</th>";  
    }
    my_table+="</tr><tr>";
    for (var i = 0; i < item_price_dict[item_name].length; i++) {
      my_table+="<td>"+ item_price_dict[item_name][i] +"тг </td>"; 
    }
    my_table+="</tr></tbody></table>";  
    new Messi(item_description + "<br/> <img src='"+item_image+"' width='150' height='150' style='margin:auto;'/><hr/>" + my_table, {title: item_name, modal: true} );
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

var textarea_visible = 0;
var search_visible = 0;
var current_item = "";

$(document).ready(function(){
  $(".subcategory").click(function(){
    var _id = $(this).attr('class').match(/\d+/)[0];
    if (!$(this).hasClass("active")) {
      $(this).addClass("active");
      window.location.href = "/all-subcategory/" + _id;
    } else {
      $(this).removeClass("active");
      window.location.href = "/all-subcategory-except/" + _id;
    }
  });

  $("#dLabel").click(function(e){
    if (!textarea_visible) {
      $(this).parent().find('.list-group.damnit').show();
      textarea_visible = 1;
      e.stopPropagation(); 
      return false; 
    }
    else {
      $(this).parent().find('.list-group.damnit').hide();
      textarea_visible = 0;
    }
  });
  $("body").click(function(){
    $(this).parent().find('.list-group.damnit').hide();
    $(".list-group.search").hide();
    search_visible = 0;
    textarea_visible = 0;
  });
  $("#search_form").click(function(e){
    if (!search_visible) {
      search_visible = 1;
      $(".list-group.search").show();
      e.stopPropagation(); 
      return false; 
    }
  });
  $(".list-group.damnit").click(function(e){
     e.stopPropagation(); 
    return false; 
   });


  $("#search_textarea").click(function(){
    var subcategory = $("#shop_list_textarea").val().toLowerCase();
    subcategory = subcategory.replace(/\r?\n/g, ' ');
    window.location.href = "/shopping_list?subcat=" + subcategory;

  });
});

