#include "target.h"

typedef struct {
    uint16_t p, o, child_p, child_o;
    uint8_t next_move, previous_face;
} search_frame;

/* Pointer lookup avoids calculating a face-dependent non-power-of-two stride. */
static const uint16_t *const perm_rows[3] = {rt_perm[0], rt_perm[1], rt_perm[2]};
static const uint16_t *const orient_rows[3] = {rt_orient[0], rt_orient[1], rt_orient[2]};
static const uint8_t face_of[9] = {0, 0, 0, 1, 1, 1, 2, 2, 2};
static const uint8_t first_turn[9] = {1, 0, 0, 1, 0, 0, 1, 0, 0};

static unsigned estimate(unsigned p, unsigned o)
{
    return rt_pd[p] > rt_od[o] ? rt_pd[p] : rt_od[o];
}

static void set_frame(search_frame *f, unsigned p, unsigned o, unsigned previous)
{
    f->p = f->child_p = (uint16_t) p;
    f->o = f->child_o = (uint16_t) o;
    f->next_move = 0;
    f->previous_face = (uint8_t) previous;
}

int target_search(unsigned p, unsigned o, uint8_t path[11])
{
    search_frame stack[12];
    for (unsigned bound = estimate(p, o); bound <= 11; ++bound) {
        int depth = 0;
        set_frame(&stack[0], p, o, 3);
        while (depth >= 0) {
            search_frame *f = &stack[depth];
            if (f->p == 0 && f->o == 0) return depth;
            if ((unsigned) depth == bound || f->next_move == 9) {
                --depth;
                continue;
            }
            unsigned move = f->next_move++;
            unsigned face = face_of[move];
            if (face == f->previous_face) continue;
            if (first_turn[move]) {
                f->child_p = f->p;
                f->child_o = f->o;
            }
            f->child_p = perm_rows[face][f->child_p];
            f->child_o = orient_rows[face][f->child_o];
            if ((unsigned) depth + 1 + estimate(f->child_p, f->child_o) > bound)
                continue;
            path[depth] = (uint8_t) move;
            set_frame(&stack[depth + 1], f->child_p, f->child_o, face);
            ++depth;
        }
    }
    return -1;
}
