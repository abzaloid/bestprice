$(function(){

    var current_size = 0;
    $('.size_btn li a').click(function(){
        var clicked_li = $(this).parent();
        clicked_li.siblings().removeClass('active');
        clicked_li.addClass('active');
        current_size = $(this).data('size');
    });

    $('.add_to_cart').click(function(){
        var qty = $('#qty_input').val();
        if (isNaN(parseInt(qty)) || parseInt(qty) == 0) { 
            alert("Please add a valid quantity");
            return false; 
        }
        var queryString = "tshirt_id=" + $('.main_img').data('tshirt_id') + 
                    "&qty=" + qty + "&size=" + current_size + 
                    "&item_title=" + $.trim($('.product_title').text());
        
        $.getJSON('/cart/add', queryString, function(data){
            if (data["status"] == 1) {
                var newcount = parseInt($.trim($('.itemCount').text())) + parseInt(qty);
                $('.itemCount').text(newcount);
            }
            $('#addition_details').html(data["msg"]);
            console.log(data["msg"]);
        });
        return false;
    });

 $('.button-checkbox').each(function () {

        // Settings
        var $widget = $(this),
            $button = $widget.find('button'),
            $checkbox = $widget.find('input:checkbox'),
            color = $button.data('color'),
            settings = {
                on: {
                    icon: 'glyphicon glyphicon-check'
                },
                off: {
                    icon: 'glyphicon glyphicon-unchecked'
                }
            };

        // Event Handlers
        $button.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });

        // Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $button.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $button.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$button.data('state')].icon);

            // Update the button's color
            if (isChecked) {
                $button
                    .removeClass('btn-default')
                    .addClass('btn-' + color + ' active');
            }
            else {
                $button
                    .removeClass('btn-' + color + ' active')
                    .addClass('btn-default');
            }
        }

        // Initialization
        function init() {

            updateDisplay();

            // Inject the icon if applicable
            if ($button.find('.state-icon').length == 0) {
                $button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i>');
            }
        }
        init();
    });
    
});
