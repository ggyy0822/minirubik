/* AI-generated exhaustive bounded-domain harness for the exercise.
 * g and bound span 0..11; h spans 0..7 (this candidate's PDB maximum).
 */
extern unsigned should_prune(unsigned g, unsigned h, unsigned bound);
unsigned smoke_main(void)
{
    for (unsigned g = 0; g <= 11; ++g)
        for (unsigned h = 0; h <= 7; ++h)
            for (unsigned bound = 0; bound <= 11; ++bound)
                if (should_prune(g, h, bound) != (unsigned) (g + h > bound))
                    return 1;
    return 12;
}
