function goToPage(el) {
    let opened_dialog = document.querySelector('dialog').getAttribute('open');
    if (!opened_dialog.getAttribute('open') == 'open'){
        location.href = el.dataset.href;
    }
}

function toggleMenu() {
    let el = document.querySelector('#menu-burger');
    el.classList.toggle('active-menu');
    el.querySelector('div').classList.toggle('dn');
}
function openMenu() {
    if (!window.matchMedia("(max-width: 425px)").matches) {
        let el = document.querySelector('#menu-burger');
        el.classList.add('active-menu');
        el.querySelector('div').classList.remove('dn');
    }else if (document.querySelector('#menu-burger>svg').dataset.action === 'back'){
        let index = document.querySelectorAll('div[data-state=open]').length - 1;
        document.querySelectorAll('div[data-state=open]')[index].querySelector('div').removeAttribute('style');
        document.querySelectorAll('div[data-state=open]')[index].removeAttribute('data-state');
        if (!index>0){
            document.querySelector('#menu-burger>svg').removeAttribute('data-action');
        }
    }else{
        toggleMenu();
        document.querySelector('header').classList.toggle('dark-bg');
    }
}

function mobileMenuOpenSub(el) {
    if (window.matchMedia("(max-width: 425px)").matches) {
        el.querySelector('div').style.left = 0;
        document.querySelector('#menu-burger>svg').dataset.action = 'back';
        el.dataset.state = 'open';
    }
}
function closeMenu() {
    if (!window.matchMedia("(max-width: 425px)").matches) {
        let el = document.querySelector('#menu-burger');
        el.classList.remove('active-menu');
        el.querySelector('div').classList.add('dn');
    }
}
document.addEventListener('DOMContentLoaded', function () {
    let menu_btn = document.querySelector('#menu-burger');
    if (!window.matchMedia("(max-width: 425px)").matches) {
        menu_btn.addEventListener('mouseover', openMenu);
        menu_btn.addEventListener('click', toggleMenu);
        document.addEventListener('click', showCities);
    } else {
        // Rebuilt menu to mobile
        let menu_inner_conts = document.querySelectorAll('#menu-burger>div>div');
        let lawyers_cont = document.createElement('div');
        lawyers_cont.setAttribute('onclick', 'mobileMenuOpenSub(this)');
        lawyers_cont.setAttribute('onclick', 'mobileMenuOpenSub(this)');
        let img_arrow = '<img src="/static/images/arrow-right.svg">';
        let div = document.createElement('div');
        lawyers_cont.insertAdjacentHTML('afterBegin', '<a href="">Наши юристы</a>');
        lawyers_cont.insertAdjacentHTML('beforeend', img_arrow);
        [...menu_inner_conts].forEach(function(el){
            let el_clone = el.cloneNode(true);
            div.appendChild(el_clone);
            el.parentNode.removeChild(el);
        });
        lawyers_cont.appendChild(div);
        document.querySelector('#menu-burger>div').appendChild(lawyers_cont);
        // Rebuilt menu to mobile
        // Append city-settings in menu start
        let city_elem = document.querySelector('#current-city').cloneNode(true);
        document.querySelector('#current-city').parentNode.removeChild(document.querySelector('#current-city'));
        let city_cont = document.createElement('div');
        city_cont.setAttribute('onclick', 'mobileMenuOpenSub(this)');
        city_cont.appendChild(city_elem);
        // let img_arrow = '<img src="/static/images/arrow-right.svg">';
        city_cont.insertAdjacentHTML('beforeend', img_arrow);
        city_cont.appendChild(city_elem.querySelector('div'));
        city_elem.removeChild(city_elem.querySelector('div'));
        city_elem.insertAdjacentHTML('afterBegin', 'Ваш город: ')
        city_cont.querySelector('div').removeAttribute('class');
        document.querySelector('#menu-burger>div').appendChild(city_cont);
        // Append add-link in menu start
        let add_link = document.getElementById('add-offer').cloneNode(true);
        document.getElementById('add-offer').parentNode.removeChild(document.getElementById('add-offer'));
        add_link.insertAdjacentHTML('beforeend', img_arrow);
        add_link.insertAdjacentHTML('afterbegin', '+ ');
        document.querySelector('#menu-burger>div').appendChild(add_link);
        // Append add-link in menu end
            // city search start
        let input = document.createElement('input');
        input.classList.add('city_search');
        input.setAttribute('oninput', 'filterSearch(this)');
        city_cont.querySelector('div').appendChild(input);
            // city search end
        // Append city-settings in menu end
    }
    
    
    lawyer_links = document.querySelectorAll('a.lawyer-links');
    [...lawyer_links].forEach(function(el, i , arr) {
        el.addEventListener('click', setLawyerLink);
    })
    function setLawyerLink() {
        lawyer_links = document.querySelectorAll('a.lawyer-links');
        [...lawyer_links].forEach(function (el, i, arr) {
            el.removeAttribute('style');
        })
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

function showCities(event) {
    el = document.querySelector('#current-city');
    console.log(event);
    if ((event.target.innerText === 'Нет, другой') || event.toElement == el.querySelector('span')){
        el.querySelector('div').classList.toggle('dn');
    } else if (event.toElement != el.querySelector('span'))  {
        console.log('ok');
        el.querySelector('div').classList.add('dn');
    }
}

function selectCity(el) {
    let city_slug = el.dataset.value;
    sessionStorage.setItem('city_slug', city_slug);
    let url = window.location.pathname + '?city=' + city_slug;
    document.querySelector('#current-city>span').innerHTML = el.innerHTML;
    let city_links = document.querySelectorAll('.city-page');
    [...city_links].forEach(function(city_link) {
        city_link.setAttribute('href', '/' + city_slug + '/');
    });
    fetch(url).then(function(){
        url_list = location.pathname.split('/');
        if (url_list[1] !== 'lawyer'){
            location.href = (url_list.length == 4 ? '/' + city_slug + '/' + url_list[2] + '/' : '/' + city_slug + '/');
        }
        });
    
}

function showMore(btn) {
    btn.dataset.shown = Number(btn.dataset.shown) + 10;
    url = location.pathname + '?show=' + btn.dataset.shown;
    fetch(url).then(res => res.text()).then(function(data) {
        btn = document.querySelector('div.list>button');
        btn.insertAdjacentHTML('beforeBegin', data);
    });
}
// GEO START
function geo_success(position) {
    url = '/' + '?lat=' + position.coords.latitude + '&lng=' + position.coords.longitude;
    fetch(url)
    .then(res => res.text())
    .then(function(data) {
        // sessionStorage.setItem('city_name', JSON.parse(data).city_slug);
        if (!window.matchMedia("(max-width: 425px)").matches) {
            ShowConfirmCity(data);
        }
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
}
//  GEO END

// Forms
function OpenDialog(el) {
    event.preventDefault();
    document.querySelector('dialog').setAttribute('open', 'open');
    document.querySelector('dialog').style.top = String(window.pageYOffset)+'px';
    document.querySelector('body').style.overflow = 'hidden';
}
function CloseCustomDialog(el) {
    el.parentNode.parentNode.removeAttribute('open');
    document.querySelector('body').removeAttribute('style');
}

document.addEventListener('DOMContentLoaded', function () {
    let opened_dialog = document.querySelector('dialog[open="open"]');
    if (opened_dialog !=null){
        opened_dialog.style.top = String(window.pageYOffset) + 'px';
    }
});