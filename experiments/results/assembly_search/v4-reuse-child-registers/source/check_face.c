/* AI-generated tests for the integrated student search fragments. */
typedef struct { unsigned *frame; unsigned depth, face; } observed;
extern unsigned select_action(unsigned *, unsigned, unsigned, observed *);
extern void init_frame(unsigned *, unsigned, unsigned, unsigned);
static const unsigned faces[9] = {0,0,0,1,1,1,2,2,2};
unsigned smoke_main(void)
{
    unsigned frame[8];
    observed out;
    for (unsigned previous = 0; previous <= 3; ++previous)
        for (unsigned start = 0; start <= 9; ++start) {
            init_frame(frame, 1, 0, previous);
            frame[4] = start;
            unsigned expected = start;
            while (expected < 9 && faces[expected] == previous) ++expected;
            unsigned result = select_action(frame, 0, 3, &out);
            if (out.frame != frame || out.depth != 0) return 1;
            if (expected == 9) {
                if (result != 11 || frame[4] != 9) return 2;
            } else {
                if (result != expected || frame[4] != expected + 1 ||
                    out.face != faces[expected]) return 3;
            }
        }
    return 12;
}
