/* AI-generated reset/preservation checks, including integration with skips. */
typedef struct { unsigned *frame; unsigned depth, face; } observed;
extern unsigned prepare_action(unsigned *, unsigned, unsigned, observed *);
static const unsigned faces[9] = {0,0,0,1,1,1,2,2,2};
static const unsigned first[9] = {1,0,0,1,0,0,1,0,0};
unsigned smoke_main(void)
{
    observed out;
    for (unsigned previous = 0; previous <= 3; ++previous)
        for (unsigned start = 0; start <= 9; ++start) {
            unsigned frame[8] = {37,26,1111,222,start,previous,9999,777};
            unsigned expected = start;
            while (expected < 9 && faces[expected] == previous) ++expected;
            unsigned result = prepare_action(frame, 0, 3, &out);
            if (out.frame != frame || out.depth != 0 || frame[0] != 37 ||
                frame[1] != 26 || frame[5] != previous || frame[7] != 777) return 1;
            if (expected == 9) {
                if (result != 11 || frame[4] != 9 || frame[6] != 9999 ||
                    frame[2] != 1111 || frame[3] != 222) return 2;
            } else {
                if (result != expected || frame[4] != expected + 1 ||
                    out.face != faces[expected] || frame[6] != expected) return 3;
                if (frame[2] != (first[expected] ? 37u : 1111u) ||
                    frame[3] != (first[expected] ? 26u : 222u)) return 4;
            }
        }
    return 12;
}
