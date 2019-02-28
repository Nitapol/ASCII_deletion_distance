// Copyright (c) 2019 Alexander Lopatin. All rights reserved.
#include <iostream>
#include <sstream>
#include <iomanip>
using namespace std;
#include <string>

int penalty(const char& character) { return character; }

string& skip_char(string &dst, const string &src, int skip) {
// Shorter "dst=src.substr(0,skip)+src.substr(skip+1);" but it will add 7 sec.
    dst.clear();
    for (int i = 0; i < src.size(); i++)
        if (i != skip)
            dst += src[i];
    return dst;
}

int distance1(const string &s1, const string &s2) {
    size_t l1 = s1.size();
    size_t l2 = s2.size();
    if (l1 == l2 && s1 == s2)
        return 0;
    int score = __INT_MAX__;
    string s;
    for (int i = 0; i < l1; i++)
        score = min(score, penalty(s1[i]) + distance1(skip_char(s, s1, i), s2));
    for (int i = 0; i < l2; i++)
        score = min(score, penalty(s2[i]) + distance1(s1, skip_char(s, s2, i)));
    return score;
}

#define LOOP 99999
#define LEN 5

int main() {
    assert(distance1("at", "cat") == penalty('c'));
    assert(distance1("bat", "cat") == penalty('b') + penalty('c'));
    assert(distance1("!~!", "~!!") == 2 * penalty('!'));
    assert(distance1("!!~", "!~!") == 2 * penalty('!'));
    clock_t start = clock();
    int n = 0, N = 0, total_score = 0;
    do {
        stringstream ss;
        ss << std::setw(LEN) << std::setfill('0') << n;
        string s = ss.str();
        for (int i = 0; i < LEN + 1; i++) {
            string s1 = s.substr(0, i);
            string s2 = s.substr(i);
            int score1 = distance1(s1, s2);
            int score2 = distance1(s2, s1);
            assert(score1 == score2);
            total_score += score1;
            N += 2;
         }
    } while (n++ < LOOP);
    double t = (clock() - start) / (double) CLOCKS_PER_SEC;
    cout << t << "," << total_score << "," << N << "," << t/N << endl;
    return 0;
}
