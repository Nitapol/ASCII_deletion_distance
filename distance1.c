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

void assert(int e) { if (e != 1) { printf("*** ERROR %d ***\n", e); exit(1); }}

#define LOOP 99999
#define LEN 5
#define FORMAT "%05d"
#define SIZE (LEN+1)

int main() {
    assert(MAXSIZE >= SIZE);
    assert(distance1("bat", "cat") == fee('b') + fee('c'));
    assert(distance1("!~!", "~!!") == 2 * fee('!'));
    clock_t start = clock();
    int n = 0, d = 0;
    char s[SIZE], a[SIZE];
    do {
        sprintf(s, FORMAT, n);
        for (int i = 0; i < SIZE; i++) {
            char c = s[i];
            s[i] = 0;
            strcpy(a, s);
            s[i] = c;
            char *b = s + i;
            int da = distance1(a, b);
            int db = distance1(b, a);
            assert(da == db);
            d += da;
        }
    } while (n++ < LOOP);
    n *= 2*SIZE;
    double t = (clock() - start) / (double) CLOCKS_PER_SEC;
    printf("%f,%d,%d,%f\n", t, d, n, t/n);
    return 0;
}
