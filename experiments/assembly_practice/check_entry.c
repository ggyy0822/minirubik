/* AI-generated branch-destination tests for the user's search entry. */
extern unsigned classify_entry(const unsigned *frame, unsigned depth, unsigned bound);
static const unsigned states[4][2] = {{0,0}, {1,0}, {0,1}, {3,7}};
unsigned smoke_main(void)
{
    for (unsigned state = 0; state < 4; ++state)
        for (unsigned bound = 0; bound <= 11; ++bound)
            for (unsigned depth = 0; depth <= bound; ++depth) {
                unsigned expected = state == 0 ? 1 : (depth == bound ? 2 : 0);
                if (classify_entry(states[state], depth, bound) != expected) return 1;
            }
    return 12;
}
