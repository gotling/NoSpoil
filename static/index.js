const lastUrlKey = "lastUrl";
const lastNameKey = "lastName";

if (document.location.pathname == '/') {
    if (lastUrlKey in localStorage) {
        let url = localStorage.getItem(lastUrlKey);
        let name = localStorage.getItem(lastNameKey);

        if (url !== document.location.pathname) {
            var a = document.getElementById('history-link');
            a.href = url;
            a.innerText = name;
        }
    }
} else {
    localStorage.setItem(lastUrlKey, location.href);
    localStorage.setItem(lastNameKey, LAST_NAME);
}
