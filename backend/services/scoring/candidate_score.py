from sklearn.metrics.pairwise import cosine_similarity

def similarity(a,b):

    return cosine_similarity(
[a],
[b]
)[0][0]