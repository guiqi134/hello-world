$('.change_location').click(function() {
    let myAddress = prompt('请输入你的地址');    
    $.ajax({
        url: '/index/',
        method: 'POST', // or another (GET), whatever you need
        data: {
            'address': myAddress, // data you need to pass to your function
            'click': true
        },
        context: this,
        success: function(data) {
            let current_location = document.querySelector('.current_location');
            current_location.textContent = data
        }, 
    });
});