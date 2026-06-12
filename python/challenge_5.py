def word_count(text):
    import string
    from collections import Counter
    
    # remove punctuation
    clean_text = text.translate(str.maketrans("","",string.punctuation+"—"))
    # convert to lowercase
    clean_text = clean_text.lower()
    # compile word counter
    word_list = clean_text.split()
    # remove stop words
    stop_words = ["the", "and", "of", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are", "as", "with", "his", "they", "i"]
    clean_words = [w for w in word_list if w not in stop_words]
   
    # create dictionary return object
    word_counts = Counter(clean_words)
    word_dict = dict(word_counts)
    # create sorted tuples return object
    sorted_words = word_counts.most_common() ## Assumes sort is by word count, not word

    return word_dict, sorted_words

# Call it

test_text = ("The quick brown fox jumps over the lazy dog. "
"The dog, however, was not impressed. "
"In fact, the dog barked at the fox — and the fox ran away. "
"Meanwhile, the quick squirrel watched the whole thing from the tree.")

print(word_count(test_text))