var C, A = n(21), D = n(22), I = n(23), z = n(24), M = n(25), R = 0, N = 1, U = 3, F = 4, P = 5, $ = 0, L = 1, B = -2, H = -3, Y = -5, J = -1, W = 1, G = 2, X = 3, Z = 4, q = 0, V = 2, K = 8, Q = 9, tt = 15, et = 8, nt = 29, rt = 256, it = rt + 1 + nt, ot = 30, at = 19, st = 2 * it + 1, ut = 15, lt = 3, ct = 258, ft = ct + lt + 1, ht = 32, dt = 42, pt = 69, gt = 73, vt = 91, _t = 103, wt = 113, mt = 666, yt = 1, bt = 2, xt = 3, kt = 4, Tt = 3;

var window = {
    seed: {
        env: "pro"
    },
    innerWidth: 1920,
    innerHeight: 1080,
    location: {
        href: "https://epassport.meituan.com/account/unitivelogin?bg_source=3&service=waimai&platform=2&continue=http://e.waimai.meituan.com/v2/epassport/entry&left_bottom_link=%2Faccount%2Funitivesignup%3Fbg_source%3D3%26service%3Dwaimai%26platform%3D2%26continue%3Dhttp%3A%2F%2Fe.waimai.meituan.com%2Fv2%2Fepassport%2FsignUp%26extChannel%3Dwaimaie%26ext_sign_up_channel%3Dwaimaie&right_bottom_link=%2Faccount%2Funitiverecover%3Fbg_source%3D3%26service%3Dwaimai%26platform%3D2%26continue%3Dhttp%3A%2F%2Fe.waimai.meituan.com%2Fv2%2Fepassport%2FchangePwd"
    },
    Yoda: {},
    behavior: '',
    token: '',
    ts: new Date().getTime(),
    cts: new Date().getTime() + 1000,
    btoa: function (str) {
        var buffer;
        if (str instanceof Buffer) {
            buffer = str;
        } else {
            buffer = Buffer.from(str.toString(), 'binary');
        }
        return buffer.toString('base64');
    },
    point: function() {
        var trace = [];
        var k = Math.floor(15 * Math.random() + 5);
        for (var i = 1; i <= k; i++) {
            var F = Math.floor(Math.random() * ((400 + (i + 1) * 30) - (400 + i * 30 + 1))) + (400 + i * 30);
            var S = Math.floor(Math.random() * ((400 + (i + 1) * 30) - (400 + i * 30 + 1))) + (400 + i * 30);
            var T = Math.floor(Math.random() * ((400 + (i + 1) * 30) - (400 + i * 30 + 1))) + (400 + i * 30);
            var N = [0, F, S, T];
            trace.push(N);
        }
        return trace
    },
    paramsMT: function() {
        var at = [];
        var k = Math.floor(Math.random() * ((60 - 40) + 1)) + 40;
        var arr = ['BUTTON', 'INPUT', 'DIV'];
        for (var i = 1; i <= k; i++) {
            var t = setTimeout(function () {
                var page_x = Math.floor(Math.random() * ((1283 - 482) + 1)) + 482;
                var page_y = Math.floor(Math.random() * ((295 - 245) + 1)) + 245;
                var t = new Date().getTime() - window.ts;
                var s = arr[Math.floor((Math.random() * arr.length))];
                at.push(`${page_x}, ${page_y}, ${s}, ${t}`)
            }, 50);

            clearTimeout(t)
        }
        return at
    },
};

var document = {
    documentElement: {
        clientWidth: 800,
        clientHeight: 600
    },
    referrer: "http://e.waimai.meituan.com/logon"
};
var screen = {
    width: 1920,
    height: 1080,
    availWidth: 1858,
    availHeight: 1080,
    colorDepth: 24,
    pixelDepth: 24
};
var navigator = {};
var babelHelpers = {};

function behavior_f(e, t) {
    return behavior_b(behavior_r(e, t))
}
function behavior_r(e, t) {
    // e = behavior_i(e);
    // t = behavior_i(t);
    behavior_a(behavior_v(behavior_c(e, true), behavior_s(behavior_c(t, false))), false)
}
function behavior_i(e) {
    if (/^[\x00-\x7f]*$/.test(e))
        return e;
    for (var t = [], n = e.length, r = 0, i = 0; r < n; ++r, ++i) {
        var o = e.charCodeAt(r);
        if (o < 128)
            t[i] = e.charAt(r);
        else if (o < 2048)
            t[i] = String.fromCharCode(192 | o >> 6, 128 | o & 63);
        else if (o < 55296 || o > 57343)
            t[i] = String.fromCharCode(224 | o >> 12, 128 | o >> 6 & 63, 128 | o & 63);
        else if (r + d < n) {
            var a = e.charCodeAt(r + d);
            if (o < 56320 && 56320 <= a && a <= 57343) {
                var c = ((o & 1023) << 10 | a & 1023) + 65536;
                t[i] = String.fromCharCode(240 | c >> 18 & 63, 128 | c >> 12 & 63, 128 | c >> 6 & 63, 128 | c & 63);
                ++r;
                continue
            }
        }
    }
    return t.join("")
}
function behavior_a(e, t) {
    var n = e["length"]
      , r = n << 2;
    if (t) {
        var i = e[n - 1];
        if (r -= 4,
        i < r - 3 || i > r)
            return Sr;
        r = i
    }
    for (var o = 0; o < n; o++)
        e[o] = String["fromCharCode"](e[o] & 255, e[o] >>> 8 & 255, e[o] >>> 16 & 255, e[o] >>> 24 & 255);
    var a = e["join"]("");
    return t ? a["substring"](0, r) : a
}
function behavior_c(e, t) {
    var n = e.length
        , r = n >> 2;
    (n & 3) !== 0 && ++r;
    var i;
    t ? (i = new Array(r + 1),
        i[r] = n) : i = new Array(r);
    for (var o = 0; o < n; ++o)
        i[o >> 2] |= e.charCodeAt(o) << ((o & 3) << 3);
    return i
}
function behavior_s(e) {
    return e.length < 4 && (e.length = 4),
        e
}
function behavior_v(e, t) {
    var n, r, i, o, a, c, s = e["length"], u = s - 1;
    for (r = e[u],
    i = 0,
    c = Math.floor(6 + 52 / s) | 0; c > 0; --c) {
        for (i = i + 2654435769 & 4294967295,
        o = i >>> 2 & 3,
        a = 0; a < u; ++a)
            n = e[a + 1],
            r = e[a] = e[a] + ((r >>> 5 ^ n << 2) + (n >>> 3 ^ r << 4) ^ (i ^ n) + (t[a & 3 ^ o] ^ r)) & 4294967295;
        n = e[0],
        r = e[u] = e[u] + ((r >>>5 ^ n << 2) + (n >>> 3 ^ r << 4) ^ (i ^ n) + (t[u & 3 ^ o] ^ r)) & 4294967295
    }
    return e
}
function behavior_b (t) {
    var e = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/"]
    var n, r, i, o, a, c, s;
    for (r = i = 0, o = t.length, a = o % 3, o -= a, c = o / 3 << 2, a > 0 && (c += 4), n = new Array(c); r < o; )
        s = t.charCodeAt(r++) << 16 | t.charCodeAt(r++) << 8 | t.charCodeAt(r++), n[i++] = e[s >> 18] + e[s >> 12 & 63] + e[s >> 6 & 63] + e[s & 63];
    return a == 1 ? (s = t.charCodeAt(r++),
        n[i++] = e[s >> 2] + e[(s & 3) << 4] + "==") : a == 2 && (s = t.charCodeAt(r++) << 8 | t.charCodeAt(r++),
        n[i++] = e[s >> 10] + e[s >> 4 & 63] + e[(s & 15) << 2] + "="), n.join("")
}
function behavior_o(e) {
    for (var t = "/", n = "+", r = e.split(""), i = [], o = 0; o < r.length; o++) {
        var a = r[o];
        a === t && (a = "("),
        a === n && (a = ")"),
            i.push(a)
    }
    return i.reverse().join("")
}

function behavior_iii(e) {
    var t = window.btoa(e);
    return t.replace(/=/g, ")").replace(/\+/g, "(")
}
function ooo(t, e, n) {
    window.behavior = e.behavior;
    var i = [];
    for (var o in e)
        i.push(encodeURIComponent(o) + "=" + encodeURIComponent(e[o]));
    e = i.join("&");
    return aaa("POST", t, e)
}
function aaa(t, e, n) {
    var r = window.Yoda.Rohr.reload(e + "&" + n);
    window.token = r;
    return r
}
function input(e, t) {
    e.timestamp = new Date().getTime();
    var n = {};
    if (e.options && e.options.body && e.options.body.behavior) {
        var r = e.options.body.behavior;
        var a = e.options.body.request_code;
        var s = behavior_f(r, behavior_iii(a));
        e.options.body.behavior = behavior_o(s);
        n.Authorization = "Bearer " + a
    }
    if (e.uri) {
        var u = e.options || {};
        return ooo(e.uri, u.body, n)
    }
}

function get_params(request_code) {
    var behavior = {
        "env":{
            "zone": [230,33],
            "client": [286,172],
            "Timestamp": [window.ts, window.cts],
            "count": 1,
            "timeout": 0
        },
        "trajectory": [{"point": window.point()}]};

    var eee = {
        uri: "https://verify.meituan.com/v2/ext_api/merchantlogin/verify?id=71",
        type: "SLIDER/add-slider",
        options: {
            method: "post",
            body: {
                behavior: JSON.stringify(behavior),
                fingerprint: undefined,
                request_code: request_code
            }
        }
    };

    input(eee);

    console.log('token: ', window.btoa(window.token));
    console.log('token: ', window.token);
    console.log('behavior: ', window.behavior);

    return {
        token: window.token,
        behavior: window.behavior
    }
}

function Y_o(t) {
    for (var e = t.length; --e >= 0; )
        t[e] = 0
}

function token_y() {
    this.strm = null,
    this.status = 0,
    this.pending_buf = null,
    this.pending_buf_size = 0,
    this.pending_out = 0,
    this.pending = 0,
    this.wrap = 0,
    this.gzhead = null,
    this.gzindex = 0,
    this.method = 8,
    this.last_flush = -1,
    this.w_size = 0,
    this.w_bits = 0,
    this.w_mask = 0,
    this.window = null,
    this.window_size = 0,
    this.prev = null,
    this.head = null,
    this.ins_h = 0,
    this.hash_size = 0,
    this.hash_bits = 0,
    this.hash_mask = 0,
    this.hash_shift = 0,
    this.block_start = 0,
    this.match_length = 0,
    this.prev_match = 0,
    this.match_available = 0,
    this.strstart = 0,
    this.match_start = 0,
    this.lookahead = 0,
    this.prev_length = 0,
    this.max_chain_length = 0,
    this.max_lazy_match = 0,
    this.level = 0,
    this.strategy = 0,
    this.good_match = 0,
    this.nice_match = 0,
    this.dyn_ltree = new Uint16Array(2 * 573),
    this.dyn_dtree = new Uint16Array(2 * (2 * 30 + 1)),
    this.bl_tree = new Uint16Array(2 * (2 * 19 + 1)),
    Y_o(this.dyn_ltree),
    Y_o(this.dyn_dtree),
    Y_o(this.bl_tree),
    this.l_desc = null,
    this.d_desc = null,
    this.bl_desc = null,
    this.bl_count = new Uint16Array(15 + 1),
    this.heap = new Uint16Array(2 * 286 + 1),
    Y_o(this.heap),
    this.heap_len = 0,
    this.heap_max = 0,
    this.depth = new Uint16Array(2 * 286 + 1),
    Y_o(this.depth),
    this.l_buf = 0,
    this.lit_bufsize = 0,
    this.last_lit = 0,
    this.d_buf = 0,
    this.opt_len = 0,
    this.static_len = 0,
    this.matches = 0,
    this.insert = 0,
    this.bi_buf = 0,
    this.bi_valid = 0
}

function b(t) {
            var e;
            return t && t.state ? (t.total_in = t.total_out = 0,
                t.data_type = V,
                e = t.state,
                e.pending = 0,
                e.pending_out = 0,
            e.wrap < 0 && (e.wrap = -e.wrap),
                e.status = e.wrap ? dt : wt,
                t.adler = 2 === e.wrap ? 0 : 1,
                e.last_flush = R,
                D._tr_init(e),
                $) : r(t, B)
        }

function x(t) {
            var e = b(t);
            return e === $ && m(t.state),
                e
        }

function T(t, e, n, i, o, a) {
    if (!t)
        return B;
    var s = 1;
    if (e === J && (e = 6),
        i < 0 ? (s = 0,
            i = -i) : i > 15 && (s = 2,
            i -= 16),
    o < 1 || o > Q || n !== K || i < 8 || i > 15 || e < 0 || e > 9 || a < 0 || a > Z)
        return r(t, B);
    8 === i && (i = 9);
    var u = new token_y;
    return t.state = u,
        u.strm = t,
        u.wrap = s,
        u.gzhead = null,
        u.w_bits = i,
        u.w_size = 1 << u.w_bits,
        u.w_mask = u.w_size - 1,
        u.hash_bits = o + 7,
        u.hash_size = 1 << u.hash_bits,
        u.hash_mask = u.hash_size - 1,
        u.hash_shift = ~~((u.hash_bits + lt - 1) / lt),
        u.window = new A.Buf8(2 * u.w_size),
        u.head = new A.Buf16(u.hash_size),
        u.prev = new A.Buf16(u.w_size),
        u.lit_bufsize = 1 << o + 6,
        u.pending_buf_size = 4 * u.lit_bufsize,
        u.pending_buf = new A.Buf8(u.pending_buf_size),
        u.d_buf = 1 * u.lit_bufsize,
        u.l_buf = 3 * u.lit_bufsize,
        u.level = e,
        u.strategy = a,
        u.method = n,
        x(t)
}

function new_n() {
    this.input = null,
    this.next_in = 0,
    this.avail_in = 0,
    this.total_in = 0,
    this.output = null,
    this.next_out = 0,
    this.avail_out = 0,
    this.total_out = 0,
    this.msg = "",
    this.state = null,
    this.data_type = 2,
    this.adler = 0;
}

function reload_r(t) {
    if (!(this instanceof reload_r))
        return new reload_r(t);
    this.options = window.assign({
        level: w,
        method: y,
        chunkSize: 16384,
        windowBits: 15,
        memLevel: 8,
        strategy: m,
        to: ""
    }, t || {});
    var e = this.options;
    e.raw && e.windowBits > 0 ? e.windowBits = -e.windowBits : e.gzip && e.windowBits > 0 && e.windowBits < 16 && (e.windowBits += 16),
        this.err = 0,
        this.msg = "",
        this.ended = !1,
        this.chunks = [],
        this.strm = new new_n,
        this.strm.avail_out = 0;
    var n = s.deflateInit2(this.strm, e.level, e.method, e.windowBits, e.memLevel, e.strategy);
    if (n !== g)
        throw new Error(c[n]);
    if (e.header && s.deflateSetHeader(this.strm, e.header),
        e.dictionary) {
        var i;
        if (i = "string" == typeof e.dictionary ? l.string2buf(e.dictionary) : "[object ArrayBuffer]" === h.call(e.dictionary) ? new Uint8Array(e.dictionary) : e.dictionary,
            n = s.deflateSetDictionary(this.strm, i),
        n !== g)
            throw new Error(c[n]);
        this._dict_set = !0
    }
}

function reload_e(t, e) {
    var n = new reload_r(e);
    if (n.push(t, !0),
        n.err)
        throw n.msg || c[n.err];
    return n.result
}

function reload_c (t) {
    t = reload_e(JSON.stringify(t), { to: "string" });
    t = window.btoa(t);
    return t
}

function reload_f (t) {
    var e = [];
    var n = Object.keys(t).sort();
    n.forEach(function(n, r) {
        e.push(n + "=" + t[n])
    });
    e = e.join("&");
    return reload_c(e)
}

function reload (e) {
    var n;
    var o = {};
    o = i.parse(e.split("?")[1]);
    t.sign = reload_f(o);
    t.cts = Date.now();
    n = reload_c(t);
    r.LogVal && "undefined" != typeof window && (window[r.LogVal] = encodeURIComponent(n));
    return n
}

get_params('65594b8a37204283ac896da1448dfde7');
