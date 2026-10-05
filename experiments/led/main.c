/* AI-authored display integration/reference. Existing student search unchanged. */
#include "../rv32_baseline/target.h"
#ifndef CUBE_INPUT
#define CUBE_INPUT "25314672313211"
#endif
#ifndef RENDER
#define RENDER 0
#endif
extern void ripes_puts(const char *);
extern void ripes_putint(unsigned);
#if RENDER
extern void led_draw(const uint8_t *,const uint8_t *,volatile unsigned *,unsigned);
static void draw(const uint8_t *p,const uint8_t *o,volatile unsigned *base,unsigned delay) {
    led_draw(p,o,base,35);
    /* Hash every pixel for comparison with independent host geometry. */
    unsigned hash=0;
    for (unsigned i=0;i<875;++i) hash=(hash<<5)^(hash>>27)^base[i];
    ripes_puts("frame: ");ripes_putint(hash);ripes_puts("\n");
    if (!delay) {
        ripes_puts("pixels:");
        for (unsigned i=0;i<875;++i) { ripes_puts(" ");ripes_putint(base[i]); }
        ripes_puts("\n");
    }
    for (volatile unsigned wait=delay;wait;--wait) {}
}
#endif
int target_main(volatile unsigned *base,unsigned width,unsigned height,unsigned delay) {
    static const char input[]=CUBE_INPUT;
    static const char *const names[9]={"R","R2","R'","B","B2","B'","D","D2","D'"};
    uint8_t p[7],o[7],path[11];unsigned pr,ori;
#if RENDER
    if (width!=35 || height!=25) { ripes_puts("Set LED Width=35 Height=25\n");return 3; }
#else
    (void)base;(void)width;(void)height;(void)delay;
#endif
    if (!target_parse(input,p,o,&pr,&ori)) return 2;
    int length=target_search(pr,ori,path);
    if (!target_replay(p,o,path,length)) return 1;
    ripes_puts("input: ");ripes_puts(input);ripes_puts("\nlength: ");ripes_putint(length);
    ripes_puts("\npath: ");
    for (int i=0;i<length;++i) { if(i) ripes_puts(" ");ripes_puts(names[path[i]]); }
    ripes_puts("\nreplay: PASS\n");
#if RENDER
    target_parse(input,p,o,&pr,&ori);
    draw(p,o,base,delay);
    for (int i=0;i<length;++i) {
        /* target_replay mutates the state; false just means not yet solved.
         * Full path has already passed physical replay above. */
        uint8_t one[11]={0};one[0]=path[i];
        (void)target_replay(p,o,one,1);
        ripes_puts("move: ");ripes_puts(names[path[i]]);ripes_puts("\n");
        draw(p,o,base,delay);
    }
#endif
    return 0;
}
