/* AI-authored host-only test manifest generator; never linked into target. */
#define IDA_REFERENCE_LIBRARY
#include "../ida_reference.c"
int main(void) {
    if (!prepare()) return 1;
    uint8_t *exact = oracle_distances();
    if (!exact) return 1;
    puts("state,rank,expected_length,generated,expanded");
    unsigned count = 0;
    for (uint32_t rank = 0; rank < STATES; ++rank) {
        if (exact[rank] != 11) continue;
        state_t state; unrank_state(rank, &state);
        result_t result = search(rank);
        if (!verify_path(state, &result, 11)) { free(exact); return 1; }
        char input[15];
        for (unsigned i=0; i<7; ++i) {
            input[i] = '1' + state.p[i]; input[i+7] = '1' + state.o[i];
        }
        input[14]=0;
        printf("%s,%u,11,%" PRIu64 ",%" PRIu64 "\n", input, rank, result.generated, result.expanded);
        ++count;
    }
    free(exact);
    if (count != 2644) return 1;
    return output_failed();
}
