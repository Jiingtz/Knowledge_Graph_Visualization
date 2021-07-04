(function (a) {
    if (typeof define === "function" && define.amd) {
        define(["jquery"], a)
    } else {
        if (typeof exports === "object") {
            a(require("jquery"))
        } else {
            a(jQuery)
        }
    }
}
(function (b) {
    b(window).bind("scroll", function () {
        var c = b(".mask");
        for (var d = 0; d < c.length; d++) {
            var h = b(c[d]).attr("ele");
            var g = b(h).offset().top;
            var f = b(document).scrollTop();
            var e = g - f;
            b(c[d]).css({"top": e + "px"})
        }
    });
    var a = {};
    b.mask_fullscreen = function (e) {
        if (b(".mask[ele=full_screen]").length > 0) {
            return
        }
        // b("body").addClass("scroll-off");
        var c = '<div style="z-index: 1001" class="mask" ele="full_screen"><div class="cssload-container">\n' +
            '\t<div class="cssload-whirlpool"></div>\n' +
            '</div></div>';
        b("body").append(c);
        clearTimeout(a["full_screen"]);
        if (e && e > 0) {
            var d = setTimeout(function () {
                b(".mask[ele=full_screen]").remove();
                b("body").removeClass("scroll-off")
            }, e);
            a["full_screen"] = d
        }
    };
    b.mask_element = function (f, e) {
        if (b(".mask[ele=" + f + "]").length > 0) {
            return
        }
        var c = '<div class="mask" ele=' + f + ' style="width: ' + b(f).width() + "px !important; height: " + b(f).height() + "px !important; left: " + b(f).offset().left + "px !important; top: " + b(f).offset().top + 'px !important;"><div>数据加载中...</div></div>';
        b("body").append(c);
        clearTimeout(a[f]);
        if (e && e > 0) {
            var d = setTimeout(function () {
                b(".mask[ele=" + f + "]").remove()
            }, e);
            a[f] = d
        }
    };
    b.mask_close = function (c) {
        b(".mask[ele=" + c + "]").remove()
    };
    b.mask_close_all = function () {
        b(".mask").remove()
    }
}));