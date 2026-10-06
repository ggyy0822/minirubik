#include "target.h"

/* Explicit integer shift/add, not a compiler multiplication helper. */
static unsigned times_small(unsigned value, unsigned factor)
{
    unsigned result = 0;
    while (factor) {
        if (factor & 1) result += value;
        factor >>= 1;
        value <<= 1;
    }
    return result;
}

int target_parse(const char *input, uint8_t p[7], uint8_t o[7],
                 unsigned *prank, unsigned *orank)
{
    unsigned seen = 0, sum = 0;
    for (unsigned i = 0; i < 7; ++i) {
        if (input[i] < '1' || input[i] > '7') return 0;
        p[i] = (uint8_t) (input[i] - '1');
        unsigned bit = 1u << p[i];
        if (seen & bit) return 0;
        seen |= bit;
    }
    for (unsigned i = 0; i < 7; ++i) {
        if (input[i + 7] < '1' || input[i + 7] > '3') return 0;
        o[i] = (uint8_t) (input[i + 7] - '1');
        sum += o[i];
    }
    if (input[14]) return 0;
    while (sum >= 3) sum -= 3;
    if (sum) return 0;
    unsigned pr = 0, ori = 0;
    for (unsigned i = 0; i < 7; ++i) {
        unsigned smaller = 0;
        for (unsigned j = i + 1; j < 7; ++j)
            if (p[j] < p[i]) ++smaller;
        pr = times_small(pr, 7 - i) + smaller;
    }
    for (unsigned i = 0; i < 6; ++i) ori = (ori << 1) + ori + o[i];
    *prank = pr;
    *orank = ori;
    return 1;
}

/* Physical replay does not rely on the generated transition tables. */
int target_replay(uint8_t p[7], uint8_t o[7], const uint8_t path[11], int length)
{
    static const uint8_t source[3][7] = {
        {1,4,2,0,3,5,6}, {0,1,2,4,5,6,3}, {0,2,5,3,1,4,6}
    };
    static const uint8_t twist[3][7] = {
        {1,2,0,2,1,0,0}, {0,0,0,1,2,1,2}, {0,0,0,0,0,0,0}
    };
    static const uint8_t face_of[9] = {0,0,0,1,1,1,2,2,2};
    static const uint8_t turns[9] = {1,2,3,1,2,3,1,2,3};
    if (length < 0 || length > 11) return 0;
    for (int step = 0; step < length; ++step) {
        unsigned move = path[step];
        if (move >= 9) return 0;
        unsigned face = face_of[move];
        for (unsigned turn = 0; turn < turns[move]; ++turn) {
            uint8_t next_p[7], next_o[7];
            for (unsigned i = 0; i < 7; ++i) {
                unsigned from = source[face][i];
                next_p[i] = p[from];
                unsigned orientation = o[from] + twist[face][i];
                if (orientation >= 3) orientation -= 3;
                next_o[i] = (uint8_t) orientation;
            }
            for (unsigned i = 0; i < 7; ++i) {
                p[i] = next_p[i];
                o[i] = next_o[i];
            }
        }
    }
    for (unsigned i = 0; i < 7; ++i)
        if (p[i] != i || o[i]) return 0;
    return 1;
}
