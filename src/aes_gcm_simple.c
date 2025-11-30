#define GCM_BLOCK_SIZE 16

typedef unsigned char uint8_t;
typedef unsigned int uint32_t;
typedef unsigned long size_t;

// Simple memcpy
void my_memcpy(uint8_t *dst, const uint8_t *src, size_t n) {
    for (size_t i = 0; i < n; i++) {
        dst[i] = src[i];
    }
}

// Simple memset
void my_memset(uint8_t *s, int c, size_t n) {
    for (size_t i = 0; i < n; i++) {
        s[i] = (uint8_t)c;
    }
}

// GF(2^128) multiplication
void gf128_mul(uint8_t *result, const uint8_t *x, const uint8_t *h) {
    uint8_t z[GCM_BLOCK_SIZE];
    uint8_t v[GCM_BLOCK_SIZE];
    
    my_memset(z, 0, GCM_BLOCK_SIZE);
    my_memcpy(v, h, GCM_BLOCK_SIZE);
    
    for (int i = 0; i < 128; i++) {
        int byte_idx = i / 8;
        int bit_idx = 7 - (i % 8);
        
        if (x[byte_idx] & (1 << bit_idx)) {
            for (int j = 0; j < GCM_BLOCK_SIZE; j++) {
                z[j] ^= v[j];
            }
        }
        
        uint8_t lsb = v[15] & 1;
        for (int j = 15; j > 0; j--) {
            v[j] = (v[j] >> 1) | (v[j-1] << 7);
        }
        v[0] >>= 1;
        
        if (lsb) {
            v[0] ^= 0xe1;
        }
    }
    
    my_memcpy(result, z, GCM_BLOCK_SIZE);
}

// GHASH computation
void ghash(const uint8_t *h, const uint8_t *data, uint8_t *output) {
    uint8_t accumulator[GCM_BLOCK_SIZE];
    
    my_memset(accumulator, 0, GCM_BLOCK_SIZE);
    
    // Process single block
    for (int j = 0; j < GCM_BLOCK_SIZE; j++) {
        accumulator[j] ^= data[j];
    }
    
    gf128_mul(accumulator, accumulator, h);
    my_memcpy(output, accumulator, GCM_BLOCK_SIZE);
}

void _start(void) {
    uint8_t h[GCM_BLOCK_SIZE] = {0x66, 0xe9, 0x4b, 0xd4, 0xef, 0x8a, 0x2c, 0x3b,
                                  0x88, 0x4c, 0xfa, 0x59, 0xca, 0x34, 0x2b, 0x2e};
    uint8_t data[GCM_BLOCK_SIZE] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                                     0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10};
    uint8_t tag[GCM_BLOCK_SIZE];

    ghash(h, data, tag);

    // Put first 4 bytes of tag in r0 for easy checking
    register uint32_t result asm("r0");
    result = ((uint32_t*)tag)[0];

    asm volatile("" : : "r"(result)); // Prevent optimization
    return;
}
