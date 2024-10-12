const lastUrlKey = "lastUrl";

if (document.location.pathname == '/' && !document.referrer) {
    if (lastUrlKey in localStorage) {
        let url = localStorage.getItem(lastUrlKey)
        if (url !== document.location.pathname) {
            location.href = url;
        }
    }
}

localStorage.setItem(lastUrlKey, location.href);