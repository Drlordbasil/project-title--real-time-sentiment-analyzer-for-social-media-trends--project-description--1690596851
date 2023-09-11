import tweepy
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import csv
from fpdf import FPDF


class RealTimeSentimentAnalyzer:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
        self.sia = SentimentIntensityAnalyzer()
        self.tweets = []

    def retrieve_tweets(self, duration, filters):
        tweet_count = 0
        while tweet_count < duration:
            new_tweets = self.api.search(q=filters, count=100)
            self.tweets.extend(new_tweets)
            tweet_count += len(new_tweets)

    def analyze_sentiment(self):
        sentiment_scores = [self.sia.polarity_scores(
            tweet.text)['compound'] for tweet in self.tweets]
        return sentiment_scores

    def generate_sentiment_visualization(self, sentiment_scores):
        plt.plot(sentiment_scores)
        plt.title('Sentiment Analysis')
        plt.xlabel('Tweet')
        plt.ylabel('Sentiment Score')
        plt.show()

    def generate_summary_report(self, sentiment_scores):
        negative_count = sum(score < 0 for score in sentiment_scores)
        positive_count = sum(score > 0 for score in sentiment_scores)
        neutral_count = sum(score == 0 for score in sentiment_scores)

        report = f"Total Tweets: {len(self.tweets)}\n"
        report += f"Positive Tweets: {positive_count}\n"
        report += f"Negative Tweets: {negative_count}\n"
        report += f"Neutral Tweets: {neutral_count}\n"

        return report

    def export_data_csv(self, sentiment_scores):
        with open('sentiment_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tweet', 'Sentiment Score'])
            writer.writerows([[tweet.text, score]
                             for tweet, score in zip(self.tweets, sentiment_scores)])

    def export_data_pdf(self, sentiment_scores, report):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Sentiment Analysis", ln=True, align='C')
        pdf.multi_cell(0, 10, txt=report)

        for tweet, score in zip(self.tweets, sentiment_scores):
            pdf.ln(5)
            pdf.multi_cell(
                0, 10, txt=f"{tweet.text}\nSentiment Score: {score}")

        pdf.output("sentiment_analysis.pdf")

    def run(self, duration, filters):
        self.retrieve_tweets(duration, filters)
        sentiment_scores = self.analyze_sentiment()
        self.generate_sentiment_visualization(sentiment_scores)
        report = self.generate_summary_report(sentiment_scores)
        self.export_data_csv(sentiment_scores)
        self.export_data_pdf(sentiment_scores, report)


if __name__ == "__main__":
    consumer_key = 'your_consumer_key'
    consumer_secret = 'your_consumer_secret'
    access_token = 'your_access_token'
    access_token_secret = 'your_access_token_secret'

    analyzer = RealTimeSentimentAnalyzer(
        consumer_key, consumer_secret, access_token, access_token_secret)
    duration = int(input("Enter the data retrieval duration (in minutes): "))
    filters = input("Enter the user-defined filters: ")
    analyzer.run(duration, filters)
