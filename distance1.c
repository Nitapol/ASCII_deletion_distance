//  Copyright (c) 2019 Alexander Lopatin. All rights reserved.
#include <stdio.h> // printf, sprintf
#include <stdlib.h> // exit
#include <string.h> // strlen, strcmp, strcpy
#include <time.h> // clock_t, clock(), CLOCKS_PER_SEC
#define MAXSIZE 6
#define min(a,b) ({__typeof__(a) _a=(a); __typeof__(b) _b=(b); _a<_b ? _a:_b; })

inline int fee(char c) { return c; }

inline char* skip_char(char *dst, const char *src, int skip) {
    int i = 0, j = 0; char c;
    while((c = src[i]) != 0)
        if (i++ != skip)
            dst[j++] = c;
    dst[j] = 0;
    return dst;
}

int distance1(const char *a, const char *b) {
    size_t l1 = strlen(a), l2 = strlen(b);
    if (l1 == l2 && strcmp(a, b) == 0)
        return 0;
    int d = __INT_MAX__; char s[MAXSIZE];
    for (int i = 0; i < l1; i++)
        d = min(d, fee(a[i]) + distance1(skip_char(s,a,i), b));
    for (int i = 0; i < l2; i++)
        d = min(d, fee(b[i]) + distance1(a, skip_char(s,b,i)));
    return d;
}

int distance8(const char *a, const char *b) {
    size_t la = strlen(a), lb = strlen(b);
    if (la == lb && strcmp(a, b) == 0)
        return 0;
    int x[la];
    int y[lb];
    int z[la+1][lb+1];
    for (int i = 0; i <= la; i++) {
        for (int j = 0; j <= lb; j++) {
            z[i][j] = 0;
        }
    }
    for (int i = 0; i < la; i++)
        x[i] = fee(a[i]);
    for (int j = 0; j < lb; j++)
        y[j] = fee(b[j]);
    for (int i = 0; i < la; i++) {
        z[i+1][0] = z[i][0] + x[i];
    }
    for (int j = 0; j < lb; j++) {
        z[0][j+1] = z[0][j] + y[j];
    }
    for (int i = 0; i < la; i++) {
        for (int j = 0; j < lb; j++) {
            if (x[i] == y[j]) {
                z[i+1][j+1] = z[i][j];
            } else {
                int m = min(z[i][j] + x[i] + y[j], z[i][j+1] + x[i]);
                z[i+1][j+1] = min(m, z[i+1][j] + y[j]);
            }
        }
    }
//    for (int i = 0; i <= la; i++) {
//        for (int j = 0; j <= lb; j++) {
//            printf("%d ", z[i][j]);
//        }
//        printf("\n");
//    }
//    printf("\n%ld %ld\n", la, lb);
    return z[la][lb];
}


1
void assert_1(const char *a, const char *b, const char *c) {
    int r = 0;
    for (int i = 0; c[i]; i++)
        r += c[i];
    int t = distance8(a, b);
    if (t != r) {
        printf("*** ERROR #1 '%s' '%s' %d != %d\n", a, b, r, t);
        exit(1);
    }
}

int assert_2(const char *a, const char *b) {
    int r = distance8(a, b);
    int t = distance8(b, a);
    if (t != r) {
        printf("*** ERROR #2 '%s' '%s' %d != %d\n", a, b, r, t);
        exit(1);
    }
    return r;
}

#define LOOP 99999
#define LEN 5
#define FORMAT "%05d"
#define SIZE (LEN+1)

int main() {
    if (MAXSIZE < SIZE) {
        printf("*** ERROR: increase MAXSIZE\n");
        exit(1);
    }
    assert_1("A", "", "A");
    assert_1("!", "~", "!~");
    assert_1("!!", "!!!", "!");
    assert_1("!!!", "!!", "!");
    assert_1("", "z", "z");
    assert_1("ooz", "zoo", "zz");
    assert_1("at", "hat", "h");
    assert_1("cat", "rat", "cr");
    assert_1("bat", "cat", "bc");
    assert_1("cool", "cold", "od");
    assert_1("!~!", "~!!", "!!");
    assert_1("~!!!", "!!!~", "!!!!!!");
    assert_1("AB", "xy", "ABxy");
    int d, n;
    clock_t start = clock();
    for (int loop = 0; loop < 100; loop++) {
        n = 0; d = 0;
        char s[SIZE], a[SIZE];
        do {
            sprintf(s, FORMAT, n);
            for (int i = 0; i < SIZE; i++) {
                char c = s[i];
                s[i] = 0;
                strcpy(a, s);
                s[i] = c;
                char *b = s + i;
                d += assert_2(a, b);
            }
        } while (n++ < LOOP);
        n *= 2*SIZE;

    }
    double t = (clock() - start) / (double) CLOCKS_PER_SEC;
    printf("%f,%d,%d,%f\n", t, d, n, t/n);
    return 0;
}
