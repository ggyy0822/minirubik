/* AI-authored host verifier for the exact C sources compiled for the target. */
#define IDA_REFERENCE_LIBRARY
#include "../experiments/ida_reference.c"
#include "../baseline/target.h"

static int check_tables(void)
{
    if (!prepare()) return 0;
    if (memcmp(rt_perm, perm_next, sizeof perm_next) ||
        memcmp(rt_orient, orient_next, sizeof orient_next) ||
        memcmp(rt_pd, perm_distance, sizeof perm_distance) ||
        memcmp(rt_od, orient_distance, sizeof orient_distance)) return 0;
    for (unsigned face = 0; face < 3; ++face) {
        unsigned char seen[PERMUTATIONS] = {0};
        for (unsigned p = 0; p < PERMUTATIONS; ++p) {
            unsigned next = rt_perm[face][p];
            if (next >= PERMUTATIONS || seen[next]) return 0;
            seen[next] = 1;
        }
        memset(seen, 0, sizeof seen);
        for (unsigned o = 0; o < ORIENTATIONS; ++o) {
            unsigned next = rt_orient[face][o];
            if (next >= ORIENTATIONS || seen[next]) return 0;
            seen[next] = 1;
        }
        printf("transition face %u: full permutations; maxima p=5039 o=728; solved successors p=%u o=%u\n",
               face, rt_perm[face][0], rt_orient[face][0]);
    }
    unsigned pm = 0, om = 0;
    for (unsigned p = 0; p < PERMUTATIONS; ++p) {
        if (rt_pd[p] == UINT8_MAX) return 0;
        if (rt_pd[p] > pm) pm = rt_pd[p];
    }
    for (unsigned o = 0; o < ORIENTATIONS; ++o) {
        if (rt_od[o] == UINT8_MAX) return 0;
        if (rt_od[o] > om) om = rt_od[o];
    }
    if (rt_pd[0] || rt_od[0] || pm != 7 || om != 6) return 0;
    puts("H2: exported transitions/PDBs complete, match host generation; PDB maxima 7/6, solved entries 0.");
    return 1;
}

int main(int argc, char **argv)
{
    int all = argc == 2 && !strcmp(argv[1], "--all");
    int hard = argc == 2 && !strcmp(argv[1], "--hard");
    if (argc != 2 || (!all && !hard && strcmp(argv[1], "--check"))) return 2;
    if (!check_tables()) { fputs("table failure\n", stderr); return 1; }
    uint8_t *exact = oracle_distances();
    if (!exact) return 1;
    const char *samples[8] = {"12345671111111", "62345713133111", "24316572122213",
        "25713642221111", "24513763133333", "43752611332133", "25416373331111", "21345671111111"};
    uint32_t sample_ranks[17];
    for (unsigned i = 0; i < 8; ++i) {
        state_t state;
        if (!parse_state(samples[i], &state)) { free(exact); return 1; }
        sample_ranks[i] = rank_state(&state);
    }
    state_t solved = {{0,1,2,3,4,5,6}, {0}};
    for (uint8_t m = 0; m < 9; ++m) {
        state_t state = apply_move(solved, m);
        sample_ranks[m + 8] = rank_state(&state);
    }
    const char *invalid[] = {"", "123", "1234567111111", "123456711111111",
        "02345671111111", "82345671111111", "12345671111110", "12345671111114",
        "1234567111111a", "11345671111111", "12345671111112"};
    for (unsigned i = 0; i < sizeof invalid / sizeof *invalid; ++i) {
        uint8_t p[7], o[7]; unsigned pr, ori;
        if (target_parse(invalid[i], p, o, &pr, &ori)) { free(exact); return 1; }
    }
    struct timeval start, end;
    gettimeofday(&start, NULL);
    unsigned checked = 0;
    for (uint32_t rank = 0; rank < STATES; ++rank) {
        unsigned pindex = rank / ORIENTATIONS, oindex = rank % ORIENTATIONS;
        unsigned h = rt_pd[pindex] > rt_od[oindex] ? rt_pd[pindex] : rt_od[oindex];
        if (h > exact[rank]) { free(exact); return 1; }
        int selected = all || (hard && exact[rank] == 11);
        if (!hard && !all)
            for (unsigned i = 0; i < 17; ++i)
                if (rank == sample_ranks[i]) selected = 1;
        if (!selected) continue;
        state_t state;
        unrank_state(rank, &state);
        char input[15]; uint8_t p[7], o[7], path[11]; unsigned pr, ori;
        for (unsigned i = 0; i < 7; ++i) {
            input[i] = (char) ('1' + state.p[i]);
            input[i + 7] = (char) ('1' + state.o[i]);
        }
        input[14] = '\0';
        if (!target_parse(input, p, o, &pr, &ori) || pr != pindex || ori != oindex) {
            fprintf(stderr, "parse mismatch at rank %u\n", rank); free(exact); return 1;
        }
        int length = target_search(pr, ori, path);
        if (length != exact[rank] || !target_replay(p, o, path, length)) {
            fprintf(stderr, "search/replay mismatch at rank %u\n", rank); free(exact); return 1;
        }
        for (int i = 0; i < length; ++i) state = apply_move(state, path[i]);
        if (rank_state(&state)) { free(exact); return 1; }
        ++checked;
        if (all && checked % 10000 == 0) {
            fprintf(stderr, "checked %u/%d\n", checked, STATES); fflush(stderr);
        }
    }
    gettimeofday(&end, NULL);
    printf("H1: all %d states passed.\n", STATES);
    printf("Search/parse/dual replay: %u states passed; wall seconds %.3f\n", checked,
           end.tv_sec - start.tv_sec + (end.tv_usec - start.tv_usec) / 1e6);
    puts(all ? "H3: full domain passed for shared target C sources (native build)." :
         "Full-domain H3 search not run by this invocation.");
    free(exact);
    return output_failed();
}
