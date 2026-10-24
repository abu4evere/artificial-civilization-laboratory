# CC1: The Cumulative Brain Proof (The Ratchet Effect)

## Objective
Demonstrate a "strong proof" of cumulative culture in ACL: a population achieves a complex goal through a chain of discovery that no single individual could reasonably achieve in one lifetime.

## The Hypothesis
If the "Cumulative Brain" mechanism is working, a population with teaching enabled will achieve a multi-step technological goal (the "Advanced Spear") significantly more often than a population where individuals must discover all steps independently, despite the individual discovery chance being near-zero for the full chain.

## The Knowledge Chain (The Ratchet)
We will introduce a 3-step dependency chain for a new high-value item: **The Advanced Spear**.

1. **Step 1: Hardened Wood (Component)**
   - *Discovery:* Accidental discovery while foraging/using fire.
   - *Probability:* Low, but possible for an individual.
2. **Step 2: Shaping Tool (Intermediate)**
   - *Requirement:* Must know `Hardened Wood`.
   - *Discovery:* Once Step 1 is known, a chance to "figure out" the tool.
   - *Probability:* Near-zero if Step 1 is unknown.
3. **Step 3: Advanced Spear (Final)**
   - *Requirement:* Must know `Shaping Tool`.
   - *Discovery:* Once Step 2 is known, a chance to "figure out" the final spear.
   - *Probability:* Near-zero if Step 2 is unknown.

## Experimental Design
**Baseline:** Nature v6.

**Arms:**
- **Arm C (Control):** Teaching is disabled. Agents can discover the steps, but cannot share them. (Individual learning only).
- **Arm R (Ratchet):** Teaching is enabled (standard Nature v6). Agents can share the steps. (Cumulative learning).

**Sample Size:** 256 worlds per arm.

## Success Metrics (The Proof)
We will define a **Strong Proof of Cumulative Culture** if:
1. **Population Success:** The `Advanced Spear` is created in Arm R but almost never in Arm C.
2. **Individual Limitation:** In Arm R, the agents who created the `Advanced Spear` did NOT discover all three steps themselves (i.e., they learned at least one step from another agent).
3. **Ratchet Verification:** We track the "First Discovery" of each step. The timeline must show Step 1 discovered $\rightarrow$ Step 2 discovered $\rightarrow$ Step 3 discovered.

## Implementation Steps
1. **Code:** Implement the 3-step recipe chain in the simulation code.
2. **Verify:** Perform "Zero Checks" to ensure:
   - An agent without Step 1 cannot discover Step 2.
   - An agent without Step 2 cannot discover Step 3.
3. **Run:** Execute Arm C and Arm R via GitHub Actions.
4. **Analyze:** Extract the discovery chains and population survival/growth.

## Frozen Rule
This plan is frozen upon creator sign-off. No code will be written, and no data will be collected until the tag `CC1-frozen` is applied.
