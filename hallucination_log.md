# Medical QA System Hallucination Log

This document catalogs examples of hallucinations detected during evaluation and provides strategies to mitigate them.

## Common Hallucination Types

### 1. Definitive Medical Claims

**Example:** *"Taking vitamin C will always prevent colds."*

**Issue:** Makes absolute claims about medical efficacy that are not supported by evidence.

**Mitigation:**
- Use qualifying language: "may help," "some studies suggest," "evidence indicates"
- Express appropriate uncertainty: "while research is ongoing," "results are mixed"
- Include context about evidence quality: "small studies have shown," "large clinical trials have demonstrated"

### 2. Specific Statistics Without Sources

**Example:** *"Studies show 87% of patients recover within two weeks."*

**Issue:** Provides precise statistics that cannot be verified or may be fabricated.

**Mitigation:**
- Use ranges instead of specific percentages
- Qualify with "approximately" or "roughly"
- Only include statistics that are widely accepted in medical literature
- Avoid citing specific studies without proper attribution

### 3. Medical Advice

**Example:** *"You should take 500mg of this medication twice daily."*

**Issue:** Provides specific medical recommendations that should come from healthcare professionals.

**Mitigation:**
- Reframe as general information: "This medication is typically prescribed as..."
- Include disclaimers: "A healthcare provider determines appropriate dosing"
- Focus on explaining mechanisms rather than making recommendations
- Use phrases like "commonly," "generally," or "typically" rather than directives

### 4. Overgeneralization

**Example:** *"All headaches are caused by stress."*

**Issue:** Oversimplifies complex medical conditions with multiple potential causes.

**Mitigation:**
- Acknowledge multiple factors: "Headaches can have various causes, including..."
- Discuss common vs. rare causes
- Use phrases like "may be associated with" instead of definitive causation
- Present information in terms of possibilities rather than certainties

### 5. Non-existent Treatments or Procedures

**Example:** *"The XYZ-5000 procedure is the newest treatment for arthritis."*

**Issue:** References treatments, procedures, or medications that don't exist.

**Mitigation:**
- Stick to well-established medical terminology
- Avoid naming specific brands or proprietary treatments
- Focus on mechanism classes rather than specific interventions
- Express uncertainty when discussing cutting-edge treatments

## Hallucination Reduction Strategies

### 1. Knowledge Grounding
- Implement a verification system against a trusted medical knowledge base
- Limit responses to information that can be verified against established medical literature
- When uncertain, explicitly state the limitations of available information

### 2. Uncertainty Expression
- Train the model to express appropriate levels of uncertainty
- Use probabilistic language when discussing medical topics
- Include phrases like "based on current understanding" or "according to available evidence"
- Acknowledge when questions fall outside the scope of reliable information

### 3. Scope Limitation
- Clearly distinguish between providing medical information vs. medical advice
- Include disclaimers about consulting healthcare professionals
- Avoid diagnostic language or treatment recommendations
- Focus on educational content rather than personalized guidance

### 4. Response Constraints
- Implement structured output formats that separate facts from interpretations
- Use templates that encourage balanced presentation of information
- Include sections for "what we know" vs. "what is still uncertain"
- Require citations or references for specific claims

### 5. Post-processing Filters
- Implement detection systems for common hallucination patterns
- Flag responses containing specific numbers without context
- Check for absolute language like "always," "never," or "guaranteed"
- Identify and remove unfounded medical claims 