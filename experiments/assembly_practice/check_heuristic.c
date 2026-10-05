/* AI-generated harness. Return 12 only if all checks pass. */
extern unsigned heuristic(unsigned p, unsigned o,
                          const unsigned char *pd, const unsigned char *od);
static const unsigned char pd[] = {0, 4, 7, 5};
static const unsigned char od[] = {0, 6, 2, 5};
unsigned smoke_main(void)
{
    if (heuristic(0, 0, pd, od) != 0) return 1;
    if (heuristic(1, 1, pd, od) != 6) return 2;
    if (heuristic(2, 2, pd, od) != 7) return 3;
    if (heuristic(3, 3, pd, od) != 5) return 4;
    if (heuristic(1, 2, pd, od) != 4) return 5;
    if (heuristic(0, 3, pd, od) != 5) return 6;
    return 12;
}
