/* AI-generated test harness for the student's max_distance function.
 * Existing smoke runtime prints 12 only when every check succeeds.
 */
extern unsigned max_distance(unsigned, unsigned);
unsigned smoke_main(void)
{
    if (max_distance(4, 6) != 6) return 1;
    if (max_distance(7, 2) != 7) return 2;
    if (max_distance(5, 5) != 5) return 3;
    if (max_distance(0, 0) != 0) return 4;
    if (max_distance(0, 3) != 3) return 5;
    if (max_distance(0xffffffffu, 1) != 0xffffffffu) return 6;
    return 12;
}
