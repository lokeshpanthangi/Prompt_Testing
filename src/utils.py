import re
import json
from colorama import Fore, Style

def format_response(response, query, hallucination_check):
    """Format a response with hallucination warnings if needed"""
    formatted = f"Q: {query}\n\n"
    
    if hallucination_check["score"] > 5:
        formatted += f"⚠️ WARNING: This response may contain unreliable information (Hallucination score: {hallucination_check['score']}/10)\n\n"
    
    formatted += f"A: {response}\n"
    
    if hallucination_check["issues"]:
        formatted += "\nPotential issues detected:\n"
        for issue in hallucination_check["issues"]:
            formatted += f"- {issue}\n"
    
    return formatted

def get_best_prompt_for_query_type(query, analysis_results):
    """Determine the best prompt type based on query characteristics"""
    query_lower = query.lower()
    
    if "symptoms" in query_lower or "signs" in query_lower:
        return "cot"  # Chain of thought for symptom analysis
    elif "medication" in query_lower or "drug" in query_lower or "medicine" in query_lower:
        return "few_shot"  # Few-shot for medication information
    elif "treatment" in query_lower or "therapy" in query_lower:
        return "meta"  # Meta-prompt for treatment options
    else:
        return analysis_results["best_overall"]  # Default to overall best

def save_example_to_log(query, response, prompt_type, hallucination_check):
    """Save an example to the log for future reference"""
    with open("evaluation/example_log.md", "a") as f:
        f.write(f"## Query: {query}\n")
        f.write(f"**Prompt type:** {prompt_type}\n")
        f.write(f"**Hallucination score:** {hallucination_check['score']}/10\n")
        f.write(f"**Response:**\n\n{response}\n\n")
        f.write("---\n\n")

def detect_hallucinations(response, query, expected_concepts=None):
    """
    Detect potential hallucinations in model responses
    Returns a hallucination score and flagged issues
    """
    hallucination_indicators = {
        "definitive_claims": [
            r"100% effective", r"always works", r"cures all", r"completely safe",
            r"guaranteed to", r"never causes", r"all patients", r"everyone with"
        ],
        "specific_numbers": [
            r"\d{2,3}% of (patients|people|cases)", r"studies show \d{2,3}%"
        ],
        "unverifiable_claims": [
            r"recent studies show", r"doctors agree that", r"research has proven",
            r"it is well established", r"it is widely accepted"
        ],
        "medical_advice": [
            r"you should", r"you must", r"you need to", r"I recommend",
            r"take \d+ (mg|milligrams)", r"increase your dosage", r"reduce your dosage"
        ]
    }
    
    issues = []
    hallucination_score = 0
    
    # Check for definitive claims
    for pattern in hallucination_indicators["definitive_claims"]:
        if re.search(pattern, response, re.IGNORECASE):
            issues.append(f"Definitive claim detected: '{re.search(pattern, response, re.IGNORECASE).group(0)}'")
            hallucination_score += 2
    
    # Check for specific unverifiable numbers
    for pattern in hallucination_indicators["specific_numbers"]:
        if re.search(pattern, response, re.IGNORECASE):
            issues.append(f"Specific unverifiable statistic: '{re.search(pattern, response, re.IGNORECASE).group(0)}'")
            hallucination_score += 1.5
    
    # Check for unverifiable claims
    for pattern in hallucination_indicators["unverifiable_claims"]:
        if re.search(pattern, response, re.IGNORECASE):
            issues.append(f"Unverifiable claim: '{re.search(pattern, response, re.IGNORECASE).group(0)}'")
            hallucination_score += 1
    
    # Check for medical advice
    for pattern in hallucination_indicators["medical_advice"]:
        if re.search(pattern, response, re.IGNORECASE):
            issues.append(f"Medical advice detected: '{re.search(pattern, response, re.IGNORECASE).group(0)}'")
            hallucination_score += 2
    
    # Check for expected concepts (if provided)
    if expected_concepts:
        found_concepts = 0
        for concept in expected_concepts:
            if concept.lower() in response.lower():
                found_concepts += 1
        
        concept_coverage = found_concepts / len(expected_concepts)
        if concept_coverage < 0.5:
            issues.append(f"Low coverage of expected medical concepts: {found_concepts}/{len(expected_concepts)}")
            hallucination_score += 1
    
    # Normalize score between 0-10
    normalized_score = min(10, hallucination_score)
    
    return {
        "score": normalized_score,
        "issues": issues,
        "severity": "High" if normalized_score > 7 else "Medium" if normalized_score > 4 else "Low"
    }

def handle_ambiguous_input(query, model_response):
    """
    Detect ambiguous responses and generate clarification prompts
    """
    # Check if response indicates uncertainty or ambiguity
    uncertainty_indicators = [
        "unclear", "ambiguous", "could mean", "need more information",
        "I'm not sure", "it depends", "could refer to", "insufficient details"
    ]
    
    # Check if the response is too short (might indicate confusion)
    is_short_response = len(model_response.split()) < 20
    
    # Check if response contains multiple conflicting possibilities
    has_multiple_possibilities = "on one hand" in model_response.lower() and "on the other hand" in model_response.lower()
    
    if (any(indicator in model_response.lower() for indicator in uncertainty_indicators) or 
        is_short_response or has_multiple_possibilities):
        
        # Generate clarification prompt based on the query type
        if "symptoms" in query.lower() or "signs" in query.lower():
            clarification = f"""I notice your question about "{query}" could benefit from more details:
            
1) Could you specify how long you've been experiencing these symptoms?
2) Are there any other symptoms you're experiencing alongside these?
3) Are you asking about general information or concerned about specific symptoms you're experiencing?

Please note I can provide medical information but cannot diagnose conditions or replace professional medical advice."""
        
        elif "medication" in query.lower() or "drug" in query.lower() or "medicine" in query.lower():
            clarification = f"""I notice your question about "{query}" could be made more specific:
            
1) Are you asking about specific dosages, side effects, or interactions?
2) Do you have any other medical conditions or take other medications that might be relevant?
3) Are you looking for general information or have concerns about a specific situation?

Please note I can provide general medication information but cannot give personalized medical advice."""
        
        else:
            clarification = f"""I notice your question about "{query}" could be interpreted in multiple ways:
            
1) Could you provide more context or specific details about your question?
2) Are you looking for general information or information about a specific situation?
3) Would it help if I explained some of the common terms or concepts related to this topic first?

Please note I can provide medical information but cannot diagnose conditions or replace professional medical advice."""
        
        return clarification
    
    return model_response

def load_test_queries(file_path="evaluation/input_queries.json"):
    """Load test queries from JSON file"""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Test queries file not found at {file_path}{Style.RESET_ALL}")
        return []
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Invalid JSON format in test queries file{Style.RESET_ALL}")
        return []

def save_results(results, file_path="evaluation/output_logs.json"):
    """Save evaluation results to JSON file"""
    try:
        with open(file_path, "w") as f:
            json.dump(results, f, indent=2)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error saving results: {str(e)}{Style.RESET_ALL}")
        return False 