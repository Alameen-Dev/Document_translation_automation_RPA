import os
import docx
from transformers import T5Tokenizer, T5ForConditionalGeneration

def load_model_and_tokenizer():
    model_name = 't5-small'  # Use 't5-base' or 't5-large' for better accuracy
    tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return model, tokenizer

def translate_text(text, model, tokenizer):
    input_text = f"translate English to Spanish: {text}"
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    translated = model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

def translate_docx(input_file, output_directory):
    model, tokenizer = load_model_and_tokenizer()
    doc = docx.Document(input_file)
    
    for i, paragraph in enumerate(doc.paragraphs):
        for j, run in enumerate(paragraph.runs):
            if run.text.strip():  # Only translate non-empty runs
                translated_text = translate_text(run.text, model, tokenizer)
                run.text = translated_text  # Replace original text with translated text
    
    base_output_filename = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_directory, f"{base_output_filename}_translated_{i + 1}.docx")
    doc.save(output_file)
    
    return output_file  # Return the path of the saved file

