//  Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import Foundation

func penalty(_ c: Character) -> Int {
    var ascii = 255
    if c.unicodeScalars.first?.isASCII == true {
        if let v = c.unicodeScalars.first?.value {
            let i = Int(Int32(bitPattern: v))
            if i > 0 && i < 255 {
                ascii = i
            }
        }
    }
    return ascii
}

// Algorithm #1: Brute force.
func distance1(_ a: String, _ b: String) -> Int {
    if a == b {
        return 0
    }
    var d = Int.max
    for i in a.indices {
        d = min(d, penalty(a[i]) + distance1(
            String(a[..<i] + a[a.index(after: i)...]), b))
    }
    for i in b.indices {
        d = min(d, penalty(b[i]) + distance1(
            a, String(b[..<i] + b[b.index(after: i)...])))
    }
    return d
}

assert(distance1("at", "cat") == penalty("c"))
assert(distance1("bat", "cat") == penalty("b") + penalty("c"))
assert(distance1("!~!", "~!!") == 2 * penalty("!")) // ! vs ~ (33 vs 126)
assert(distance1("!!~", "!~!") == 2 * penalty("!"))

var n = 0
var N = 0
var total_score = 0
let date = Date()
while n <= 99999 {
    var s = String(n)
    while s.count < 5 {
        s = "0" + s
    }
    func test(_ a: String, _ b: String) {
        let score1 = distance1(a, b)
        let score2 = distance1(b, a)
        total_score += score1
        assert(score1 == score2)
        N += 2
        // print(score1, a, b)
    }
    test("", s)
    for i in s.indices {
        test(String(s[...i]), String(s[s.index(after: i)...]))
    }
    n += 1
}
let t = Date().timeIntervalSince(date as Date)
print("\(t),\(total_score),\(N),\(t.magnitude / Double(N))")
