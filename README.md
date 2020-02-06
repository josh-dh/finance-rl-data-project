# finance-rl-data-project

reinforcement learning outline:
    agent: stock trader who recieves tweets in real time
    actions: buy, sell, or hold any stock mentioned in the tweet
    value function: the total amount of money the trader has at the end of the time period
    environment: a stream of tweets the stock trader recieves
    reward function: the immediate gain or loss to the liquid cash the trader has

NOTE: Currently can only find daily stock data, therefore trader will use daily open price for that stock when evaluating a tweet. Ideally I need to find a dataset which contains higher density data (up to the minute) so more precise trades can be made.