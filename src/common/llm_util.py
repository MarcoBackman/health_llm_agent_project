class LlmUtil:

    @staticmethod
    def cosine_similarity(vec1, vec2):
        """
        Compute cosine similarity between two vectors.

        :param vec1: First vector.
        :param vec2: Second vector.
        :return: Cosine similarity as a float.
        """
        from numpy import dot
        from numpy.linalg import norm

        return dot(vec1, vec2) / (norm(vec1) * norm(vec2))
