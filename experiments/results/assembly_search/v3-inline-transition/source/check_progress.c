/* AI-generated integration tests for action order and backtracking. */
typedef struct { unsigned *frame; unsigned depth; } observed;
extern unsigned advance_search(unsigned *, unsigned, unsigned, observed *);
static unsigned frames[3][8];
unsigned smoke_main(void)
{
    observed out;
    for (unsigned i = 0; i < 3; ++i) {
        frames[i][0] = 1;
        frames[i][1] = 0;
        frames[i][4] = 0;
    }
    for (unsigned move = 0; move < 9; ++move) {
        if (advance_search(frames[0], 0, 3, &out) != move ||
            frames[0][4] != move + 1 || out.frame != frames[0] || out.depth != 0)
            return 1;
    }
    if (advance_search(frames[0], 0, 3, &out) != 11 ||
        out.frame != frames[0] || out.depth != 0) return 2;
    frames[0][4] = 4;
    frames[1][4] = 9;
    if (advance_search(frames[1], 1, 3, &out) != 4 ||
        frames[0][4] != 5 || out.frame != frames[0] || out.depth != 0) return 3;
    frames[0][4] = frames[1][4] = frames[2][4] = 9;
    if (advance_search(frames[2], 2, 3, &out) != 11 ||
        out.frame != frames[0] || out.depth != 0) return 4;
    frames[0][4] = 6;
    if (advance_search(frames[1], 1, 1, &out) != 6 ||
        out.frame != frames[0] || out.depth != 0) return 5;
    frames[1][0] = frames[1][1] = 0;
    if (advance_search(frames[1], 1, 1, &out) != 10 ||
        out.frame != frames[1] || out.depth != 1) return 6;
    return 12;
}
