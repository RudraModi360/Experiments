import csv
import sys

def get_sentiment(rating, text):
    # Rating-based / text-based sentiment
    # rating 4-5: Positive
    # rating 3: Neutral
    # rating 1-2: Negative
    # Score between -1.0 and 1.0 (e.g. (rating - 3) / 2)
    # Let's refine score calculation or use simple heuristics
    score = (int(rating) - 3) / 2.0  # 5->1.0, 4->0.5, 3->0.0, 2->-0.5, 1->-1.0
    if rating >= 4:
        label = 'positive'
    elif rating == 3:
        label = 'neutral'
    else:
        label = 'negative'
    return label, round(score, 2)

def main():
    rows = []
    with open('reviews.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    sentiment_rows = []
    for r in rows:
        label, score = get_sentiment(int(r['rating']), r['text'])
        sentiment_rows.append({
            'id': r['id'],
            'text': r['text'],
            'rating': r['rating'],
            'sentiment_label': label,
            'sentiment_score': score
        })

    # Write sentiment.csv
    with open('sentiment.csv', mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'text', 'rating', 'sentiment_label', 'sentiment_score'])
        writer.writeheader()
        writer.writerows(sentiment_rows)

    print("sentiment.csv generated successfully.")

if __name__ == '__main__':
    main()
