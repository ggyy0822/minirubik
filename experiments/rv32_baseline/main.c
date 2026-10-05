#include "target.h"
#ifndef CUBE_INPUT
#define CUBE_INPUT "21345671111111"
#endif
static const char input[] = CUBE_INPUT;
extern void ripes_puts(const char *);
extern void ripes_putint(unsigned);

int target_main(void)
{
    static const char *const names[9] = {"R", "R2", "R'", "B", "B2", "B'", "D", "D2", "D'"};
    uint8_t p[7], o[7], path[11];
    unsigned pr, ori;
    if (!target_parse(input, p, o, &pr, &ori)) {
        ripes_puts("INVALID INPUT\n");
        return 2;
    }
    int length = target_search(pr, ori, path);
    if (!target_replay(p, o, path, length)) {
        ripes_puts("PATH CHECK FAILED\n");
        return 1;
    }
    ripes_puts("input: "); ripes_puts(input);
    ripes_puts("\nlength: "); ripes_putint((unsigned) length);
    ripes_puts("\npath: ");
    for (int i = 0; i < length; ++i) {
        if (i) ripes_puts(" ");
        ripes_puts(names[path[i]]);
    }
    ripes_puts("\nreplay: PASS\n");
    return 0;
}
