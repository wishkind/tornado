import base64
import execjs





def c(e, t):
    n = len(e)
    r = n >> 2
    if t:
        r = r + 2
    i = [0 * i for i in range(r)]
    for o in range(n):
        i[o >> 2] |= ord(e[o]) << ((o & 3) << 3)
    if t:
        i[-1] = n
    return i


def base_(a):
    return base64.b64encode(a.encode()).decode().replace('=', ")").replace("+", "(")


ctx = execjs.compile("""
 function f(e, t) {
            return b(r(e, t))
        }
   function r(e, t) {
   return  a(v(c(e, true), s(c(t, false))))

        }
       function s(e) {
            return e["length"] < 4 && (e["length"] = 4),
            e
        }
 function c(e, t) {
            var n = e["length"]
              , r = n >> 2;
            (n & 3) !== 0 && ++r;
            var i;
            t ? (i = new Array(r + 1),
            i[r] = n) : i = new Array(r);
            for (var o = 0; o < n; ++o)
                i[o >> 2] |= e["charCodeAt"](o) << ((o & 3) << 3);
            return i
        }


function v(e, t) {
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

function a(e, t) {
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
var b = function() {
            var e = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/"];
            return function(t) {
                var n, r, i, o, a, c, s;
                for (r = i = 0,
                o = t["length"],
                a = o % 3,
                o -= a,
                c = o / 3 << 2,
                a > 0&& (c += 4),
                n = new Array(c); r < o; )
                    s = t["charCodeAt"](r++) << 16 | t["charCodeAt"](r++) << 8 | t["charCodeAt"](r++),
                    n[i++] = e[s >> 18] + e[s >> 12 & 63] + e[s >> 6 & 63] + e[s & 63];
                return a == 1 ? (s = t["charCodeAt"](r++),
                n[i++] = e[s >> 2] + e[(s & 3) << 4] + "==") : a == 2 && (s = t["charCodeAt"](r++) << 8 | t["charCodeAt"](r++),
                n[i++] = e[s >> 10] + e[s >> 4 & 63] + e[(s & 15) << 2] + "="),
                n["join"]("")
            }
        }()
 function o(e) {
            for (var t = "/", n = "+", r = e["split"](""), i = [], o = 0; o < r["length"]; o++) {
                var a = r[o];
                a === "/" && (a = "("),
                a === n && (a = ")"),
                i["push"](a)
            }
            return i["reverse"]()["join"]("")
        }


""")
