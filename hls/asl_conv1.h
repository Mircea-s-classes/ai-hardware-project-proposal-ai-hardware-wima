#pragma once

#define IMG_H 28
#define IMG_W 28
#define IMG_C 1
#define OUT_C 32
#define K     3

void asl_conv1(
    float *in,   // pointer to input feature map in DDR
    float *out   // pointer to output feature map in DDR
);
