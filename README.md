# D3 Knowledge SFT + RAG Integration

A specialized fine-tuning project that combines Supervised Fine-Tuning (SFT) with Retrieval-Augmented Generation (RAG) for D3 database documentation. This project creates a domain-specific language model capable of answering questions about D3 database operations and syntax.

## 🎯 Project Overview

This project enhances Llama 3.1 (8B) with domain-specific knowledge of D3 database systems by:
- Fine-tuning on custom Q&A pairs generated from D3 documentation
- Implementing RAG for dynamic context retrieval
- Using structured data extraction and AI-assisted dataset preparation

## 🏗️ Architecture

```
D3 Documentation → Data Extraction → SFT Dataset → Fine-tuned Model
                                          ↓
PDF Manual → RAG Database → Context Retrieval → Enhanced Inference
```

## 📊 Dataset Preparation

### SFT Dataset Creation
- **Source**: D3 Online Reference Manual
- **Extraction**: `pandas` + `async_playwright` for web scraping
- **Enhancement**: Claude 4 for Q&A pair generation
- **Format**: Structured training pairs following SFT best practices

### RAG Database Construction
- **Source**: D3 Manual PDF files
- **Structure**: JSON format with comprehensive metadata
- **Schema**:
  ```json
  {
    "id": "doc_0598",
    "title": " - GE",
    "content": "denotes a 'greater than or equal' conditional between two elements.",
    "syntax": "Syntax\nexpression GE expression",
    "examples": ["Example\nif date ge \"6/1\" then print \"yes\""],
    "options": "",
    "metadata": {
      "level": 1,
      "page_number": 284,
      "segment_type": "content",
      "section_component": "FlashBASIC",
      "has_syntax": true,
      "has_examples": true,
      "has_options": false,
      "example_count": 1,
      "content_length": 67,
      "syntax_length": 31,
      "options_length": 0
    }
  }
  ```

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas playwright transformers torch datasets
playwright install
```

### Base Model
This project uses the Llama 3.1 (8B) Alpaca configuration as the foundation:
- **Notebook**: [Llama3.1_(8B)-Alpaca.ipynb](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Llama3.1_(8B)-Alpaca.ipynb)
- **Model**: Meta-Llama/Llama-3.1-8B-Instruct
- **Fine-tuning**: LoRA/QLoRA for efficient training

### Training Process

1. **Data Collection**
   ```python
   # Web scraping D3 documentation
   from playwright.async_api import async_playwright
   import pandas as pd
   
   # Extract content from D3 Online Reference Manual
   # Clean and structure data for SFT preparation
   ```

2. **SFT Dataset Generation**
   - Load extracted D3 documentation
   - Use Claude 4 API with custom prompt (`prompt_sft.txt`)
   - Generate high-quality Q&A pairs
   - Format for Alpaca-style training

3. **Model Fine-tuning**
   - Follow the Colab notebook structure
   - Replace dataset with D3-specific Q&A pairs
   - Maintain same hyperparameters and training loop

4. **RAG Integration**
   - Build vector database from PDF extractions
   - Implement retrieval mechanism
   - Use same prompt template for consistency

## 📁 Project Structure

```
├── data/
│   ├── d3_manual.pdf                 # Source PDF documentation
│   ├── scraped_content.csv          # Raw scraped data
│   ├── sft_dataset.json            # Processed SFT training data
│   └── rag_database.json           # RAG vector database
├── prompts/
│   └── prompt_sft.txt              # SFT prompt template
├── scripts/
│   ├── scrape_d3_docs.py          # Web scraping script
│   ├── generate_qa_pairs.py       # Claude 4 Q&A generation
│   ├── prepare_sft_data.py        # SFT dataset preparation
│   └── extract_pdf_rag.py         # RAG database creation
├── notebooks/
│   └── d3_sft_training.ipynb      # Modified Alpaca training notebook
├── models/
│   └── d3_llama_sft/              # Fine-tuned model output
└── README.md
```

## 🔧 Configuration

### SFT Prompt Template
The project uses a consistent prompt template stored in `prompt_sft.txt` for both:
- Training data generation (with Claude 4)
- Model inference (fine-tuned model)

### Training Parameters
- **Base Model**: Llama 3.1 8B Instruct
- **Method**: LoRA fine-tuning
- **Dataset Size**: Generated from complete D3 documentation
- **Training Steps**: Optimized for domain knowledge retention

## 💡 Usage

### Training
```python
# Follow the modified Alpaca notebook with D3 dataset
# Ensure prompt consistency between SFT and inference
```

### Inference with RAG
```python
# Load fine-tuned model
# Retrieve relevant context from RAG database
# Apply same prompt template for consistent responses
```

## 🎯 Results

The fine-tuned model demonstrates improved performance on:
- D3 database syntax questions
- FlashBASIC programming queries
- System configuration and setup
- Error troubleshooting and debugging

## 🤝 Contributing

This is a personal research project focused on domain-specific fine-tuning techniques. The methodology can be adapted for other technical documentation domains.

## 📄 License

This project is for educational and research purposes. Please respect the original D3 documentation licensing terms.

## 🔗 References

- [Original Alpaca Training Notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Llama3.1_(8B)-Alpaca.ipynb)
- D3 Online Reference Manual
- Meta Llama 3.1 Model Documentation

---

**Note**: This project demonstrates the integration of traditional fine-tuning with modern RAG techniques for specialized domain knowledge enhancement.
