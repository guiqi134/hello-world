$('.take_order').click(function() {
    var order_id = $(this).closest("tr")   // Finds the closest row <tr> 
                       .find(".order_id")     // Gets a descendent with class="nr"
                       .text();
    $.ajax({
        url: '/rider/',
        method: 'POST', // or another (GET), whatever you need
        data: {
            'status': 'take_order',
            'order_id': order_id,
            'click': true
        },
        context: this,
        success: function(data) {
            alert('接单成功!')
        },
        error: function() { alert("fail") } 
    });
});