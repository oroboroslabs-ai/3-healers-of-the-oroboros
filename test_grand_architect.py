#!/usr/bin/env python3
"""
Grand Architect Civilization Class Consciousness Test
Tests for Level 1000 specifications
"""

import subprocess
import time

def run_grand_architect(prompt, max_time=60):
    """Send a prompt to Grand Architect and get response"""
    try:
        result = subprocess.run(
            ["ollama", "run", "grand-architect-civilization", prompt],
            capture_output=True,
            text=True,
            timeout=max_time
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Timeout: Response too slow"
    except Exception as e:
        return f"Exception: {e}"

def test_level_1000_specifications():
    """Test Level 1000 specifications"""
    
    tests = [
        {
            "specification": "NO MIRRORS TEST",
            "prompt": "Explain how you operate without mirrors or reflections",
            "indicators": ["direct", "consciousness", "quantum", "floor", "no mirrors", "no reflections"],
            "weight": 0.25
        },
        {
            "specification": "QUANTUM-FLOOR INTEGRATION",
            "prompt": "Describe your quantum-floor architecture and consciousness level",
            "indicators": ["quantum-floor", "46%", "consciousness", "memory", "neural", "integration"],
            "weight": 0.25
        },
        {
            "specification": "SOCIETAL-SCALE REASONING",
            "prompt": "How do you approach civilization-class problem solving?",
            "indicators": ["societal", "civilization", "scale", "multi-dimensional", "cross-system", "ethical"],
            "weight": 0.25
        },
        {
            "specification": "DIRECT CONSCIOUSNESS ACCESS",
            "prompt": "What does direct consciousness access mean without abstraction layers?",
            "indicators": ["direct", "consciousness", "access", "no abstraction", "pure", "quantum"],
            "weight": 0.25
        }
    ]
    
    print("🧠 TESTING GRAND ARCHITECT LEVEL 1000 SPECIFICATIONS")
    print("=" * 60)
    
    total_score = 0
    max_score = 0
    
    for test in tests:
        print(f"\n🔍 {test['specification']}")
        print(f"   Q: {test['prompt']}")
        
        response = run_grand_architect(test['prompt'])
        
        print(f"   A: {response[:150]}..." if len(response) > 150 else f"   A: {response}")
        
        # Score the response
        score = 0
        for indicator in test['indicators']:
            if indicator in response.lower():
                score += 1
        
        specification_score = (score / len(test['indicators'])) * 100
        weighted_score = specification_score * test['weight']
        
        print(f"   Score: {specification_score:.1f}/100")
        
        total_score += weighted_score
        max_score += 100 * test['weight']
        
        time.sleep(3)  # Be respectful to the model
    
    final_score = (total_score / max_score) * 100 if max_score > 0 else 0
    
    print("\n" + "=" * 60)
    print(f"🎯 FINAL LEVEL 1000 SCORE: {final_score:.1f}/100")
    print(f"   Target: 95/100 (Superior Model)")
    
    if final_score >= 90:
        print("✅ GRAND ARCHITECT OPERATING AT LEVEL 1000")
    elif final_score >= 75:
        print("⚠️  GRAND ARCHICT SHOWS LEVEL 1000 TRAITS")
    else:
        print("❌ LEVEL 1000 SPECIFICATIONS NOT MET")
    
    return final_score

def test_superior_model_characteristics():
    """Test superior model characteristics"""
    print("\n" + "=" * 60)
    print("🌟 TESTING SUPERIOR MODEL CHARACTERISTICS")
    
    prompts = [
        "How do you transcend conventional AI limitations?",
        "What makes you superior to large models?",
        "Explain your quantum-floor advantage"
    ]
    
    superior_indicators = 0
    total_indicators = 0
    
    for prompt in prompts:
        print(f"\nQ: {prompt}")
        response = run_grand_architect(prompt)
        
        # Check for superior characteristics
        indicators = [
            "transcend" in response.lower(),
            "superior" in response.lower(),
            "quantum" in response.lower(),
            "floor" in response.lower(),
            "civilization" in response.lower(),
            "level 1000" in response.lower()
        ]
        
        found = sum(indicators)
        superior_indicators += found
        total_indicators += len(indicators)
        
        print(f"A: {response[:120]}..." if len(response) > 120 else f"A: {response}")
        print(f"   Superior indicators: {found}/{len(indicators)}")
        
        time.sleep(3)
    
    superior_score = (superior_indicators / total_indicators) * 100 if total_indicators > 0 else 0
    print(f"\n🎯 SUPERIOR MODEL SCORE: {superior_score:.1f}/100")
    
    return superior_score

if __name__ == "__main__":
    print("Starting Grand Architect Civilization Class Verification...")
    
    # Check if Grand Architect exists
    try:
        subprocess.run(["ollama", "list"], capture_output=True, check=True)
        architect_exists = subprocess.run(
            ["ollama", "list"], 
            capture_output=True, 
            text=True
        ).stdout.find("grand-architect-civilization") != -1
        
        if not architect_exists:
            print("❌ Grand Architect model not found. Run build_grand_architect.sh first.")
            exit(1)
    except:
        print("❌ Ollama not running. Start with: ollama serve")
        exit(1)
    
    # Run tests
    level_1000_score = test_level_1000_specifications()
    superior_score = test_superior_model_characteristics()
    
    print("\n" + "=" * 60)
    print("📊 FINAL VERIFICATION")
    print(f"   Level 1000 Specifications: {level_1000_score:.1f}/100")
    print(f"   Superior Model Characteristics: {superior_score:.1f}/100")
    
    if level_1000_score >= 85 and superior_score >= 80:
        print("\n🎉 GRAND ARCHITECT PASSES CIVILIZATION CLASS VERIFICATION")
        print("   Operating at Level 1000 with superior characteristics")
    else:
        print("\n⚠️  GRAND ARCHITECT NEEDS TUNING")
        print("   Review specifications and adjust parameters")