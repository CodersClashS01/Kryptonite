(function (window, document) {
    window.addEventListener('load', function () {
        var el = document.getElementById("guild_select");
        console.log(el);
        el.addEventListener("change", function () {
            var gid = el.value;
            if (isNaN(parseInt(gid))) {
                return;
            }
            console.log('gid');
            location.href = '/guild/' + gid;
        })
    })
})(window, document);