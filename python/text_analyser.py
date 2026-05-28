import re
from collections import Counter

def analyze_document(text):
    # Basic metrics
    words = re.findall(r'\w+', text.lower())
    
    # AI Training 'Red-Flag' Words
    red_flags = ['very', 'actually', 'basically', 'really', 'important']
    found_flags = {word: words.count(word) for word in red_flags if words.count(word) > 0}

    print(f"--- Document Analysis ---")
    print(f"Total Words: {len(words)}")
    print(f"Top 5 Words: {Counter(words).most_common(5)}")
    print(f"Red-Flag Words Found: {found_flags}")

if __name__ == "__main__":
    # Test with a snippet from your book or article
    sample = "Actually, writing is very important. It is basically the core of communication."
    analyze_document(sample)