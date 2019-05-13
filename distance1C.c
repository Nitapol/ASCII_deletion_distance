#include <string.h> // strlen, strcmp, strcpy


extern "C" int add_one(int i)
{
    return i+1;
}

#define MAXSIZE 6
#define min(a,b) ({__typeof__(a) _a=(a); __typeof__(b) _b=(b); _a<_b ? _a:_b; })

static inline int fee(char c) { return c; }

inline char* skip_char(char *dst, const char *src, int skip) {
    int i = 0, j = 0; char c;
    while((c = src[i]) != 0)
        if (i++ != skip)
            dst[j++] = c;
    dst[j] = 0;
    return dst;
}

extern "C" int distance1C(const char *a, const char *b) {
    size_t l1 = strlen(a), l2 = strlen(b);
    if (l1 == l2 && strcmp(a, b) == 0)
        return 0;
    int d = __INT_MAX__; char s[MAXSIZE];
    for (int i = 0; i < l1; i++)
        d = min(d, fee(a[i]) + distance1C(skip_char(s,a,i), b));
    for (int i = 0; i < l2; i++)
        d = min(d, fee(b[i]) + distance1C(a, skip_char(s,b,i)));
    return d;
}

extern "C" int distance8C(const char *a, const char *b) {
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
    return z[la][lb];
}
