import pdfplumber
import json

def extract_text_with_pages(pdf_path):
    output = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                output.append({
                    "page": i + 1,
                    "text": text.strip()
                })
    return output

if __name__ == "__main__":
    data = extract_text_with_pages("data/NR-12.pdf")
    with open("data/nr12_text.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ Texto extraído e salvo em data/nr12_text.json")
