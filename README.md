# Investopedia-Bot
![Investopedia-2017](https://user-images.githubusercontent.com/40627412/136075564-c1179715-164c-4e87-b81c-154adf20fb41.png)

Investopedia Bot is a tkitner python program that's suitable for beginners who want to enter the trading world via automation. First, why I chose Investopedia as stock simulator platform? It is an excellent simulator that is always recommend for beginners due to its simplicity. Second, where did the idea come from? The idea stemmed from my need to calculate the expectancy of stocks that I'm interested in to decide on the stock that I will buy. This process of calculating the expectancy of each stock is very exhausting, so I thought about automating the process through my programming skills. The program developed through time to become a "platform" for Investopedia automation.

## What Does Investopedia Bot do?
Investopedia Bot asks you to enter the stocks you're interested in to calculate their expectancies (a measure to show which stocks are less risky and gonna make you more money).
It also shows you stock data and recommends you the number of shares to be bought according to many factors that you decide on; all of that in order to facilitate reaching a decisoin. After you choose the stocks that you want to trade, you can execute the trade from the program automatically.

## Setup
1. Install repository `git clone git@github.com:bassel27/Investopedia-Bot.git`
2. CD into repository `cd Investopedia-Bot`
3. Install required libraries `pip install -r requirements.txt`
4. Install UBlock Origin on Google Chrome shorturl.at/qvCLM
5. Change Investopedia login info in the `config.py` file
6. Start the program `python main.py`

## How to Use Investopedia Trading?
### First Stage
Upon running the program, you get this window which asks you about the **risk percentage**: how much of your cash are you ready to lose on a single trade? Risk percentage is often 2% if you have much cash. On the other hand, people with less cash tend to increase it to 5%. If you uncheck 2%, you can enter your own risk percentage. Secondly, the program will ask you about the chance of winning which set by default to 0.9 to all stocks. If you uncheck it, you'll have to enter winning chance to each individual stock. Thirdly, below the two checkboxes you'll find the account value and cash. These values are scraped from your Investopedia profile.

![image](https://user-images.githubusercontent.com/40627412/136844357-76fa68f2-5ea8-4626-b633-ba1c21baef12.png)
### Seocnd Stage
Then, you'll have this window for each stock that you're interested in. The first entry is for the ticker (symbol) of the stock. The second is for the target price (what price you think the stock will reach). The third entry is for the stop loss price (the price at which you accept your loss and exit the trade.) If you've got more stocks that you're intersted in, then you can press "Onto the next stock" button. If this is the last stock, then you can press "finish" to display the results.

![image](https://user-images.githubusercontent.com/40627412/136844395-f4694ab3-1a72-474d-9629-348207852646.png)
### Third Stage
After you enter the stocks you're interested in, the results are displayed and the stocks are ranked descendingly according to expectancy. You get to choose the type of order (either market or limit order) and also specify the price of the limit order (the limit price is by default `current price ± 0.02`). The number of shares that are to be bought/ shorted is displayed. The number of shares is calculated through the following rule: `position size (number of shares) = Max loss per trade/ amount you can lose per share` or in other words: `position size (number of shares) = quantity = account value * (risk percentage / 100) / (|current price - stop loss price|)`.

![image](https://user-images.githubusercontent.com/40627412/136072260-660f6a72-d608-48ef-b480-ac4e3728974b.png)
