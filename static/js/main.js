/*! Author: Asim Ihsan.
*/

$(document).ready(function() {
    /* ---------------------------------------------------------------------
     *  Put the CSRF cookie in the HTTP headers of all unsafe HTTP
     *  requests.
     *
     *  Reference: https://docs.djangoproject.com/en/1.4/ref/contrib/csrf/
     * --------------------------------------------------------------------- */
    jQuery(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
    /* --------------------------------------------------------------------- */

    /* --------------------------------------------------------------------- */
    /*  Handling AJAX polling after starting a search.                       */
    /* --------------------------------------------------------------------- */
    var poll_interval = 500;
    var retry_maximum = 60;
    var retry_count = 1;
    if (typeof search_uuid != "undefined") {
        $("#search_container").mask("Searching...");
        window.check_if_search_is_finished_timer = window.setTimeout(check_if_search_is_finished,
                                                                     poll_interval,
                                                                     is_search_finished_uri);
    }

    function check_if_search_is_finished(is_search_finished_uri) {
        $.ajax({
            url: is_search_finished_uri,
            dataType: 'json',
            contentType: 'application/json',
            error: function(xhr_data) {
                console.log("is_search_finished_uri: " + is_search_finished_uri + " returned error.");
                return false;
            },
            success: function(xhr_data) {
                console.log("is_search_finished_uri: " + is_search_finished_uri + " returned success.");
                if (!("is_search_finished" in xhr_data)) {
                    console.log("is_search_finished_uri: " + is_search_finished_uri + "missing 'is_search_finished");
                    return false;
                }
                if (xhr_data["is_search_finished"] == false) {
                    console.log("search still not finished.");
                    retry_count += 1;
                    if (retry_count <= retry_maximum) {
                        console.log("will retry.");
                        window.check_if_search_is_finished_timer = 
                            window.setTimeout(check_if_search_is_finished,
                                              poll_interval,
                                              is_search_finished_uri);
                        return false;
                    }
                } else if (xhr_data["is_search_finished"] == true) {
                    console.log("search is finished.");
                    window.clearTimeout(check_if_search_is_finished_timer);
                    window.location.replace(xhr_data["read_search_uri"]);
                    return true;
                } else {
                    console.log("is_search_finished result key not boolean.");
                    return false;
                } // parsing 'is_search_finished'
            }, // success callback
        }); // AJAX call
    }
    /* --------------------------------------------------------------------- */

});

