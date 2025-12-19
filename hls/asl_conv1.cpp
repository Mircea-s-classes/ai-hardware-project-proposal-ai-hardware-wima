#include "asl_conv1.h"
#include "weights_init.h"

void asl_conv1(
    float *in,
    float *out
) {
#pragma HLS INTERFACE m_axi     port=in   offset=slave bundle=gmem
#pragma HLS INTERFACE m_axi     port=out  offset=slave bundle=gmem
#pragma HLS INTERFACE s_axilite port=in   bundle=control
#pragma HLS INTERFACE s_axilite port=out  bundle=control
#pragma HLS INTERFACE s_axilite port=return bundle=control

    float in_buf[IMG_H][IMG_W][IMG_C];
#pragma HLS ARRAY_PARTITION variable=in_buf complete dim=3

    // Load input from DDR into local buffer
    int idx = 0;
    for (int h = 0; h < IMG_H; h++) {
        for (int w = 0; w < IMG_W; w++) {
            for (int c = 0; c < IMG_C; c++) {
#pragma HLS PIPELINE II=1
                in_buf[h][w][c] = in[idx++];
            }
        }
    }

    // Conv output 26x26xOUT_C
    float conv_out[26][26][OUT_C];
#pragma HLS ARRAY_PARTITION variable=conv_out complete dim=3

    // Convolution + ReLU
    for (int y = 0; y < 26; y++) {
        for (int x = 0; x < 26; x++) {
            for (int oc = 0; oc < OUT_C; oc++) {
#pragma HLS PIPELINE II=1
                float sum = conv1_biases[oc];
                for (int ky = 0; ky < K; ky++) {
                    for (int kx = 0; kx < K; kx++) {
                        for (int ic = 0; ic < IMG_C; ic++) {
                            float v = in_buf[y + ky][x + kx][ic];
                            float w = conv1_weights[ky][kx][ic][oc];
                            sum += v * w;
                        }
                    }
                }
                // ReLU
                conv_out[y][x][oc] = (sum > 0.f) ? sum : 0.f;
            }
        }
    }

    // MaxPool 2x2 stride 2 -> 13x13xOUT_C, write back to DDR
    int out_idx = 0;
    for (int y = 0; y < 13; y++) {
        for (int x = 0; x < 13; x++) {
            for (int oc = 0; oc < OUT_C; oc++) {
#pragma HLS PIPELINE II=1
                float m = conv_out[2*y][2*x][oc];
                if (conv_out[2*y][2*x+1][oc]   > m) m = conv_out[2*y][2*x+1][oc];
                if (conv_out[2*y+1][2*x][oc]   > m) m = conv_out[2*y+1][2*x][oc];
                if (conv_out[2*y+1][2*x+1][oc] > m) m = conv_out[2*y+1][2*x+1][oc];
                out[out_idx++] = m;
            }
        }
    }
}
