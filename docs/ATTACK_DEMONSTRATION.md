# AES-GCM Authentication Forgery Attack

## Attack Scenario: Banking Transaction Forgery

### The Setup
**Legitimate Transaction**:
```
Message: "Transfer $100 to Account 5678"
Encrypted: [ciphertext block]
Authentication Tag: Valid
```

**Attacker's Goal**:
```
Intercept and modify to: "Transfer $999 to Account 5678"
Problem: Modified ciphertext produces different tag
Solution: Fault injection during tag verification
```

---

## Attack Execution

### Without Fault Injection (Baseline)
```
Golden Run Results:
- Verification Result (R0): 0x0 (FAILED)
- Computed Tag (R1): 0x1ec0750b
- ATTACK DETECTED - System rejects modified message
```

**Defense works correctly**: The authentication tag doesn't match, transaction is rejected.

---

### With Fault Injection (Attack)

**Campaign Parameters**:
- Faults injected: 10,000 instruction windows
- Target: Registers R0-R3 during GHASH computation
- Fault type: Single-bit flips (8 positions per register)
- Total attempts: 58,656

**Results**:
```
Successful Forgeries: 14,161
Failed Attacks: 18,487
Success Rate: 24.14%
```

**Interpretation**: **Nearly 1 in 4 faults allows the forged transaction to validate!**

---

## Attack Flow Diagram
```
[Legitimate Sender]
      |
      | Encrypts: "Transfer $100"
      | Tag: 0xABCD1234
      v
[Network/Storage]
      |
      | <-- ATTACKER INTERCEPTS
      |
[Attacker Modifies]
      | Changes to: "Transfer $999"
      | Tag still: 0xABCD1234 (wrong for modified data)
      v
[Receiver]
      |
      | Decrypts ciphertext
      | Computes tag from modified data
      | <-- FAULT INJECTION HERE during GHASH
      |
[Tag Verification]
      | Without fault: Tags don't match → REJECT 
      | With fault: Corrupted computation → ACCEPT 
      v
[Result]
   SUCCESS: $999 transferred instead of $100
```