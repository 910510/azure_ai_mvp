import pandas as pd
import re
import argparse

def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r"[^ㄱ-ㅎ가-힣a-zA-Z0-9\\s]", "", text)
    return text.strip()

def main(raw_input_path, output_path):
    df = pd.read_csv(raw_input_path)
    df["clean_title"] = df["title"].apply(clean_text)
    df["clean_description"] = df["description"].apply(clean_text)
    df["clean_transcript"] = df["transcript"].apply(clean_text)
    df.to_csv(output_path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_input_path")
    parser.add_argument("--output_path")
    args = parser.parse_args()
    main(args.raw_input_path, args.output_path)