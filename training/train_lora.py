#!/usr/bin/env python3
"""
GramSetu AI - LoRA / QLoRA SFT Fine-Tuning Script
Fine-tunes Qwen 2.5 3B / Llama 3.2 on GramSetu's 10-Lakh Persona Dataset.
Compatible with Google Colab (Free T4 GPU), Local CUDA GPU, and Apple Silicon MPS.
"""

import os
import sys
import torch

def check_environment():
    print("=" * 60)
    print("🌾 GRAMSETU AI - LORA FINE-TUNING PIPELINE")
    print("=" * 60)
    
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"🚀 CUDA GPU Detected: {device_name} ({vram:.1f} GB VRAM)")
        return "cuda"
    elif torch.backends.mps.is_available():
        print("🍎 Apple Silicon MPS Detected (Running on Mac M-Series GPU)")
        return "mps"
    else:
        print("⚠️ No GPU detected. Running on CPU (Fine-tuning is best run on Google Colab with free T4 GPU).")
        return "cpu"

def train_model(
    base_model_name: str = "Qwen/Qwen2.5-3B-Instruct",
    dataset_path: str = "dataset/train_10lakh_personas.jsonl",
    output_dir: str = "models/gramsetu-trained-lora",
    epochs: int = 3,
    batch_size: int = 2
):
    try:
        from datasets import load_dataset
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            TrainingArguments,
            BitsAndBytesConfig
        )
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from trl import SFTTrainer
    except ImportError:
        print("\n❌ Missing required training libraries. Install them via:")
        print("pip install torch transformers datasets peft trl bitsandbytes accelerate")
        return

    device = check_environment()
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n📂 Loading Dataset: {dataset_path}...")
    raw_dataset = load_dataset("json", data_files=dataset_path, split="train")

    def format_prompts(batch):
        formatted = []
        for inst, inp, out in zip(batch["instruction"], batch["input"], batch["output"]):
            sys_msg = "You are GramSetu AI, an expert agricultural, rural and multidisciplinary intelligence assistant."
            user_msg = f"{inst}\n({inp})" if inp else inst
            chat_text = f"<|im_start|>system\n{sys_msg}<|im_end|>\n<|im_start|>user\n{user_msg}<|im_end|>\n<|im_start|>assistant\n{out}<|im_end|>"
            formatted.append(chat_text)
        return {"text": formatted}

    dataset = raw_dataset.map(format_prompts, batched=True)

    print(f"🧠 Loading Base Model: {base_model_name}...")
    
    # 4-bit Quantization Config (QLoRA)
    bnb_config = None
    if device == "cuda":
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )

    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=bnb_config if device == "cuda" else None,
        device_map="auto" if device == "cuda" else None,
        torch_dtype=torch.float16 if device in ["cuda", "mps"] else torch.float32,
        trust_remote_code=True
    )

    if device == "cuda":
        model = prepare_model_for_kbit_training(model)

    # LoRA Config
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        optim="paged_adamw_8bit" if device == "cuda" else "adamw_torch",
        logging_steps=10,
        learning_rate=2e-4,
        weight_decay=0.01,
        fp16=(device == "cuda"),
        bf16=False,
        max_grad_norm=0.3,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        save_strategy="epoch",
        report_to="none"
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="text",
        max_seq_length=1024,
        tokenizer=tokenizer,
        args=training_args
    )

    print("\n🔥 Starting GramSetu LoRA Fine-Tuning...")
    trainer.train()

    print(f"\n💾 Saving Trained LoRA Adapter to: {output_dir}")
    trainer.model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("\n🎉 Training Complete! Model is ready for GGUF export and Ollama deployment.")

if __name__ == "__main__":
    train_model()
