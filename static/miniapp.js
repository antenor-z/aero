function showMiniApp(location) {
    const iframe = document.getElementsByTagName('iframe')[0]
    iframe.src = location

    document.getElementById('iframe-container').style.display = 'none'

    iframe.onload = function() {
        document.getElementById('iframe-container').style.display = 'block'
    }
}

function toggleMenu(event) {
    const menu = document.getElementById('menu');
    
    if (menu.style.display === "none") {
        menu.style.display = "grid";
        menu.style.left = `${event.pageX-200}px`;
        menu.style.top = `${event.pageY}px`;
    } else {
        menu.style.display = "none";
    }
}

document.addEventListener('click', closeMenu)
document.addEventListener('scroll', closeMenu)


function closeMenu (event) {
    const menu = document.getElementById('menu');
    const ellipsisBtn = document.getElementById('ellipsis-btn');
    
    if (!ellipsisBtn.contains(event.target)) {
        menu.style.display = 'none';
    }
}