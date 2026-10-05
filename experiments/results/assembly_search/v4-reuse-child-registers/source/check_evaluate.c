/* AI-generated integration harness using the actual projection distances. */
#include "../rv32_baseline/target.h"
extern unsigned evaluate_state(unsigned p, unsigned o,
                               const uint8_t *pd, const uint8_t *od,
                               unsigned g, unsigned bound);
static const unsigned ps[6] = {0, 1, 10, 1023, 5039, 720};
static const unsigned os[6] = {0, 728, 27, 512, 1, 364};
unsigned smoke_main(void)
{
    for (unsigned i = 0; i < 6; ++i) {
        unsigned h = rt_pd[ps[i]] > rt_od[os[i]] ? rt_pd[ps[i]] : rt_od[os[i]];
        for (unsigned g = 0; g <= 11; ++g)
            for (unsigned bound = 0; bound <= 11; ++bound)
                if (evaluate_state(ps[i], os[i], rt_pd, rt_od, g, bound) !=
                    (unsigned) (g + h > bound)) return 1;
    }
    return 12;
}
