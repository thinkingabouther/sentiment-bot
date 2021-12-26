from sentiment_analyser import SentimentAnalyzer
from youtube_reader import YouTubeReader
from statistics import median
from analysis_data import AnalysisData


class SentimentAggregator:

    def __init__(self, sentiment_endpoint, sentiment_key, youtube_endpoint, youtube_key):
        self.sentiment_analyser = SentimentAnalyzer(sentiment_endpoint, sentiment_key)
        self.youtube_reader = YouTubeReader(youtube_endpoint, youtube_key)

    def aggregate_sentiments(self, video_id: str) -> AnalysisData:
        sentiment_results = self.get_sentiments_list(video_id)
        positive_count = sum(1 for i in sentiment_results if i.sentiment == "positive")
        negative_count = sum(1 for i in sentiment_results if i.sentiment == "negative")
        neutral_count = sum(1 for i in sentiment_results if i.sentiment == "neutral")
        positive_scores = [sentiment.confidence_scores.positive for sentiment in sentiment_results]
        negative_scores = [sentiment.confidence_scores.negative for sentiment in sentiment_results]
        neutral_scores = [sentiment.confidence_scores.neutral for sentiment in sentiment_results]
        return AnalysisData(len(sentiment_results), positive_count, negative_count, neutral_count,
                            positive_scores, negative_scores, neutral_scores)

    def get_sentiments_list(self, video_id):
        comments = self.youtube_reader.read_comments_by_id(video_id)
        sentiment_results = self.sentiment_analyser.get_sentiment(comments)
        return sentiment_results
