//  Copyright (c) 2019 Alexander Lopatin. All rights reserved.
#include <stdio.h> // printf, sprintf
#include <stdlib.h> // exit
#include <string.h> // strlen, strcmp, strcpy
#include <time.h> // clock_t, clock(), CLOCKS_PER_SEC
#define MAXSIZE 6
#define min(a,b) ({__typeof__(a) _a=(a); __typeof__(b) _b=(b); _a<_b ? _a:_b; })

inline int penalty(char c) { return c; }

char* skip_char(char *dst, const char *src, int skip) {
    int i = 0, j = 0;
    char c;
    while((c = src[i]) != 0)
        if (i++ != skip)
            dst[j++] = c;
    dst[j] = 0;
    return dst;
}

int distance1(const char *s1, const char *s2) {
    char s[MAXSIZE+MAXSIZE];
    size_t l1 = strlen(s1);
    size_t l2 = strlen(s2);
    if (l1 == l2 && strcmp(s1, s2) == 0)
        return 0;
    int score = __INT_MAX__, i;
    for (i = 0; i < l1; i++)
        score = min(score, penalty(s1[i]) + distance1(skip_char(s,s1,i),s2));
    for (i = 0; i < l2; i++)
        score = min(score, penalty(s2[i]) + distance1(s1,skip_char(s,s2,i)));
    return score;
}

void assert(int e) { if (e != 1) { printf("*** ERROR %d ***\n", e); exit(1); }}

#define LOOP 99999
#define LEN 5
#define FORMAT "%05d"
#define SIZE LEN+1

int main() {
    assert(MAXSIZE >= SIZE);
    assert(distance1("at", "cat") == penalty('c'));
    assert(distance1("bat", "cat") == penalty('b') + penalty('c'));
    assert(distance1("!~!", "~!!") == 2 * penalty('!'));
    assert(distance1("!!~", "!~!") == 2 * penalty('!'));
    clock_t start = clock();
    int n = 0, N = 0, total_score = 0, score1, score2, i;
    char s[SIZE], s1[SIZE], *s2, c;
    do {
        sprintf(s, FORMAT, n);
        for (i = 0; i < SIZE; i++) {
            c = s[i];
            s[i] = 0;
            strcpy(s1, s);
            s[i] = c;
            s2 = s + i;
            score1 = distance1(s1, s2);
            score2 = distance1(s2, s1);
            assert(score1 == score2);
            total_score += score1;
            N += 2;
        }
    } while (n++ < LOOP);
    double t = (clock() - start) / (double) CLOCKS_PER_SEC;
    printf("%f,%d,%d,%f\n", t, total_score, N, t/N);
    return 0;
}
