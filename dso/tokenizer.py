import re

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can",
    "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above",
    "below", "between", "out", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where",
        "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "just", "about",
    "up", "this", "that", "these", "those", "it", "its", "you",
    "your", "i", "we", "they"
}

SUFFIXES = ("ing", "ed", "ly", "es", "s", "tion", "ness", "ment",
            "able", "ible", "ful", "less", "ously", "e", "ies")


def stem(word):
    w = word.lower()
    for suf in SUFFIXES:
        if len(w) > 4 and w.endswith(suf):
            w = w[:-len(suf)]
            if suf == "tion" and w.endswith("i"):
                w = w[:-1]
            break
    return w


def tokenize(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())
    result = []
    for w in words:
        if w not in STOPWORDS:
            result.append(w)
            s = stem(w)
            if s != w:
                result.append(s)
    return result
