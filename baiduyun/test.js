/**
 * Created by 15850 on 2017/7/29.
 */
;define("system-core:system/uiService/button/button.js", function (t, n, i) {
    var e = t("base:widget/libs/jquerypacket.js"), o = t("base:widget/libs/underscore.js"),
        s = t("base:widget/tools/tools.js"), a = t("system-core:system/uiService/log/log.js").instanceForSystem,
        d = (s.client().browserString, function (t) {
            d._length++, this.startTime = (new Date).getTime(), this.dom = null, this.width = 0, this.height = 0, this.container = null, this.menu = {}, this.menuLength = 0, this.id = "b" + d._length++, this.type = t.type || "default", this.config = t, this.config.buttonDefaultConfig = t.buttonDefaultConfig || {}, this._init()
        });
    d._map = {}, d._length = 0, d._secondMenuCallbacks = {}, d.getButton = function (t) {
        return d._map["b" + t] ? d._map["b" + t] : null
    }, d.TPL = o.template('<a class="g-button<%- tips ? \' g-button-hastips\' : ""%>" data-button-id="<%- id %>" data-button-index="<%- index %>" href="<%- link %>" ><span class="g-button-right"><% if (typeof icon !== "undefined") { %><em class="icon <%- icon %>" title="<%- tips ? "" : title %>"></em><% } %><span class="text"><%- title %></span></span><% if (tips !== "") { %><span class="g-button-tips"><%- tips%></span><% } %></a>'), d.prototype = {
        constructor: d,
        _init: function () {
            this._initUserEvent(), this._renderButton(), d._map[this.id] = this
        },
        _renderButton: function () {
            var t = "javascript:void(0);";
            /^(\/|(https?\:\/\/)?(([a-zA-Z0-9]|[\.\-])+){1,3}(cn|com|co|io|gov|org|tv|hk|tw|me))\/?/i.test(this.config.link) && (t = this.config.link);
            var n = {
                title: this.config.title || "",
                icon: this.config.icon,
                id: this.id,
                index: this.config.index,
                link: t,
                tips: this.config.tips || ""
            }, i = d.TPL(n);
            if ("dropdown" === this.type) {
                var o = '<span class="g-dropdown-button"></span>';
                if (this.dom = e(o), this.dom.append(i), this.dom.menu = e('<span class="menu"></span>'), this.dom.append(this.dom.menu), this.dom.mainButton = this.dom.find(".g-button"), "object" == typeof this.config.menu && this.config.menu.length) {
                    var s = this._renderMenuList(this.config.menu);
                    this.dom.menu.append(s)
                }
            } else this.dom = e(i), this.dom.mainButton = this.dom;
            var u = this._caulateClassName();
            this.dom.mainButton.addClass(u), this._initSizeAndPosition(), this._initDomEvent(), this.isShow = !0, this.isEnable = !0, "none" === this.config.display && (this.dom[0].style.display = "none", this.isShow = !1);
            var h = (new Date).getTime() - this.startTime;
            a.send({name: "buttonCreate", value: h})
        },
        _initSizeAndPosition: function () {
            "left" === this.config.position ? this.dom.css("float", "left") : "right" === this.config.position && this.dom.css("float", "right");
            var t = 0, n = 0;
            this.dom.mainButton.find(".text").width("undefined" != typeof this.config.textWidth ? this.config.textWidth : "auto"), "undefined" != typeof this.config.iconMarginRight && this.dom.mainButton.find(".icon").css("margin-right", this.config.iconMarginRight);
            var i = this.dom.mainButton;
            this.config.padding instanceof Array && 2 === this.config.padding.length && (t = this.config.padding[0], n = this.config.padding[1], i.css("padding-left", t), i.find(".g-button-right").css("padding-right", n)), "string" == typeof this.config.margin && i.css("margin", this.config.margin)
        },
        _renderMenuOne: function (t) {
            var n = "b-menu" + this.menuLength++;
            this.menu[n] = t;
            var i = "", e = "", o = "";
            if ("none" === t.display && (e = ' style="display:none;"'), "function" == typeof t.display && (o = t.display()), t.symLink && t.symLink.config && "dropdown" === t.symLink.config.type && t.symLink.config.multiMenu) {
                t.symLink.config.menuLevel = 2;
                var s = new d(t.symLink.config);
                s.dom.addClass("g-dropdown-button-second"), s.dom.attr("menuLevel", 2);
                var a = s.dom[0].outerHTML;
                return s.id && t.symLink.config.menu && (d._secondMenuCallbacks[s.id] = t.symLink.config.menu), a = "<span" + e + ' data-menu-id="' + n + '" class="g-button-menu g-menu-hasIcon">' + a + "</span>"
            }
            return "string" == typeof t.icon ? (i = '<em class="icon ' + t.icon + '"></em>', "<a" + e + ' data-menu-id="' + n + '" class="g-button-menu g-menu-hasIcon" href="javascript:void(0);">' + i + t.title + "</a>") : t.symLink && t.symLink.config.buttonClass && t.symLink.config.filesType ? "<a" + e + ' data-menu-id="' + n + '" data-excludetype="' + t.symLink.config.filesType + '"  class="g-button-menu ' + t.symLink.config.buttonClass + '" href="javascript:void(0);">' + t.title + "</a>" : t.symLink && t.symLink.config.buttonClass && t.symLink.config.excludeDirType ? "<a" + e + ' data-menu-id="' + n + '" data-excludedir="' + t.symLink.config.excludeDirType + '"  class="g-button-menu ' + t.symLink.config.buttonClass + '" href="javascript:void(0);">' + t.title + "</a>" : "<a " + e + ' data-menu-id="' + n + '" class="g-button-menu ' + o + '" href="javascript:void(0);">' + t.title + "</a>"
        },
        _renderMenuList: function (t, n) {
            var i = "";
            if ("object" == typeof t) {
                if (t.length)for (var o = 0, s = t.length; s > o; o++)i += this._renderMenuOne(t[o])
            } else i = this._renderMenuOne(t);
            return n && e(n).html(i), i
        },
        _initDomEvent: function () {
            this.dom.undelegate();
            var t = this, n = (e(this.dom), function (n) {
                var i = (new Date).getTime();
                if (t.onMouseEnter(), "dropdown" === t.type) {
                    t.onBeforeOpen() !== !1 && t.dom.addClass("button-open"), "function" == typeof t.config.menu && t.config.menu(t.dom.menu, function (n) {
                        t._renderMenuList(n, t.dom.menu), t.config.resize === !0 && t.resizeButtonWidth()
                    });
                    var o = e(n.currentTarget);
                    if (o.length && o.parent().hasClass("g-dropdown-button-second")) {
                        var s = o.attr("data-button-id"), u = d._secondMenuCallbacks[s], h = o.parent().find(".menu");
                        o.parent().addClass("button-open"), "function" == typeof u && u(h, function (n) {
                            t._renderMenuList(n, h), t.config.resize === !0 && t.resizeButtonWidth()
                        })
                    }
                    e(this).hasClass("g-button-hastips") && e(".g-button-tips").css({visibility: "visible"});
                    var r = (new Date).getTime() - i;
                    a.send({name: "buttonHover", value: r})
                }
            }), i = function (n) {
                t.onMouseLeave(), e(this).hasClass("g-button-hastips") && e(".g-button-tips").css({visibility: "hidden"});
                var i = n.currentTarget;
                t.menuHideTimeout = setTimeout(function () {
                    var t = e(i), n = t.parent().attr("menuLevel");
                    t.length && t.parent().hasClass("g-dropdown-button-second") && 2 === +n && t.parent().removeClass("button-open")
                }, 100)
            }, o = function () {
                t.isEnable && t.onClick()
            };
            this.dom.bind("mouseleave", function () {
                "dropdown" === t.type && t.onBeforeClose() !== !1 && t.dom.removeClass("button-open")
            }).bind("mouseenter", n).bind("mouseleave", i).bind("click", o).delegate(".g-button", "mouseenter", n).delegate(".g-button", "mouseleave", i).delegate(".g-button", "click", o).delegate(".g-button-menu", "click", function (n) {
                if (n.stopPropagation(), !e(this).hasClass("g-disabled")) {
                    var i = e(this).data("menu-id"), o = t.menu[i];
                    o && "function" == typeof o.click && o.click()
                }
            }).delegate("g-dropdown-button-second", "mouseleave", function () {
                "dropdown" === t.type && t.onBeforeClose() !== !1 && t.dom.removeClass("button-open")
            }).delegate(".menu", "mouseenter", function (n) {
                var i = e(n.currentTarget);
                i.length && i.parent().hasClass("g-dropdown-button-second") && t.menuHideTimeout && clearTimeout(t.menuHideTimeout)
            }).delegate(".menu", "mouseleave", function (t) {
                var n = e(t.currentTarget);
                n.length && n.parent().hasClass("g-dropdown-button-second") && n.parent().removeClass("button-open")
            })
        },
        _initUserEvent: function () {
            "function" == typeof this.config.click && (this.onClick = this.config.click), "function" == typeof this.config.mouseEnter && (this.onMouseEnter = this.config.mouseEnter), "function" == typeof this.config.mouseLeave && (this.onMouseLeave = this.config.mouseLeave), "function" == typeof this.config.beforeOpen && (this.onBeforeOpen = this.config.beforeOpen), "function" == typeof this.config.beforeClose && (this.onBeforeClose = this.config.beforeClose), "function" == typeof this.config.visibleChange && (this.onVisibleChange = this.config.visibleChange), "dropdown" !== this.type ? (this.onBeforeOpen = null, this.onBeforeClose = null) : this.onBeforeOpen = this.onBeforeClose = function () {
            }
        },
        _caulateClassName: function () {
            var t = "", n = this.config.color;
            return t = "big" === this.type ? n ? "g-button-" + n + "-large" : "g-button-large" : "middle" === this.type ? n ? "g-button-" + n + "-middle" : "g-button-middle" : n ? "g-button-" + n : ""
        },
        appendTo: function (t) {
            return t = e(t), t.append(this.dom), this.resizeButtonWidth(), this.container = t, this
        },
        resizeButtonWidth: function () {
            if ("dropdown" === this.type) {
                for (var t, n = this.dom.menu[0].children, i = 0, o = this.dom.outerWidth(), s = 0, a = n.length; a > s; s++)t = d.caculateDropButtonWidth(e(n[s]), this.config), i < t.width && (i = t.width), this.dom.menu.width(i - 2), this.width = i, this.height = t.height;
                t = d.caculateDropButtonWidth(null, this.config), i < t.width && (i = t.width), o > i && (i = o), this.dom.menu.width(i - 2), this.width = i, this.height = t.height
            } else {
                var t = d.caculataButtonWidth(this.config);
                this.width = t.width, this.height = t.height
            }
        },
        change: function (t, n) {
            if (this.config = e.extend(this.config, t), t.type && t.type !== this.type || n) {
                var i = this.dom;
                this.type = t.type, this._init(), i.after(this.dom).remove(), this.resizeButtonWidth(), i = null
            } else {
                this.dom.mainButton.attr("class", "g-button " + this._caulateClassName());
                var o = this.dom.mainButton.find(".icon");
                o.length && !this.config.icon ? o.remove() : 0 === o.length && this.config.icon ? this.dom.mainButton.prepend('<em class="icon ' + this.config.icon + '"></em>') : o.length && o.attr("class", "icon " + this.config.icon), this.dom.mainButton.find(".text").text(this.config.title), this._initSizeAndPosition()
            }
            return this
        },
        addToMenu: function (t, n) {
            if ("dropdown" === this.type) {
                "object" != typeof t || t.length || (t = [t]);
                var i = this._renderMenuList(t)
            }
            return 0 === n ? this.dom.menu.prepend(i) : this.dom.menu.append(i), this.config.resize === !0 && this.resizeButtonWidth(), this
        },
        triggerClick: function (t) {
            this.isEnable && this.onClick(t)
        },
        removeFromMenu: function (t) {
            var n = e(this.dom.menu.find(".g-button-menu")[t]), i = n.data("menu-id");
            return n.remove(), delete this.menu[i], this.config.resize === !0 && this.resizeButtonWidth(), this
        },
        getMenuDom: function (t) {
            return "dropdown" === this.type ? e(this.dom.menu.find(".g-button-menu")[t]) : null
        },
        menuShow: function (t, n) {
            if ("dropdown" === this.type) {
                var i = e(this.dom.menu.find(".g-button-menu")[t]);
                return n === !1 ? i.hide() : i.css("display", "block"), this.config.resize === !0 && this.resizeButtonWidth(), i
            }
            return null
        },
        menuDisable: function (t, n) {
            if ("dropdown" === this.type) {
                var i = e(this.dom.menu.find(".g-button-menu")[t]);
                return n === !1 ? i.removeClass("g-disabled") : i.addClass("g-disabled")
            }
            return null
        },
        hide: function () {
            return this.dom.hide(), this.isShow = !1, this
        },
        show: function () {
            return this.dom.css("display", "inline-block"), this.isShow = !0, this
        },
        disable: function (t) {
            return t === !1 ? (this.dom.removeClass("g-disabled"), this.isEnable = !0) : (this.dom.addClass("g-disabled"), this.isEnable = !1), this
        },
        onClick: function () {
        },
        onMouseEnter: function () {
        },
        onMouseLeave: function () {
        },
        onBeforeOpen: function () {
        },
        onBeforeClose: function () {
        },
        onVisibleChange: function () {
        }
    }, d.caculataButtonWidth = function (t) {
        var n = 2, i = t.title, e = t.icon, o = t.iconMarginRight, s = t.padding, a = t.textWidth;
        return n += a ? parseInt(a, 10) + 4 : 13 * i.length + 4, "string" == typeof e && (n += "undefined" != typeof o ? 20 + parseInt(o, 10) : 20), n += s ? parseInt(s[0], 10) + parseInt(s[1], 10) : 20, {
            width: n,
            height: 33
        }
    }, d.caculateDropButtonWidth = function (t, n) {
        var i = 2, e = n.title, o = n.icon, s = n.iconMarginRight, a = n.padding, d = n.textWidth,
            u = n.buttonDefaultConfig.paddingLeft, h = n.buttonDefaultConfig.paddingRight,
            r = n.buttonDefaultConfig.paddingHeight;
        return t ? "none" !== t.css("display") ? (i += t.hasClass("g-button-menu") && t.find(".g-dropdown-button-second").length > 0 ? 12 * t.find("a.g-button").text().length : 12 * t.text().length, i += a ? parseInt(a[0], 10) + parseInt(a[1], 10) : 24) : i = 0 : (i += d ? parseInt(d, 10) : 12 * e.length, "string" == typeof o && (i += "undefined" != typeof s ? 20 + parseInt(s, 10) : 24), i += a ? parseInt(a[0], 10) + parseInt(a[1], 10) : u && h ? u + h : 30), {
            width: i,
            height: r || 34
        }
    }, i.exports = d
});