import math
from textblob import TextBlob as tb

def term_freq(word, blob):
    # Counts the number of times a word appears in a TextBlob,
    # relative to total number of words.
    return blob.words.count(word) / len(blob.words)

def presence(word, bloblist):
    # Counts the number of blobs a word appears in
    count = 0
    for blob in bloblist:
        if word in blob.words:
            count += 1
    return count

def inv_doc_freq(word, bloblist):
    # Counts number of times a word appears across multiple
    # blobs. The more it appears frequently in other blobs,
    # the less important it is, and the lower the idf value.

    # return the log of the number of blobs divided by the number of blobs containing word
    return math.log(len(bloblist) / (presence(word, bloblist) + 1))

def tfidf(word, blob, bloblist):
    # Computes actual tfidf value using helper functions
    # which is product of tf and idf.
    tf = term_freq(word, blob)
    idf = inv_doc_freq(word, bloblist)
    return tf * idf