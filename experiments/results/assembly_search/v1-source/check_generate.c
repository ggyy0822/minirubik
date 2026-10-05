/* AI-generated real-table tests of sequential child generation. */
#include "../rv32_baseline/target.h"
extern unsigned generate_action(unsigned *, unsigned, unsigned);
extern void init_frame(unsigned *, unsigned, unsigned, unsigned);
static const uint16_t *const pp[3] = {rt_perm[0], rt_perm[1], rt_perm[2]};
static const uint16_t *const oo[3] = {rt_orient[0], rt_orient[1], rt_orient[2]};
static const unsigned states[4][2] = {{1,0}, {0,1}, {5039,728}, {720,364}};
static const unsigned faces[9] = {0,0,0,1,1,1,2,2,2};
static const unsigned turns[9] = {1,2,3,1,2,3,1,2,3};
unsigned smoke_main(void)
{
    for (unsigned state = 0; state < 4; ++state)
        for (unsigned previous = 0; previous <= 3; ++previous) {
            unsigned frame[8];
            init_frame(frame, states[state][0], states[state][1], previous);
            for (unsigned move = 0; move < 9; ++move) {
                if (faces[move] == previous) continue;
                unsigned p = states[state][0], o = states[state][1];
                for (unsigned turn = 0; turn < turns[move]; ++turn) {
                    p = pp[faces[move]][p];
                    o = oo[faces[move]][o];
                }
                if (generate_action(frame, 0, 11) != move ||
                    frame[2] != p || frame[3] != o || frame[6] != move ||
                    frame[0] != states[state][0] || frame[1] != states[state][1])
                    return 1;
            }
            if (generate_action(frame, 0, 11) != 11) return 2;
        }
    return 12;
}
