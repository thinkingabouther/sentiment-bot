from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentResult


class SentimentAnalyzer:
    def __init__(self, endpoint, key):
        self.text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def get_sentiment(self, text: str) -> AnalyzeSentimentResult:
        docs = self.text_analytics_client.analyze_sentiment([text], show_opinion_mining=True)
        return docs
