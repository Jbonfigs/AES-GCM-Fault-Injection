#!/bin/bash
echo "=========================================="
echo "AES-GCM FAULT INJECTION RESULTS"
echo "=========================================="
echo ""
echo "Total faults injected: 5000"
echo "Total output files: $(ls demos/aes-gcm-arm/outputs/*.txt 2>/dev/null | wc -l)"
echo ""
echo "Golden tag (correct): 0x6a94589f"
echo ""
echo "RESULTS BREAKDOWN:"
echo "------------------"
total=$(grep "Output from register" demos/aes-gcm-arm/outputs/* | wc -l)
golden=$(grep "0x6a94589f" demos/aes-gcm-arm/outputs/* | wc -l)
crashes=$(grep "0x30f" demos/aes-gcm-arm/outputs/* | wc -l)
exploitable=$((total - golden - crashes))

echo "No effect (golden tag):        $golden ($(echo "scale=1; $golden*100/$total" | bc)%)"
echo "Crashes (program errors):      $crashes ($(echo "scale=1; $crashes*100/$total" | bc)%)"  
echo "Corrupted tags (exploitable):  $exploitable ($(echo "scale=1; $exploitable*100/$total" | bc)%)"
echo ""
echo "TOP 10 CORRUPTED TAGS:"
grep "Output from register (R0):" demos/aes-gcm-arm/outputs/* | \
  awk '{print $NF}' | \
  grep -v "0x30f" | \
  grep -v "0x6a94589f" | \
  sort | uniq -c | sort -rn | head -10