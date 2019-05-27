$('.change_FName').click(function() {
    let myFName = prompt('请输入食物名称');
    var food_id = $(this).parent("div").parent("div")   
                       .find(".food_id")     
                       .text();
    $.ajax({
        url: '/restaurant/',
        method: 'POST', // or another (GET), whatever you need
        data: {
            'status': 'change_FName',
            'food_name': myFName, // data you need to pass to your function
            'food_id': food_id,
            'click': true
        },
        context: this,
        success: function(data) {
            $(this).text(data)
        },
        error: function() { alert("fail") } 
    });
});

$('.change_price').click(function() {
    let myprice = prompt('请输入食物价格');
    var food_id = $(this).parent("span").parent("div")   
                       .find(".food_id")     
                       .text();
    $.ajax({
        url: '/restaurant/',
        method: 'POST', // or another (GET), whatever you need
        data: {
            'status': 'change_price',
            'food_price': myprice, // data you need to pass to your function
            'food_id': food_id,
            'click': true
        },
        context: this,
        success: function(data) {
            $(this).text('¥ ' + data)
        },
        error: function() { alert("fail") } 
    });
});

$('.change_count').click(function() {
    let mycount = prompt('请输入食物剩余数量');
    var food_id = $(this).parent("span").parent("div")   
                       .find(".food_id")     
                       .text();
    $.ajax({
        url: '/restaurant/',
        method: 'POST', // or another (GET), whatever you need
        data: {
            'status': 'change_count',
            'food_count': mycount, // data you need to pass to your function
            'food_id': food_id,
            'click': true
        },
        context: this,
        success: function(data) {
            $(this).text('剩余: ' + data)
        },
        error: function() { alert("fail") } 
    });
});