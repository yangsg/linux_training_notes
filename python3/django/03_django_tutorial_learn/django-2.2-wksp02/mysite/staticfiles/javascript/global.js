(function (global) {
    var common = global.common = {};

    common.init = init;
    common.getCsrfToken = getCsrfToken;
    common.getCookie = getCookie;

    var CSRF_COOKIE_NAME = 'csrftoken';

    function init() {
        initCrsfTokenForAjax();
    }

    function initCrsfTokenForAjax() {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCsrfToken());
                }
            }
        });
    }

    function getCsrfToken() {
        return getCookie(CSRF_COOKIE_NAME);
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
    // https://github.com/js-cookie/js-cookie/
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

})(window);