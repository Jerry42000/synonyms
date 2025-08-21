# Semantic Similarity Synonym Selection

When you see a digital dictionary suggest alternatives, a writing assistant pick better wording, or a search engine understand “car” ≈ “vehicle,” you are benefiting from semantic similarity. This project learns word meaning from large texts and then answers multiple-choice synonym questions (like TOEFL) by picking the option most similar in meaning to the prompt word.

Feed the system roughly ~100000 words of text (combined novels/articles are fine). With that scale, you can expect around ~70% correct guesses on synonym questions.

*How it works

-->Build a semantic descriptor for each word: a dictionary counting how often other words co-occur with it in the same sentence (from your training corpus). Then compare words by cosine similarity of those vectors. The starter spec describes this pipeline and the cosine metric. 

-->Core functions (in synonyms.py): vector norm & cosine, building descriptors from sentences/files, and choosing the most similar choice.
