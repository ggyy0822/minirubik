/* AI-generated harness using the generated real cube transition tables.
 * A two-word integer struct is returned in a0/a1 by the RV32 ABI.
 */
#include "../rv32_baseline/target.h"
typedef struct { unsigned p, o; } pair;
extern pair quarter_step(unsigned p, unsigned o,
                         const uint16_t *permutation, const uint16_t *orientation);
static const uint16_t *const pp[3] = {rt_perm[0], rt_perm[1], rt_perm[2]};
static const uint16_t *const oo[3] = {rt_orient[0], rt_orient[1], rt_orient[2]};
static const unsigned ps[4] = {0, 1, 1023, 5039};
static const unsigned os[4] = {0, 728, 255, 512};

unsigned smoke_main(void)
{
    for (unsigned face = 0; face < 3; ++face) {
        for (unsigned i = 0; i < 4; ++i) {
            pair next = quarter_step(ps[i], os[i], pp[face], oo[face]);
            if (next.p != pp[face][ps[i]] || next.o != oo[face][os[i]]) return 1;
        }
        pair state = {5039, 728};
        for (unsigned turn = 0; turn < 4; ++turn)
            state = quarter_step(state.p, state.o, pp[face], oo[face]);
        if (state.p != 5039 || state.o != 728) return 2;
    }
    return 12;
}
