/* Host-only validation helper. Reuses the upstream model and exact BFS.
 * This is not a target solver and does not constitute H3 or T5 coverage.
 * Build: cc -O3 -std=c99 -Wall -Wextra -Wpedantic tests/verify_path.c
 *        -o output/verify_path
 */
#define main upstream_solver_main
#include "../solver.c"
#undef main

static int exact_distance(state_t state, const uint8_t *table)
{
    for (int distance = 0; distance <= 11; ++distance) {
        uint32_t rank = rank_state(&state);
        if (rank == 0)
            return distance;
        if (table[rank] >= MOVES)
            break;
        state = apply_move(state, table[rank]);
    }
    return -1;
}

int main(int argc, char **argv)
{
    state_t initial, current;
    uint8_t diameter;
    if (argc != 3 || !parse_state(argv[1], &initial)) {
        fputs("usage: verify_path STATE \"SPACE-SEPARATED MOVES\"\n", stderr);
        return 2;
    }
    size_t size = strlen(argv[2]) + 1;
    char *path = malloc(size);
    if (!path)
        return 1;
    memcpy(path, argv[2], size);
    current = initial;
    size_t length = 0;
    for (char *token = strtok(path, " \t\r\n"); token;
         token = strtok(NULL, " \t\r\n")) {
        uint8_t move = 0;
        while (move < MOVES && strcmp(token, move_names[move]))
            ++move;
        if (move == MOVES) {
            fprintf(stderr, "invalid move: %s\n", token);
            free(path);
            return 2;
        }
        current = apply_move(current, move);
        ++length;
    }
    free(path);
    uint8_t *table = build_table(&diameter);
    if (!table || diameter != 11) {
        free(table);
        fputs("baseline BFS unavailable or unexpected diameter\n", stderr);
        return 1;
    }
    int distance = exact_distance(initial, table);
    free(table);
    if (distance < 0) {
        fputs("baseline path inconsistent\n", stderr);
        return 1;
    }
    int solved = rank_state(&current) == 0;
    int optimal = solved && length == (size_t) distance;
    printf("exact_distance: %d\npath_length: %zu\nsolved: %s\noptimal: %s\n",
           distance, length, solved ? "yes" : "no", optimal ? "yes" : "no");
    if (output_failed())
        return 1;
    return optimal ? 0 : 1;
}
