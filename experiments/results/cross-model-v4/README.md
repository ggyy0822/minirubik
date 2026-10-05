# Cross-model tests of frozen assembly search v4

Four inputs pass actual target physical replay and native exact-distance checking
on both RV32_ISS and RV32_5S. These cover solved, one-step, three-step and the
reference eleven-step case. Paths agree between models. See summary.csv/json and
raw reports. The reference 5S run: 16,128,314 retired; 19,952,587 cycles;
395,311 ms model time. It was allowed 900,000 ms and finished successfully.

This is not the LED-integrated final runtime or an entirely handwritten program:
input parsing/replay/startup retain their documented provenance. Do not infer
full 2644-state performance coverage, final-build coverage, or observed GUI
control signals from these CLI results. Raw one-instruction model retirement
count differences are preserved. Measurements were executed by the assistant;
student reproduction and own-work requirements remain distinct.
