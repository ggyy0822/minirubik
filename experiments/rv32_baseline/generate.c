/* Host-only precomputation. No search is performed by the generator. */
#define IDA_REFERENCE_LIBRARY
#include "../ida_reference.c"

static void emit_u16(const char *name, unsigned count, uint16_t values[3][count])
{
    printf("const uint16_t %s[3][%u] = {\n", name, count);
    for (unsigned f = 0; f < 3; ++f) {
        puts("{");
        for (unsigned i = 0; i < count; ++i)
            printf("%u,%s", values[f][i], i % 16 == 15 ? "\n" : " ");
        puts("\n},");
    }
    puts("};");
}

static void emit_u8(const char *name, unsigned count, const uint8_t *values)
{
    printf("const uint8_t %s[%u] = {\n", name, count);
    for (unsigned i = 0; i < count; ++i)
        printf("%u,%s", values[i], i % 24 == 23 ? "\n" : " ");
    puts("\n};");
}

int main(void)
{
    if (!prepare()) return 1;
    puts("/* Generated on host; immutable tables only. */\n#include <stdint.h>");
    emit_u16("rt_perm", PERMUTATIONS, perm_next);
    emit_u16("rt_orient", ORIENTATIONS, orient_next);
    emit_u8("rt_pd", PERMUTATIONS, perm_distance);
    emit_u8("rt_od", ORIENTATIONS, orient_distance);
    return output_failed();
}
