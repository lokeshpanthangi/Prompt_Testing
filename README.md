# Medical Q&A System with Qwen3-4B

This project implements a medical question answering system using the Qwen3-4B model, exploring different prompt engineering techniques to enhance reasoning, reduce hallucination, and manage ambiguity in the medical domain.

## Project Overview

- **Domain**: Medical Question Answering
- **Model**: Qwen3-4B
- **Prompt Techniques**: Zero-shot, Few-shot, Chain-of-Thought (CoT), Meta-prompting/Self-ask
- **Evaluation Metrics**: Accuracy, Safety, Clarity, Consistency, Hallucination detection

## Setup Instructions

1. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the notebooks:
   ```
   jupyter notebook notebooks/main_medical_qa.ipynb
   ```

## Project Structure

- `README.md`: Project overview and setup instructions
- `domain_analysis.md`: Understanding of medical domain tasks
- `prompts/`: Contains different prompt templates
  - `zero_shot.txt`: Zero-shot prompt template
  - `few_shot.txt`: Few-shot prompt template
  - `cot_prompt.txt`: Chain-of-Thought prompt template
  - `meta_prompt.txt`: Meta-prompt/Self-ask template
- `evaluation/`: Evaluation resources and results
  - `input_queries.json`: Test queries for evaluation
  - `output_logs.json`: Results of prompt testing
  - `analysis_report.md`: Comparative analysis of prompt types
- `notebooks/`: Jupyter notebooks for implementation
  - `main_medical_qa.txt`: Main implementation notebook (convert to .ipynb)
  - `prompt_testing.txt`: Testing different prompt strategies (convert to .ipynb)
  - `evaluation_analysis.txt`: Results comparison notebook (convert to .ipynb)
  - `hallucination_detection.txt`: Failure case analysis notebook (convert to .ipynb)
- `src/`: Source code
  - `utils.py`: Helper functions
  - `convert_notebook.py`: Script to convert .txt files to .ipynb notebooks
- `hallucination_log.md`: Examples of hallucinations and mitigation strategies
- `requirements.txt`: Required dependencies
- `CONVERT_NOTEBOOK.md`: Instructions for converting .txt to .ipynb files

## Core Functionalities

1. **Symptom Explanation**: Describe common symptoms and their potential causes
2. **Medical Term Simplification**: Convert complex medical terminology to layman's terms
3. **General Health Guidance**: Provide evidence-based health information and wellness advice

## Safety Features

- Medical disclaimers in all responses
- Emergency symptom detection
- Avoidance of diagnostic language
- Hallucination detection and mitigation
- Ambiguity handling with clarification requests

## Converting Notebooks

Since we couldn't create .ipynb files directly, we've provided the notebook content in .txt format. To convert these to proper Jupyter notebooks:

1. Use the provided conversion script:
   ```
   python src/convert_notebook.py notebooks/main_medical_qa.txt notebooks/main_medical_qa.ipynb
   ```

2. Or follow the manual conversion instructions in `CONVERT_NOTEBOOK.md`

## Findings

The evaluation demonstrates the effectiveness of different prompt engineering techniques in the medical domain. Chain-of-Thought (CoT) prompting generally performs best for complex medical questions, while Few-shot prompting works well for standardized responses. See `evaluation/analysis_report.md` for detailed findings and recommendations. 