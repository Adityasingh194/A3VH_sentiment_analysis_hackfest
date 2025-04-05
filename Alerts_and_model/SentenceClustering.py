from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

class SentenceClustering:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2', similarity_threshold=0.75, min_cluster_size=1):
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = similarity_threshold
        self.min_cluster_size = min_cluster_size

    def encode_sentences(self, sentences):
        self.sentences = sentences
        self.embeddings = self.model.encode(sentences)
        return self.embeddings

    def cluster_sentences(self):
        sim_matrix = cosine_similarity(self.embeddings)
        n = len(self.sentences)
        visited = [False] * n
        self.clusters = []

        def dfs(i, cluster):
            visited[i] = True
            cluster.append(i)
            for j in range(n):
                if not visited[j] and sim_matrix[i][j] >= self.similarity_threshold:
                    dfs(j, cluster)

        for i in range(n):
            if not visited[i]:
                cluster = []
                dfs(i, cluster)
                self.clusters.append(cluster)
        return self.clusters

    def get_representative_sentences(self):
        representatives = []
        for cluster in self.clusters:
            if len(cluster) >= self.min_cluster_size:
                cluster_embeddings = [self.embeddings[i] for i in cluster]
                cluster_sentences = [self.sentences[i] for i in cluster]
                centroid = np.mean(cluster_embeddings, axis=0)
                similarities = cosine_similarity([centroid], cluster_embeddings)[0]
                rep_idx = np.argmax(similarities)
                representatives.append(cluster_sentences[rep_idx])
        return representatives