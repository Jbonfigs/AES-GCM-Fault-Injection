# AES-GCM Fault Injection Attack Demonstration

**Course Project**: EECE7352 - Computer Architecture  
**Author**: Jack Bonfiglio  
**Institution**: Northeastern University  
**Date**: December 2025

## Overview

This project demonstrates practical fault injection attacks on AES-GCM authenticated encryption using the FaultFinder simulation framework. We show that physical fault injection can bypass cryptographic authentication, allowing message forgery with a 24% success rate.

## What This Demonstrates

### Security Vulnerability

AES-GCM is used in TLS 1.3 and IPsec. This project shows:
- GHASH authentication can be bypassed with fault injection
- ~1 in 4 faults allows message forgery
- Physical security is critical for cryptographic systems

### Attack Scenario

**Original Message**: "Transfer $100"  
**Modified Message**: "Transfer $999"  

Without faults: Attack detected  
With faults: 24% success rate

## Technologies Used

- **FaultFinder**: Multi-architecture fault injection simulator
- **Unicorn Engine**: CPU emulation framework
- **ARM GCC**: Cross-compilation toolchain
- **Python/Matplotlib**: Data visualization

## Project Structure
```
├── README.md                          # This file
├── docs/
│   ├── ATTACK_DEMONSTRATION.md       # Attack scenario walkthrough
│   ├── EECE7352-Final-Project-Report.pdf       # Complete technical analyis
│   └── *.png                         # Visualizations
├── src/
│   ├── aes_gcm_simple.c             # GHASH implementation
│   ├── aes_gcm_attack_demo.c        # Attack scenario code
│   └── link.ld                       # Linker script
├── aes-gcm-arm/                      # FaultFinder demo files
│   ├── jsons/                        # Configuration files
│   ├── faultmodels/                  # Fault injection models
│   ├── outputs/                      # Campaign results
│   └── README.md                     # Demo usage guide
└── scripts/
    ├── analyze_results.sh            # Results analysis
    ├── create_visualization.py       # Generate charts
    └── create_attack_visualization.py # Attack visualizations
```

## Quick Start

### Prerequisites

This project requires [FaultFinder](https://github.com/fault-finder/fault-finder) to be installed.
```bash
# Clone FaultFinder
git clone https://github.com/fault-finder/fault-finder.git
cd fault-finder

# Install dependencies (Ubuntu/Debian)
sudo apt-get install libjson-c-dev pkg-config

# Install Capstone and Unicorn (see FaultFinder README)
# Then build
make faultfinder
```

### Running the Demo

1. **Copy demo files to FaultFinder**:
```bash
cp -r aes-gcm-arm /path/to/fault-finder/demos/
```

2. **Run golden run** (verify setup):
```bash
cd /path/to/fault-finder
./faultfinder demos/aes-gcm-arm/jsons/goldenrun_full.json
```

3. **Run fault campaign**:
```bash
./faultfinder demos/aes-gcm-arm/jsons/fault.json
```

4. **Run attack demonstration**:
```bash
./faultfinder demos/aes-gcm-arm/jsons/attack-fault.json
```

### Analyzing Results
```bash
# View results summary
./analyze_results.sh

# Generate visualizations
python3 create_visualization.py
python3 create_attack_visualization.py
```

## Documentation

- [**Final Report**](docs/EECE7352-Final-Project-Report.pdf) - Complete technical analysis
- [**Attack Demo**](docs/ATTACK_DEMONSTRATION.md) - Step-by-step attack walkthrough

## Building from Source
```bash
cd src

# Compile for ARM
arm-linux-gnueabi-gcc -nostdlib -nostartfiles -static -O0 -g \
  aes_gcm_simple.c -o aes_gcm_simple.elf -T link.ld

# Create binary
arm-linux-gnueabi-objcopy -O binary aes_gcm_simple.elf aes_gcm_simple.bin

# Same process for attack demo
arm-linux-gnueabi-gcc -nostdlib -nostartfiles -static -O0 -g \
  aes_gcm_attack_demo.c -o aes_gcm_attack_demo.elf -T link.ld
arm-linux-gnueabi-objcopy -O binary aes_gcm_attack_demo.elf aes_gcm_attack_demo.bin
```

## Key Results

- **7.4%** of faults produce exploitable authentication corruption
- **24%** success rate in forging modified banking transactions
- **14,161** successful forgeries out of 58,656 fault attempts
- Demonstrated on ARM 32-bit architecture

## References

1. Murdock, K., Thompson, M., & Oswald, D. (2024). FaultFinder: lightning-fast, multi-architectural fault injection simulation. *ASHES '24*.

## License

This project is for educational purposes as part of EECE7352 coursework.

FaultFinder is used under its MIT license: https://github.com/fault-finder/fault-finder

## Acknowledgments

- Prof. David R. Kaeli - Course instructor
- FaultFinder authors - Simulation framework

---

**Contact**: bonfiglio.j@northeastern.edu  
**Course**: EECE7352 - Computer Architecture
