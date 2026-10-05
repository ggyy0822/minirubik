/* AI-generated harness using the real cube transition tables. */
#include "../rv32_baseline/target.h"
typedef struct { unsigned p, o; } pair;
extern pair half_step(unsigned p, unsigned o,
                      const uint16_t *permutation, const uint16_t *orientation);
static const uint16_t *const pp[3] = {rt_perm[0], rt_perm[1], rt_perm[2]};
static const uint16_t *const oo[3] = {rt_orient[0], rt_orient[1], rt_orient[2]};
static const unsigned ps[4] = {0, 1, 1023, 5039};
static const unsigned os[4] = {0, 728, 255, 512};
unsigned smoke_main(void)
{
    for (unsigned face = 0; face < 3; ++face) {
        for (unsigned i = 0; i < 4; ++i) {
            pair next = half_step(ps[i], os[i], pp[face], oo[face]);
            unsigned ep = pp[face][pp[face][ps[i]]];
            unsigned eo = oo[face][oo[face][os[i]]];
            if (next.p != ep || next.o != eo) return 1;
        }
        pair state = half_step(5039, 728, pp[face], oo[face]);
        state = half_step(state.p, state.o, pp[face], oo[face]);
        if (state.p != 5039 || state.o != 728) return 2;
    }
    return 12;
}
