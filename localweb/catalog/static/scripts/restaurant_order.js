$('.order_status').click(function() {
    let change_status = prompt('订单是否送出？(未起送/正在配送)');
    var order_id = $(this).closest("tr")   // Finds the closest row <tr> 
                       .find(".order_id")     // Gets a descendent with class="nr"
                       .text();
    $.ajax({
        url: '/restaurant/restaurant_order/',
        method: 'POST', // or another (GET), whatever you need
        data: {
            'status': 'change_status',
            'order_status': change_status, // data you need to pass to your function
            'order_id': order_id,
            'click': true
        },
        context: this,
        success: function(data) {
            $(this).text(data)
        },
        error: function() { alert("fail") } 
    });
});