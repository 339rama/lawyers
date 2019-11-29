function goToPage(el) {
    location.href = el.dataset.href;
}

function toggleMenu() {
    let el = document.querySelector('#menu-burger');
    el.classList.toggle('active-menu');
    el.querySelector('div').classList.toggle('dn');
}
function openMenu() {
    let el = document.querySelector('#menu-burger');
    el.classList.add('active-menu');
    el.querySelector('div').classList.remove('dn');
}
function closeMenu() {
    let el = document.querySelector('#menu-burger');
    el.classList.remove('active-menu');
    el.querySelector('div').classList.add('dn');
}
document.addEventListener('DOMContentLoaded', function () {
    let menu_btn = document.querySelector('#menu-burger');
    menu_btn.addEventListener('mouseover', openMenu);
    menu_btn.addEventListener('click', toggleMenu);
    document.addEventListener('click', closeMenu);
    
    lawyer_links = document.querySelectorAll('a.lawyer-links');
    for (let i=0; i<lawyer_links.length; i++){
        lawyer_links[i].addEventListener('click', setLawyerLink);
    }
    function setLawyerLink() {
        lawyer_links = document.querySelectorAll('a.lawyer-links');
            for (let i = 0; i < lawyer_links.length; i++) {
                lawyer_links[i].removeAttribute('style');
            }
        this.style.cssText ='color: #1771E6;'
    }

});

function ShowValues(element) {
    let values = element.parentNode.querySelector('div');
    values.classList.toggle('dn');
    element.classList.toggle('transScaleY-1');
    element.parentNode.classList.toggle('box-shadow');
}

function filterSearch(el) {
    let value = el.value.toLowerCase();
    let list = el.parentNode.querySelector('ul');
    let vars = list.querySelectorAll('li');
    for (let i=0; i < vars.length; i++){
        if (vars[i].innerHTML.toLowerCase().indexOf(value)!=-1){
            vars[i].removeAttribute('style');
        } else{
            vars[i].style.cssText = "display: none;";
        }
    }
}

function SelectValue(element) {
    let input = element.parentNode.parentNode.parentNode.querySelector('input');
    element.parentNode.parentNode.parentNode.querySelector('svg').classList.toggle('transScaleY-1');
    element.parentNode.parentNode.parentNode.classList.toggle('box-shadow');
    input.dataset.value = element.dataset.value;
    input.value = element.innerHTML;
    let siblings = element.parentNode.querySelectorAll('li');
    for (let i = 0; i < siblings.length; i++){
        siblings[i].classList.remove('selected');
    }
    element.classList.add('selected');
    element.parentNode.parentNode.classList.toggle('dn');
    if (window.matchMedia("(max-width: 425px)").matches){
        console.log('ok');
        let filter_btn = document.querySelector('div.filters button.filter-btn');
        let machineEvent = new Event('click');
        filter_btn.dispatchEvent(machineEvent);
    }
}

function filter(element){
    inputs = element.parentNode.querySelectorAll('input[type=text]');
    let url ='/';
    let city;
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].dataset.value !== ''){
            url += inputs[i].dataset.value + '/';
            if ( inputs[i].dataset.uses === 'city' ){
                city = inputs[i].dataset.value;
            }
        }
    }
    fetch(window.location.pathname + '?city=' + city).finally(() => location.href = url);
    
}

function showCities() {
    el = document.querySelector('#current-city');
    el.querySelector('div').classList.toggle('dn');
}

function selectCity(el) {
    let city_slug = el.dataset.value;
    sessionStorage.setItem('city_slug', city_slug);
    let url = window.location.pathname + '?city=' + city_slug;
    document.querySelector('#current-city>span').innerHTML = el.innerHTML;
    let city_links = document.querySelectorAll('.city-page');
    for (let i=0; i<city_links.length; i++){
        city_links[i].setAttribute('href', '/' + city_slug + '/');
    }
    fetch(url).then(function(){
        url_list = location.pathname.split('/');
        if (url_list[1] !== 'lawyer'){
            location.href = (url_list.length == 4 ? '/' + city_slug + '/' + url_list[2] + '/' : '/' + city_slug + '/');
        }
        });
    
}

function showMore(btn) {
    btn.dataset.shown = Number(btn.dataset.shown) + 5;
    url = location.href + '?show=' + btn.dataset.shown;
    fetch(url).then(res => res.text()).then(function(data) {
        btn = document.querySelector('div.list>button');
        btn.insertAdjacentHTML('beforeBegin', data);
    });
}
// GEO
function geo_success(position) {
    url = '/' + '?lat=' + position.coords.latitude + '&lng=' + position.coords.longitude;
    fetch(url)
    .then(res => res.text())
    .then(function(data) {
        // sessionStorage.setItem('city_name', JSON.parse(data).city_slug);
        ShowConfirmCity(data);
        console.log('wrong');
        // window.location.reload(true);

    });
    console.log('Lat:' + position.coords.latitude, 'Lng:' + position.coords.longitude);
};

function ConfirmCity(elem) {
    document.querySelector('div.confirm-city').classList.add('dn');
    sessionStorage.setItem('city_slug', elem.dataset.city);
    window.location.reload(true);
}

function ShowConfirmCity(data) {
    document.querySelector('div.confirm-city').classList.remove('dn');
    document.querySelector('button.confirm-city').dataset.city = JSON.parse(data).city_slug;
    document.querySelector('div.confirm-city p:last-of-type').innerHTML = JSON.parse(data).city_name;
}
function NotConfirmCity() {
    document.querySelector('div.confirm-city').classList.add('dn');
    showCities();
}

function geo_error(err) {
    console.log('Geo Error', err)
    if (sessionStorage.getItem('city_slug') === null) {
        showCities();
    }
}

let geo_options = {
    enableHighAccuracy: true,
    maximumAge: 30000,
    timeout: 27000
};

if (sessionStorage.getItem('city_slug') === null){
    navigator.geolocation.getCurrentPosition(geo_success, geo_error, geo_options);
} else{
    console.log(sessionStorage.getItem('city_slug'));
}
//  GEO END
