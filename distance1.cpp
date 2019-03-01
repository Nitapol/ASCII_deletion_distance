// Copyright (c) 2019 Alexander Lopatin. All rights reserved.
#include <iostream>
#include <sstream>
#include <iomanip>
using namespace std;
#include <string>

int penalty(const char& c) { return c; }

string& skip_char(string &dst, const string &src, int skip) {
    dst.clear();
    for (int i = 0; i < src.size(); i++)
        if (i != skip)
            dst += src[i];
    return dst;
}

int distance1(const string &a, const string &b) {
    size_t la = a.size();
    size_t lb = b.size();
    if (la == lb && a == b)
        return 0;
    int d = __INT_MAX__;
    string s;
    for (int i = 0; i < la; i++)
        d = min(d, penalty(a[i]) + distance1(skip_char(s, a, i), b));
    for (int i = 0; i < lb; i++)
        d = min(d, penalty(b[i]) + distance1(a, skip_char(s, b, i)));
    return d;
}

#define LOOP 99999
#define LEN 5

int main() {
    assert(distance1("at", "cat") == penalty('c'));
    assert(distance1("bat", "cat") == penalty('b') + penalty('c'));
    assert(distance1("!~!", "~!!") == 2 * penalty('!'));
    assert(distance1("!!~", "!~!") == 2 * penalty('!'));
    clock_t start = clock();
    int n = 0, N = 0, d = 0;
    do {
        stringstream ss;
        ss << std::setw(LEN) << std::setfill('0') << n;
        string s = ss.str();
        for (int i = 0; i < LEN + 1; i++) {
            string a = s.substr(0, i);
            string b = s.substr(i);
            int d1 = distance1(a, b);
            int d2 = distance1(b, a);
            assert(d1 == d2);
            d += d1;
            N += 2;
         }
    } while (n++ < LOOP);
    double t = (clock() - start) / (double) CLOCKS_PER_SEC;
    cout << t << "," << d << "," << N << "," << t/N << endl;
    return 0;
}
