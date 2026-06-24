from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ATSScorer:
      def calculate_score(
                self,
                jd,
                resume_text
                ):
             docs = [jd, resume_text]
             Tfidf = TfidfVectorizer()
             matrix = Tfidf.fit_transform(docs)
             similarity= cosine_similarity(
                    matrix[0:1],
                    matrix[1:2]
                    )
             return round(
                    similarity[0][0]*100,
                    2
                    )