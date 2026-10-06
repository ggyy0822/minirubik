/* AI-assisted educational C experiment, not a hand-written submission.
 * Host table generation and validation reuse the unchanged upstream model.
 * Search uses an explicit bounded stack; no recursion or allocation in search.
 * Native node counts are NOT Ripes retired instruction measurements.
 */
#define main upstream_solver_main
#include "../solver.c"
#undef main
#include <inttypes.h>
#include <time.h>
#include <sys/time.h>

static uint16_t perm_next[3][PERMUTATIONS];
static uint16_t orient_next[3][ORIENTATIONS];
static uint8_t perm_distance[PERMUTATIONS];
static uint8_t orient_distance[ORIENTATIONS];

typedef struct {
    uint16_t p, o, child_p, child_o;
    uint8_t next_move, previous_face;
} frame_t;

typedef struct {
    uint8_t moves[11];
    int length, initial_bound, iterations;
    uint64_t expanded, generated;
} result_t;

static uint8_t heuristic(uint16_t p, uint16_t o)
{
    return perm_distance[p] > orient_distance[o] ?
           perm_distance[p] : orient_distance[o];
}

/* Host-only BFS queue, reused between projections. Nine unit-cost HTM moves. */
static int make_distances(unsigned count, uint16_t next[3][count], uint8_t *distance)
{
    uint16_t queue[PERMUTATIONS];
    unsigned head = 0, tail = 1;
    memset(distance, UINT8_MAX, count);
    distance[0] = 0;
    queue[0] = 0;
    while (head < tail) {
        uint16_t here = queue[head++];
        for (unsigned face = 0; face < 3; ++face) {
            uint16_t child = here;
            for (unsigned turn = 0; turn < 3; ++turn) {
                child = next[face][child];
                if (distance[child] == UINT8_MAX) {
                    distance[child] = (uint8_t) (distance[here] + 1);
                    queue[tail++] = child;
                }
            }
        }
    }
    return tail == count;
}

static int prepare(void)
{
    state_t state;
    for (unsigned p = 0; p < PERMUTATIONS; ++p) {
        unrank_state(p * ORIENTATIONS, &state);
        for (uint8_t face = 0; face < 3; ++face) {
            state_t next = quarter_turn(state, face);
            perm_next[face][p] = (uint16_t) (rank_state(&next) / ORIENTATIONS);
        }
    }
    for (unsigned o = 0; o < ORIENTATIONS; ++o) {
        unrank_state(o, &state);
        for (uint8_t face = 0; face < 3; ++face) {
            state_t next = quarter_turn(state, face);
            orient_next[face][o] = (uint16_t) (rank_state(&next) % ORIENTATIONS);
        }
    }
    return make_distances(PERMUTATIONS, perm_next, perm_distance) &&
           make_distances(ORIENTATIONS, orient_next, orient_distance);
}

static frame_t frame(uint16_t p, uint16_t o, uint8_t previous_face)
{
    frame_t f = {p, o, p, o, 0, previous_face};
    return f;
}

static result_t search(uint32_t rank)
{
    result_t result = {{0}, -1, 0, 0, 0, 0};
    uint16_t p = (uint16_t) (rank / ORIENTATIONS);
    uint16_t o = (uint16_t) (rank % ORIENTATIONS);
    frame_t stack[12];
    result.initial_bound = heuristic(p, o);
    for (int bound = result.initial_bound; bound <= 11; ++bound) {
        ++result.iterations;
        int depth = 0;
        stack[0] = frame(p, o, 3);
        ++result.expanded;
        while (depth >= 0) {
            frame_t *f = &stack[depth];
            if (f->p == 0 && f->o == 0) {
                result.length = depth;
                return result;
            }
            if (depth == bound || f->next_move == MOVES) {
                --depth;
                continue;
            }
            uint8_t move = f->next_move++;
            uint8_t face = move / 3;
            /* Consecutive turns of one face compose to at most one HTM move. */
            if (face == f->previous_face)
                continue;
            if (move % 3 == 0) {
                f->child_p = f->p;
                f->child_o = f->o;
            }
            f->child_p = perm_next[face][f->child_p];
            f->child_o = orient_next[face][f->child_o];
            ++result.generated;
            if (depth + 1 + heuristic(f->child_p, f->child_o) > bound)
                continue;
            result.moves[depth] = move;
            stack[depth + 1] = frame(f->child_p, f->child_o, face);
            ++depth;
            ++result.expanded;
        }
    }
    return result;
}

/* Host-only reference distances: follow the upstream exact move-to-goal table.
 * Memoization avoids rewalking suffixes. No search heuristic is used here.
 */
static uint8_t *oracle_distances(void)
{
    uint8_t diameter;
    uint8_t *toward = build_table(&diameter);
    uint8_t *distance = malloc(STATES);
    if (!toward || !distance || diameter != 11) {
        free(toward);
        free(distance);
        return NULL;
    }
    memset(distance, UINT8_MAX, STATES);
    distance[0] = 0;
    for (uint32_t rank = 1; rank < STATES; ++rank) {
        uint32_t chain[11], current = rank;
        unsigned length = 0;
        while (distance[current] == UINT8_MAX) {
            state_t state;
            if (length == 11 || toward[current] >= MOVES) {
                free(toward);
                free(distance);
                return NULL;
            }
            chain[length++] = current;
            unrank_state(current, &state);
            state = apply_move(state, toward[current]);
            current = rank_state(&state);
        }
        unsigned d = distance[current];
        while (length)
            distance[chain[--length]] = (uint8_t) ++d;
    }
    free(toward);
    return distance;
}

static int verify_path(state_t state, const result_t *result, uint8_t exact)
{
    if (result->length != exact || result->length < 0 || result->length > 11)
        return 0;
    for (int i = 0; i < result->length; ++i)
        state = apply_move(state, result->moves[i]);
    return rank_state(&state) == 0;
}

static void print_result(uint32_t rank, const result_t *result)
{
    printf("rank=%u initial_h=%d length=%d iterations=%d expanded=%" PRIu64
           " generated=%" PRIu64 "\n", rank, result->initial_bound,
           result->length, result->iterations, result->expanded, result->generated);
    for (int i = 0; i < result->length; ++i)
        printf("%s%s", i ? " " : "", move_names[result->moves[i]]);
    putchar('\n');
}

static int check(int exhaustive_search)
{
    uint8_t *exact = oracle_distances();
    if (!exact)
        return 1;
    unsigned pmax = 0, omax = 0, histogram[12] = {0};
    for (unsigned p = 0; p < PERMUTATIONS; ++p) {
        if (perm_distance[p] == UINT8_MAX) { free(exact); return 1; }
        if (perm_distance[p] > pmax) pmax = perm_distance[p];
    }
    for (unsigned o = 0; o < ORIENTATIONS; ++o) {
        if (orient_distance[o] == UINT8_MAX) { free(exact); return 1; }
        if (orient_distance[o] > omax) omax = orient_distance[o];
    }
    for (uint32_t rank = 0; rank < STATES; ++rank) {
        if (exact[rank] > 11 || heuristic(rank / ORIENTATIONS, rank % ORIENTATIONS) > exact[rank]) {
            fprintf(stderr, "distance/admissibility failure at %u\n", rank);
            free(exact);
            return 1;
        }
        ++histogram[exact[rank]];
    }
    if (perm_distance[0] || orient_distance[0] || histogram[11] != 2644) {
        free(exact);
        return 1;
    }
    printf("H1 heuristic check: %d states passed\n", STATES);
    printf("PDBs fully populated; solved entries 0; maxima p=%u o=%u\n", pmax, omax);
    printf("Oracle distance-11 count: %u\n", histogram[11]);
    if (!exhaustive_search) {
        const char *vectors[] = {
            "12345671111111", "62345713133111", "24316572122213",
            "25713642221111", "24513763133333", "43752611332133",
            "25416373331111", "21345671111111"
        };
        for (unsigned i = 0; i < sizeof vectors / sizeof *vectors; ++i) {
            state_t state;
            if (!parse_state(vectors[i], &state)) { free(exact); return 1; }
            uint32_t rank = rank_state(&state);
            result_t result = search(rank);
            if (!verify_path(state, &result, exact[rank])) { free(exact); return 1; }
            print_result(rank, &result);
        }
        state_t solved = {{0, 1, 2, 3, 4, 5, 6}, {0}};
        for (uint8_t move = 0; move < MOVES; ++move) {
            state_t state = apply_move(solved, move);
            uint32_t rank = rank_state(&state);
            result_t result = search(rank);
            if (!verify_path(state, &result, 1)) { free(exact); return 1; }
        }
        puts("Search/path checks: 8 reference vectors + 9 one-move states passed.");
        puts("H3 exhaustive search NOT run. Target checks NOT run.");
    } else {
        struct timeval start, end;
        gettimeofday(&start, NULL);
        uint64_t maximum_generated = 0;
        uint32_t worst_rank = 0, checked = 0;
        for (uint32_t rank = 0; rank < STATES; ++rank) {
            if (exhaustive_search == 2 && exact[rank] != 11)
                continue;
            state_t state;
            unrank_state(rank, &state);
            result_t result = search(rank);
            if (!verify_path(state, &result, exact[rank])) {
                fprintf(stderr, "search failure at %u\n", rank);
                free(exact);
                return 1;
            }
            ++checked;
            if (result.generated > maximum_generated) {
                maximum_generated = result.generated;
                worst_rank = rank;
            }
            if (exhaustive_search == 1 && checked % 10000 == 0) {
                fprintf(stderr, "checked %u/%d\n", checked, STATES);
                fflush(stderr);
            }
        }
        gettimeofday(&end, NULL);
        printf("Host search/path checks passed: %u; wall seconds %.3f\n", checked,
               end.tv_sec - start.tv_sec + (end.tv_usec - start.tv_usec) / 1e6);
        state_t worst;
        char input[15];
        unrank_state(worst_rank, &worst);
        for (unsigned i = 0; i < 7; ++i) {
            input[i] = (char) ('1' + worst.p[i]);
            input[i + 7] = (char) ('1' + worst.o[i]);
        }
        input[14] = '\0';
        printf("Maximum generated children: %" PRIu64 "; state: %s\n",
               maximum_generated, input);
        puts(exhaustive_search == 1 ? "H3 host full-domain check passed." :
             "Only distance-11 states searched; full-domain H3 NOT run.");
        puts("Target instruction counts and target checks NOT run.");
    }
    free(exact);
    return output_failed();
}

#ifndef IDA_REFERENCE_LIBRARY
int main(int argc, char **argv)
{
    if (argc != 2) {
        fputs("usage: ida_reference STATE | --check | --check-hard | --check-all\n", stderr);
        return 2;
    }
    if (!prepare()) {
        fputs("incomplete projection table\n", stderr);
        return 1;
    }
    fprintf(stderr, "transition+PDB payload: %zu bytes; explicit search stack: %zu bytes\n",
            sizeof perm_next + sizeof orient_next + sizeof perm_distance + sizeof orient_distance,
            12 * sizeof(frame_t));
    if (!strcmp(argv[1], "--check")) return check(0);
    if (!strcmp(argv[1], "--check-all")) return check(1);
    if (!strcmp(argv[1], "--check-hard")) return check(2);
    state_t state;
    if (!parse_state(argv[1], &state)) return 2;
    uint32_t rank = rank_state(&state);
    result_t result = search(rank);
    print_result(rank, &result);
    return result.length < 0 || output_failed();
}
#endif
