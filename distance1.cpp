// Copyright (c) 2019 Alexander Lopatin. All rights reserved.
#include <iostream>
#include <sstream>
#include <iomanip>
#include <string>
using namespace std;

int fee(const char& c) { return c; }

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
        d = min(d, fee(a[i]) + distance1(skip_char(s, a, i), b));
    for (int i = 0; i < lb; i++)
        d = min(d, fee(b[i]) + distance1(a, skip_char(s, b, i)));
    return d;
}

#define LOOP 99999
#define LEN 5

int main() {
    assert(distance1("bat", "cat") == fee('b') + fee('c'));
    assert(distance1("!~!", "~!!") == 2 * fee('!'));
    clock_t start = clock();
    int n = 0, d = 0;
    do {
        stringstream ss;
        ss << std::setw(LEN) << std::setfill('0') << n;
        string s = ss.str();
        for (int i = 0; i < LEN+1; i++) {
            string a = s.substr(0, i);
            string b = s.substr(i);
            int da = distance1(a, b);
            int db = distance1(b, a);
            assert(da == db);
            d += da;
        }
    } while (n++ < LOOP);
    n *= 2*(LEN+1);
    double t = (clock() - start) / (double) CLOCKS_PER_SEC;
    cout << t << "," << d << "," << n << "," << t/n << endl;
    return 0;
}
