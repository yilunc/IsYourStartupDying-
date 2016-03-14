# IsYourStartupDying-

### Classifier to answer the question:
Is it dying or nah?

Uses ML neighbor classifier algorithm to let budding entrepreneurs if their startup is successful or not, just enter your company details in, cross your fingers and read your result which was calculated based on pre-existing database of over 73,000 startups.

#### Current accuracy

98.941% accuracy using k=9.

#### Usage
For testing:

```$ python classify-startup.py test {k_value}```

To classify your company:

```$ python classify-startup.py name status market country city funding_value funding_rounds first_round_date last_round_date {k_value}```
