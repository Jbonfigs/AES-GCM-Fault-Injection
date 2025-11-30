# AES-GCM Fault Injection Demo

This demo shows fault injection attacks on AES-GCM authenticated encryption, specifically targeting the GHASH authentication function.

## What's in this demo

This folder contains a bare-metal implementation of AES-GCM's GHASH component compiled for ARM. We use this to demonstrate how fault injection can bypass authentication in encrypted communications.

## Quick Start

### Running the golden run

First, let's verify everything works without any faults:
```bash
./faultfinder demos/aes-gcm-arm/jsons/goldenrun_full.json
```

You should see the program execute successfully and output a tag value in register R0.

### Running a basic fault campaign

To inject faults into the GHASH computation:
```bash
./faultfinder demos/aes-gcm-arm/jsons/fault.json
```

This will inject single-bit faults into registers during the Galois field multiplication and show which faults produce corrupted authentication tags.

### Attack demonstration

We also include a more realistic attack scenario where an attacker tries to forge a modified message:
```bash
./faultfinder demos/aes-gcm-arm/jsons/attack-goldenrun.json
./faultfinder demos/aes-gcm-arm/jsons/attack-fault.json
```

The golden run shows that without faults, the modified message is correctly rejected. The fault campaign shows how many faults allow the forged message to pass authentication.

## What to look at

1. **Binary details** - `jsons/binary-details.json` and `jsons/attack-binary-details.json` configure the memory layout and where to capture outputs
2. **Fault models** - `faultmodels/ghash-focused.txt` and `faultmodels/forgery-attack.txt` define which instructions and registers to fault
3. **Campaign configs** - The various JSON files in `jsons/` bring together the binary and fault model settings

## Analyzing results

After running a fault campaign, you can analyze the outputs:
```bash
grep "Output from register (R0):" demos/aes-gcm-arm/outputs/* | awk '{print $NF}' | sort | uniq -c | sort -rn
```

For the attack demo, check how many faults bypassed authentication:
```bash
grep "Output from register (R0): 0x1\." demos/aes-gcm-arm/attack-outputs/* | wc -l
```

## Building from source

If you want to modify the code:
```bash
cd ~/aes-gcm-fault

# Edit the source
vim aes_gcm_simple.c

# Recompile
arm-linux-gnueabi-gcc -nostdlib -nostartfiles -static -O0 -g aes_gcm_simple.c -o aes_gcm_simple.elf -T link.ld
arm-linux-gnueabi-objcopy -O binary aes_gcm_simple.elf aes_gcm_simple.bin

# Copy to demo folder
cp aes_gcm_simple.bin ~/fault-finder/demos/aes-gcm-arm/
```

The same process works for the attack demo - just use `aes_gcm_attack_demo.c` instead.

## Notes

- The binaries are compiled for ARM 32-bit (ARMv7)
- We use a custom linker script to place code at address 0x8000
- Checkpoints are used to speed up the fault campaigns - you can adjust the number in the campaign JSON files

## Why GHASH?

GHASH is the authentication component of AES-GCM. It performs polynomial multiplication in GF(2^128), which involves a lot of iterative operations on registers. This makes it a good target for demonstrating how faults during cryptographic computations can break security guarantees.