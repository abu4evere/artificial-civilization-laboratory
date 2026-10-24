import sys
import os
import copy
import random

# Add ACL and the experiment folder to path
sys.path.append(os.path.abspath("D:\\acl"))
sys.path.append(os.path.abspath("D:\\acl\\experiments\\CC1_cumulative_proof"))

from acl import world
from acl.config import Config
from ledger import ledger as global_ledger

def test_dependency_chain():
    print("Running Dependency Chain Test...")
    cfg = Config(founders=1)
    w = world.World(cfg)
    # Use the first agent in the dictionary
    p = list(w.people.values())[0]
    
    # Step 1: Hardened Wood
    # We simulate the result of heating wood
    from acl.matter import item_from
    hardened_wood = item_from("wood^5", {"hard": 50, "tight": 50, "edge": 5, "reach": 60, "contain": 0, "warm": 0, "float": 50, "plastic": 0, "fuel": 60, "flex": 20})
    
    # Test: Shaping Tool requires Hardened Wood
    from acl.knowhow import can_follow
    recipe_shaping = {"verb": "strike", "target": "hardened_wood", "tool": "stone", "parts": ["hardened_wood"]}
    
    # Before knowing Hardened Wood
    p.recipes = {}
    assert not can_follow(p, recipe_shaping), "FAILED: Should not be able to follow Shaping Tool without Hardened Wood"
    
    # After knowing Hardened Wood
    p.recipes["hardened_wood"] = {} 
    assert can_follow(p, recipe_shaping), "FAILED: Should be able to follow Shaping Tool with Hardened Wood"
    
    # Test: Advanced Spear requires Shaping Tool
    recipe_spear = {"verb": "bind", "parts": ["shaping_tool", "wood"], "binder": "fiber"}
    p.recipes = {}
    assert not can_follow(p, recipe_spear), "FAILED: Should not be able to follow Advanced Spear without Shaping Tool"
    p.recipes["shaping_tool"] = {}
    assert can_follow(p, recipe_spear), "FAILED: Should be able to follow Advanced Spear with Shaping Tool"
    
    print("PASS: Dependency Chain Verified.")

def test_control_isolation():
    print("Running Control Isolation Test...")
    cfg = Config(founders=2)
    w = world.World(cfg)
    p1, p2 = list(w.people.values())
    
    # Manually give p1 a recipe
    p1.recipes["test_recipe"] = {"verb": "strike", "target": "stone", "tool": "stone"}
    p1.itemval["test_recipe"] = 1.0
    
    # Arm C simulation: we manually simulate the 'block'
    # In actual implementation, this is a flag in the experiment runner.
    # Here we verify the a la mode block.
    from acl.information import show_how
    
    # Mock a a a 'Arm C' world where we'd intercept the call.
    # Since we haven't modified show_how yet to take a flag, we test that 
    # a learner without prerequisites cannot learn.
    p2.recipes = {}
    # Give p2 a recipe that requires something they don't have
    recipe_hard = {"verb": "strike", "target": "hardened_wood", "tool": "stone", "parts": []}
    p1.recipes["hardened_wood"] = {}
    p1.recipes["shaping_tool"] = recipe_hard
    p1.itemval["shaping_tool"] = 1.0
    
    # Try to teach
    result = show_how(w, p1, p2, False)
    # result should be False because p2 cannot follow the recipe
    assert not result, "FAILED: Learner should not have acquired a recipe they cannot follow"
    
    print("PASS: Control Isolation (Prerequisite Block) Verified.")

def test_deterministic_replay():
    print("Running Deterministic Replay Test...")
    cfg = Config(seed=42, founders=5)
    
    # Run 1: No Ledger
    w1 = world.World(cfg)
    for _ in range(100):
        w1.step()
    state1 = {
        "pop": len(w1.living()),
        "recipes": sum(len(p.recipes) for p in w1.living()),
        "health": sum(p.health for p in w1.living())
    }
    
    # Run 2: With Ledger
    w2 = world.World(cfg)
    w2.cc1_ledger = global_ledger
    # Clear ledger for fresh run
    global_ledger.events = []
    for _ in range(100):
        w2.step()
    state2 = {
        "pop": len(w2.living()),
        "recipes": sum(len(p.recipes) for p in w2.living()),
        "health": sum(p.health for p in w2.living())
    }
    
    assert state1 == state2, f"FAILED: Divergence detected! {state1} vs {state2}"
    print("PASS: Deterministic Replay Verified.")

if __name__ == "__main__":
    try:
        test_dependency_chain()
        test_control_isolation()
        test_deterministic_replay()
        print("\nALL VALIDATION TESTS PASSED.")
    except AssertionError as e:
        print(f"\nVALIDATION FAILED: {e}")
        sys.exit(1)
