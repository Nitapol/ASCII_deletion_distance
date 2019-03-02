// Copyright © 2019 Alexander Lopatin. All rights reserved.

#import <Foundation/Foundation.h>

int fee(const char c) { return c; }

NSString *skip_char(NSString *a, int skip) {
    NSString *b = [a substringFromIndex:skip+1];
    return [[a substringToIndex:skip] stringByAppendingString:b];
}

int distance1(NSString *a, NSString *b) {
    NSUInteger la = a.length;
    NSUInteger lb = b.length;
    if (la == lb && [a isEqualToString:b])
        return 0;
    int d = __INT_MAX__;
    for (int i = 0; i < la; i++) {
        d = MIN(d, fee([a characterAtIndex:i]) + distance1(skip_char(a, i), b));
    }
    for (int i = 0; i < lb; i++) {
        d = MIN(d, fee([b characterAtIndex:i]) + distance1(a, skip_char(b, i)));
    }
    return d;
}

#define LOOP 99999
#define LEN 5
#define FORMAT "%05d"
#define SIZE (LEN+1)

int mainObjC () {
    @autoreleasepool {
        NSLog(@"Running in Objective-C mode...(use no arguments for C mode)\n");
        assert(distance1(@"cool", @"cold") == fee('o') + fee('d'));
        assert(distance1(@"!~!", @"~!!") == 2 * fee('!'));
        clock_t start = clock();
        int n = 0, d = 0;
        do {
            NSString *s = [NSString stringWithFormat:@FORMAT, n];
            for (int i = 0; i < SIZE; i++) {
                NSString *a = [s substringToIndex:i];
                NSString *b = [s substringFromIndex:i];
                int d1 = distance1(a, b);
                int d2 = distance1(b, a);
                assert(d1 == d2);
                d += d1;
            }
        } while (n++ < LOOP);
        n *= 2*SIZE;
        double t = (clock() - start) / (double) CLOCKS_PER_SEC;
        NSLog(@"%e,%d,%d,%e\n", t, d, n, t/n);
    }
    return 0;
}

// Just plain C will also work in Objective-C
#define MAXSIZE 6
#define min(a,b) ({__typeof__(a) _a=(a); __typeof__(b) _b=(b); _a<_b ? _a:_b; })

char* skip_charC(char *dst, const char *src, int skip) {
    int i = 0, j = 0;
    char c;
    while((c = src[i]) != 0)
        if (i++ != skip)
            dst[j++] = c;
    dst[j] = 0;
    return dst;
}

int distance1C(const char *s1, const char *s2) {
    char s[MAXSIZE+MAXSIZE];
    size_t l1 = strlen(s1);
    size_t l2 = strlen(s2);
    if (l1 == l2 && strcmp(s1, s2) == 0)
        return 0;
    int score = __INT_MAX__, i;
    for (i = 0; i < l1; i++)
        score = min(score, fee(s1[i]) + distance1C(skip_charC(s,s1,i),s2));
    for (i = 0; i < l2; i++)
        score = min(score, fee(s2[i]) + distance1C(s1,skip_charC(s,s2,i)));
    return score;
}

void assert1(int e) { if (e != 1) { printf("*** ERROR %d ***\n", e); exit(1); }}

int mainOldC() {
    printf("Running in C mode ... (enter any argument for Objective-C\n");
    assert1(MAXSIZE >= SIZE);
    assert1(distance1C("bat", "cat") == fee('b') + fee('c'));
    assert1(distance1C("!~!", "~!!") == 2 * fee('!'));
    clock_t start = clock();
    int n = 0, total_score = 0, score1, score2, i;
    char s[SIZE], s1[SIZE], *s2, c;
    do {
        sprintf(s, FORMAT, n);
        for (i = 0; i < SIZE; i++) {
            c = s[i];
            s[i] = 0;
            strcpy(s1, s);
            s[i] = c;
            s2 = s + i;
            score1 = distance1C(s1, s2);
            score2 = distance1C(s2, s1);
            assert(score1 == score2);
            total_score += score1;
        }
    } while (n++ < LOOP);
    n *= 2*SIZE;
    double t = (clock() - start) / (double) CLOCKS_PER_SEC;
    printf("%f,%d,%d,%f\n", t, total_score, n, t/n);
    return 0;
}

int main(int argc, const char * argv[]) {
    return argc > 1 ? mainObjC() : mainOldC();
}
