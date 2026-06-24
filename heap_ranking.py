import heapq
class HeapRanking:
    
    @staticmethod
    def top_candidates(
        candidates,
        k=5
    ):
        
        return heapq.nlargest(
            k,
            candidates,
            key= lambda x: x.score
        )