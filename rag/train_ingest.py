#!/usr/bin/env python3
"""
GramSetu AI - High-Precision Knowledge Ingestion & Training Engine
Enables instant custom training by updating:
1. Python Backend RAG (rag/knowledge.py)
2. Frontend Offline PWA (knowledge_data.js)
3. SQLite Persistence (gramsetu.db)
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime

# Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.database import save_knowledge_node, get_all_knowledge_nodes
import rag.knowledge as py_rag

KNOWLEDGE_PY_PATH = os.path.join(BASE_DIR, "rag", "knowledge.py")
KNOWLEDGE_JS_PATH = os.path.join(BASE_DIR, "knowledge_data.js")

STOP_WORDS = {
    "a", "an", "the", "in", "on", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to", "from", "up",
    "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same",
    "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now",
    "kya", "hai", "kaise", "kare", "karein", "aur", "ki", "ka", "ke", "ko", "se", "mein",
    "me", "par", "h", "tha", "the", "thi", "kya", "kyu", "kyon", "kahan", "kitna", "kitni"
}

def extract_keywords_auto(text: str, max_keywords: int = 15) -> list:
    """Extracts top significant words from English/Hindi text for keyword matching."""
    if not text:
        return []
    words = re.findall(r'[a-zA-Z0-9\u0900-\u097F]+', text.lower())
    filtered = [w for w in words if len(w) > 2 and w not in STOP_WORDS]
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for w in filtered:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    return unique[:max_keywords]

def slugify(text: str) -> str:
    """Creates a clean ID slug."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')[:50] or "custom_node"

def load_existing_python_nodes() -> list:
    """Loads existing KNOWLEDGE_BASE items from rag/knowledge.py."""
    try:
        return list(py_rag.KNOWLEDGE_BASE)
    except Exception:
        return []

def sync_to_python_file(all_nodes: list):
    """Rewrites rag/knowledge.py safely with updated KNOWLEDGE_BASE."""
    code_lines = [
        '"""',
        'GramSetu AI - Comprehensive Multidisciplinary Knowledge & Offline RAG Engine',
        'Auto-trained & synced via rag/train_ingest.py',
        '"""',
        '',
        'import re',
        '',
        'KNOWLEDGE_BASE = ['
    ]

    for item in all_nodes:
        node_id = item.get("id", "custom_id")
        category = item.get("category", "general")
        title = item.get("title", "Untitled")
        keywords = item.get("keywords", [])
        summary = item.get("summary", "")
        response = item.get("response", "")

        # Format item dictionary
        code_lines.append('    {')
        code_lines.append(f'        "id": {json.dumps(node_id)},')
        code_lines.append(f'        "category": {json.dumps(category)},')
        code_lines.append(f'        "title": {json.dumps(title)},')
        code_lines.append(f'        "keywords": {json.dumps(keywords, ensure_ascii=False)},')
        code_lines.append(f'        "summary": {json.dumps(summary, ensure_ascii=False)},')
        code_lines.append(f'        "response": {json.dumps(response, ensure_ascii=False)}')
        code_lines.append('    },')

    code_lines.append(']')
    code_lines.append('')
    code_lines.append('GENERIC_STOP_KEYWORDS = {"python", "javascript", "code", "function", "biology", "science", "medical", "drug", "medicine", "first aid", "soil", "crop", "farming"}')
    code_lines.append('')
    code_lines.append('def search_knowledge(query: str, threshold: int = 30) -> dict:')
    code_lines.append('    """')
    code_lines.append('    Multidisciplinary keyword and phrase matching engine with specific term weighting.')
    code_lines.append('    """')
    code_lines.append('    if not query:')
    code_lines.append('        return None')
    code_lines.append('')
    code_lines.append('    clean = query.strip().lower()')
    code_lines.append('    words = [w for w in re.findall(r\'[a-zA-Z0-9\\u0900-\\u097F]+\', clean) if len(w) > 2]')
    code_lines.append('    if not words:')
    code_lines.append('        return None')
    code_lines.append('')
    code_lines.append('    best_item = None')
    code_lines.append('    best_score = 0')
    code_lines.append('')
    code_lines.append('    for item in KNOWLEDGE_BASE:')
    code_lines.append('        score = 0')
    code_lines.append('        title_lower = item.get("title", "").lower()')
    code_lines.append('')
    code_lines.append('        # Direct phrase match in title')
    code_lines.append('        if clean in title_lower:')
    code_lines.append('            score += 80')
    code_lines.append('')
    code_lines.append('        # Match keywords using exact word boundaries with full Unicode support')
    code_lines.append('        for kw in item.get("keywords", []):')
    code_lines.append('            kw_lower = kw.lower()')
    code_lines.append('            is_generic = kw_lower in GENERIC_STOP_KEYWORDS')
    code_lines.append('            ')
    code_lines.append('            # Full phrase match')
    code_lines.append('            if len(kw_lower.split()) > 1:')
    code_lines.append('                if kw_lower in clean:')
    code_lines.append('                    score += 60')
    code_lines.append('            else:')
    code_lines.append('                # Standalone word boundary match with Unicode support')
    code_lines.append('                pattern = r"(?:^|[^\\w\\u0900-\\u097F\\u0A00-\\u0A7F])" + re.escape(kw_lower) + r"(?:$|[^\\w\\u0900-\\u097F\\u0A00-\\u0A7F])"')
    code_lines.append('                if re.search(pattern, clean) or (kw_lower in clean and len(kw_lower) >= 4):')
    code_lines.append('                    score += 15 if is_generic else 45')
    code_lines.append('')
    code_lines.append('        if score > best_score:')
    code_lines.append('            best_score = score')
    code_lines.append('            best_item = item')
    code_lines.append('')
    code_lines.append('    if best_score >= threshold:')
    code_lines.append('        return best_item')
    code_lines.append('    return None')
    code_lines.append('')

    with open(KNOWLEDGE_PY_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(code_lines))

def sync_to_js_file(all_nodes: list):
    """Rewrites knowledge_data.js for offline browser PWA engine."""
    js_content = "// Comprehensive Multi-Domain Knowledge Base\n// 100% Offline Auto-Trained Intelligence Engine\n\n"
    js_content += "var COMPREHENSIVE_KNOWLEDGE_BASE = "
    js_content += json.dumps(all_nodes, indent=2, ensure_ascii=False)
    js_content += ";\n"
    
    with open(KNOWLEDGE_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)

def sync_to_sqlite(all_nodes: list):
    """Persists all nodes to local SQLite database."""
    for item in all_nodes:
        save_knowledge_node(
            node_id=item["id"],
            category=item.get("category", "general"),
            title=item.get("title", "Untitled"),
            keywords=item.get("keywords", []),
            summary=item.get("summary", ""),
            response=item.get("response", ""),
            tags=item.get("tags", [])
        )

def train_and_ingest_nodes(new_items: list) -> dict:
    """
    Main pipeline to train & ingest new knowledge items.
    Updates Python RAG, JS Browser Engine, and SQLite.
    """
    if not isinstance(new_items, list):
        new_items = [new_items]

    existing = load_existing_python_nodes()
    existing_map = {item["id"]: item for item in existing}

    added_count = 0
    updated_count = 0

    for raw in new_items:
        # Handle QA instruction format as well
        title = raw.get("title") or raw.get("question") or raw.get("instruction") or "Custom Knowledge Item"
        response = raw.get("response") or raw.get("answer") or raw.get("output") or ""
        category = raw.get("category") or "general"
        node_id = raw.get("id") or f"{category}_{slugify(title)}"

        keywords = raw.get("keywords", [])
        if not keywords:
            keywords = extract_keywords_auto(f"{title} {response}")

        summary = raw.get("summary", "")
        if not summary and response:
            summary = response.split("\n")[0][:180] + "..."

        node = {
            "id": node_id,
            "category": category,
            "title": title,
            "keywords": keywords,
            "summary": summary,
            "response": response
        }

        if "tags" in raw:
            node["tags"] = raw["tags"]

        if node_id in existing_map:
            updated_count += 1
        else:
            added_count += 1

        existing_map[node_id] = node

    full_list = list(existing_map.values())

    # 3-Way Sync
    sync_to_python_file(full_list)
    sync_to_js_file(full_list)
    sync_to_sqlite(full_list)

    # Reload memory module
    try:
        import importlib
        importlib.reload(py_rag)
    except Exception:
        pass

    return {
        "status": "success",
        "added": added_count,
        "updated": updated_count,
        "total_knowledge_nodes": len(full_list)
    }

def ingest_from_json_file(file_path: str) -> dict:
    """Ingests a JSON array or JSONL file of knowledge/QA items."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    items = []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content.startswith("["):
            items = json.loads(content)
        else:
            # Try JSONL
            for line in content.splitlines():
                if line.strip():
                    items.append(json.loads(line))

    return train_and_ingest_nodes(items)

def ingest_from_text_file(file_path: str, category: str = "general") -> dict:
    """
    Parses sections or Q&A in a text/markdown file and creates knowledge nodes.
    Supports '# Heading' or 'Q: ... A: ...' blocks.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    items = []
    # Try Q&A block regex
    qa_blocks = re.findall(r'(?:Q|Question|प्रश्न):\s*(.+?)\n(?:A|Answer|उत्तर):\s*(.+?)(?=\n(?:Q|Question|प्रश्न):|\Z)', text, re.DOTALL | re.IGNORECASE)
    
    if qa_blocks:
        for q, a in qa_blocks:
            q_clean = q.strip()
            a_clean = a.strip()
            items.append({
                "title": q_clean,
                "response": a_clean,
                "category": category
            })
    else:
        # Split by Markdown H1/H2/H3
        sections = re.split(r'\n(?=#{1,3}\s+)', text)
        for sec in sections:
            sec = sec.strip()
            if not sec:
                continue
            lines = sec.split("\n", 1)
            title = re.sub(r'^#{1,3}\s*', '', lines[0]).strip()
            body = lines[1].strip() if len(lines) > 1 else lines[0]
            items.append({
                "title": title,
                "response": body,
                "category": category
            })

    return train_and_ingest_nodes(items)

def interactive_cli():
    """Interactive Command Line Training Wizard."""
    print("=" * 65)
    print("🌾 GRAMSETU AI - KNOWLEDGE INGESTION & TRAINING ENGINE 🧠")
    print("=" * 65)
    print("Select an option:")
    print("1. Add a single Knowledge / Q&A Node interactively")
    print("2. Train / Ingest from a JSON / JSONL file")
    print("3. Ingest from a Text / Markdown document")
    print("4. Test search / query matching accuracy")
    print("5. Exit")
    print("-" * 65)

    choice = input("Enter choice (1-5): ").strip()

    if choice == "1":
        print("\n--- Enter Node Details ---")
        category = input("Category (agriculture/tech/coding/biology/pharmacy/medical/general) [agriculture]: ").strip() or "agriculture"
        title = input("Title / Topic (e.g. Mustard Sowing & Irrigation Guide): ").strip()
        keywords_str = input("Keywords (comma separated) [Leave blank for auto]: ").strip()
        print("Detailed Solution / Knowledge Response (Type text, enter EOF or empty line twice to finish):")
        
        response_lines = []
        while True:
            try:
                line = input()
                if line == "EOF":
                    break
                response_lines.append(line)
                if len(response_lines) >= 2 and response_lines[-1] == "" and response_lines[-2] == "":
                    response_lines.pop()
                    response_lines.pop()
                    break
            except EOFError:
                break
        
        response = "\n".join(response_lines).strip()
        keywords = [k.strip() for k in keywords_str.split(",") if k.strip()] if keywords_str else extract_keywords_auto(f"{title} {response}")

        item = {
            "id": f"{category}_{slugify(title)}",
            "category": category,
            "title": title,
            "keywords": keywords,
            "summary": response.split("\n")[0][:150] + "...",
            "response": response
        }

        res = train_and_ingest_nodes([item])
        print(f"\n✅ Training Successful! Synced 3-way. Total nodes: {res['total_knowledge_nodes']}")

    elif choice == "2":
        path = input("Enter path to JSON / JSONL file: ").strip()
        try:
            res = ingest_from_json_file(path)
            print(f"\n✅ Batch Ingestion Complete! Added: {res['added']}, Updated: {res['updated']}, Total: {res['total_knowledge_nodes']}")
        except Exception as e:
            print(f"❌ Error: {e}")

    elif choice == "3":
        path = input("Enter path to TXT / Markdown file: ").strip()
        cat = input("Category [general]: ").strip() or "general"
        try:
            res = ingest_from_text_file(path, category=cat)
            print(f"\n✅ Document Ingestion Complete! Added: {res['added']}, Updated: {res['updated']}, Total: {res['total_knowledge_nodes']}")
        except Exception as e:
            print(f"❌ Error: {e}")

    elif choice == "4":
        query = input("Enter search test query (e.g. gehu ki buwai, arduino dht22, paracetamol): ").strip()
        match = py_rag.search_knowledge(query)
        if match:
            print(f"\n🎯 MATCH FOUND (Category: {match.get('category')}):")
            print(f"📌 Title: {match.get('title')}")
            print(f"🔑 Keywords: {match.get('keywords')}")
            print(f"📄 Response Preview:\n{match.get('response')[:250]}...")
        else:
            print("❌ No match found with current threshold.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="GramSetu AI Knowledge Ingestion & Training CLI")
        parser.add_argument("--json", help="Path to JSON or JSONL file to ingest")
        parser.add_argument("--text", help="Path to text or markdown file to ingest")
        parser.add_argument("--category", default="general", help="Category for text ingestion")
        parser.add_argument("--test", help="Test a search query")
        args = parser.parse_args()

        if args.json:
            res = ingest_from_json_file(args.json)
            print(json.dumps(res, indent=2))
        elif args.text:
            res = ingest_from_text_file(args.text, category=args.category)
            print(json.dumps(res, indent=2))
        elif args.test:
            match = py_rag.search_knowledge(args.test)
            print(json.dumps(match, indent=2, ensure_ascii=False) if match else "No match")
    else:
        interactive_cli()
