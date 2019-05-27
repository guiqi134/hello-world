$('.change_rest').click(function() {
    let myrest_rating = prompt('请输入评分(区间为0～5)');
    var order_id = $(this).closest("tr")   // Finds the closest row <tr> 
                       .find(".order_id")     // Gets a descendent with class="nr"
                       .text();
    $.ajax({
        url: '/index/customer_order/',
        method: 'POST', // or another (GET), whatever you need
        data: {
            'status': 'restaurant',
            'rest_rating': myrest_rating, // data you need to pass to your function
            'order_id': order_id,
            'click': true
        },
        context: this,
        success: function(data) {
            if (!(data>=0 && data<=5)) {
                alert("输入评分范围错误")
            }
            $(this).text(data)
        },
        error: function() { alert("fail") } 
    });
});

$('.change_rider').click(function() {
    let myrider_rating = prompt('请输入评分(区间为0～5)');
    var order_id = $(this).closest("tr")   // Finds the closest row <tr> 
                       .find(".order_id")     // Gets a descendent with class="nr"
                       .text();   
    $.ajax({
        url: '/index/customer_order/',
        method: 'POST', // or another (GET), whatever you need
        data: {
            'status': 'rider',
            'rider_rating': myrider_rating, // data you need to pass to your function
            'order_id': order_id,
            'click': true
        },
        context: this,
        success: function(data) {
            if (!(data>=0 && data<=5)) {
                alert("输入评分范围错误")
            }
            $(this).text(data)
        },
        error: function() { alert("fail") }  
    });
});

