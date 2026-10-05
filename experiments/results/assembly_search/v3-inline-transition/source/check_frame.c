/* AI-generated harness checking fields, reserved words, and adjacent frames. */
extern void init_frame(unsigned *frame, unsigned p, unsigned o, unsigned previous);
static unsigned frames[4][8];
static const unsigned expected1[6] = {37, 26, 37, 26, 0, 2};
static const unsigned expected2[6] = {5039, 728, 5039, 728, 0, 3};
unsigned smoke_main(void)
{
    for (unsigned i = 0; i < 4; ++i)
        for (unsigned j = 0; j < 8; ++j)
            frames[i][j] = 0x12345678;
    init_frame(frames[1], 37, 26, 2);
    init_frame(frames[2], 5039, 728, 3);
    for (unsigned i = 0; i < 6; ++i)
        if (frames[1][i] != expected1[i] || frames[2][i] != expected2[i])
            return 1;
    for (unsigned i = 0; i < 8; ++i)
        if (frames[0][i] != 0x12345678 || frames[3][i] != 0x12345678)
            return 2;
    for (unsigned i = 6; i < 8; ++i)
        if (frames[1][i] != 0x12345678 || frames[2][i] != 0x12345678)
            return 3;
    return 12;
}
