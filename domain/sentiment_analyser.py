from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentResult


class SentimentAnalyzer:
    MAX_BATCH_SIZE = 10

    def __init__(self, endpoint, key):
        self.text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def get_sentiment(self, docs_list: [str]) -> [AnalyzeSentimentResult]:
        batch_size = self.MAX_BATCH_SIZE
        result = []
        for idx in range(0, len(docs_list), batch_size):
            batch = docs_list[idx: idx + batch_size]
            docs = self.text_analytics_client.analyze_sentiment(batch, show_opinion_mining=True)
            result += docs
        return result
