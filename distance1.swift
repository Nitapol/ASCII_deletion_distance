//  Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import Foundation

func fee(_ c:Character)->Int {return Int(c.unicodeScalars.first?.value ?? 255)}

// Algorithm #1: Brute force.
func distance1(_ a: String, _ b: String) -> Int {
    if a == b {
        return 0
    }
    var d = Int.max
    for i in a.indices {
        d=min(d,fee(a[i])+distance1(String(a[..<i]+a[a.index(after:i)...]),b))
    }
    for i in b.indices {
        d=min(d,fee(b[i])+distance1(a,String(b[..<i]+b[b.index(after:i)...])))
    }
    return d
}

assert(distance1("cool", "cold") == fee("o") + fee("d"))
assert(distance1("!~!", "~!!") == 2 * fee("!")) // ! vs ~ (33 vs 126)

let date = Date()
var d = 0
var n = 0
while n <= 100000 {

    func test(_ a: String, _ b: String) {
        let da = distance1(a, b)
        let db = distance1(b, a)
        d += da
        assert(da == db)
    }

    var s = String(format: "%05d", n)
    test("", s)
    for i in s.indices {
        test(String(s[...i]), String(s[s.index(after: i)...]))
    }
    n += 1
}
let t = Date().timeIntervalSince(date as Date)
print("\(t),\(d),\(N),\(t.magnitude/Double(N))")
