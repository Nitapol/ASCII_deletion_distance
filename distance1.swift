//  Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import Foundation

func fee(_ c: Character) -> Int {
    var i = 255
    if let v = c.unicodeScalars.first?.value {
        i = Int(v)
        if i < 0 || i > 255 {
            i = 255
        }
    }
    return i
}

// Algorithm #1: Brute force.
func distance1a(_ a: inout [UInt8], _ b: inout [UInt8]) -> Int {
    if a == b {
        return 0
    }
    var d = Int.max
    for i in a.indices {
        let n = a.remove(at: i)
        d = min(d, Int(n) + distance1a(&a , &b))
        a.insert(n, at: i)
    }
    for i in b.indices {
        let n = b.remove(at: i)
        d = min(d, Int(n) + distance1a(&a , &b))
        b.insert(n, at: i)
    }
    return d
}

extension String {
    func byteArray() -> [UInt8] {
        var a = [UInt8]()
        for c in self.unicodeScalars {
            a.append(c.value < UInt8.max ? UInt8(c.value) :UInt8.max)
        }
        return a
    }
}

func distance1(_ a: String, _ b: String) -> Int {
    var aA = a.byteArray()
    var bA = b.byteArray()
    return distance1a(&aA, &bA)
}

assert(distance1("at", "cat") == fee("c"))
assert(distance1("cool", "cold") == fee("o") + fee("d"))
assert(distance1("!~!", "~!!") == 2 * fee("!")) // ! vs ~ (33 vs 126)

let date = Date()
var d = 0
var n = 0
while n < 100000 {

    func test(_ a: String, _ b: String) {
        let da = distance1(a, b)
        let db = distance1(b, a)
        d += da
        assert(da == db)
    }

    let s = String(format: "%05d", n)
    test("", s)
    for i in s.indices {
        test(String(s[...i]), String(s[s.index(after: i)...]))
    }
    n += 1
}
n *= 12
let t = Date().timeIntervalSince(date as Date)
print("\(t),\(d),\(n),\(t.magnitude/Double(n))")
