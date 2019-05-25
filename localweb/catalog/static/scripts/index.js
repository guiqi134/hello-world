let change_location = document.querySelector('.change_location')

change_location.onclick = function setAddress() {
    let myAddress = prompt('请输入你的地址');
    localStorage.setItem('address', myAddress);
    let address_field = document.querySelector('.current_location');
    address_field.textContent = myAddress;
} 
