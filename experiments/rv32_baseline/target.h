/* AI-generated educational compiler baseline, not student-authored assembly. */
#ifndef TARGET_H
#define TARGET_H
#include <stdint.h>
extern const uint16_t rt_perm[3][5040];
extern const uint16_t rt_orient[3][729];
extern const uint8_t rt_pd[5040], rt_od[729];
int target_search(unsigned p, unsigned o, uint8_t path[11]);
int target_parse(const char *input, uint8_t p[7], uint8_t o[7],
                 unsigned *prank, unsigned *orank);
int target_replay(uint8_t p[7], uint8_t o[7], const uint8_t path[11], int length);
#endif
