# Investopedia-Bot
![Investopedia-2017](https://user-images.githubusercontent.com/40627412/136075564-c1179715-164c-4e87-b81c-154adf20fb41.png)

Investopedia Bot is a tkitner python program that's suitable for beginners who want to enter the trading world via automation. First, why I chose Investopedia as stock simulator platform? It is an excellent simulator that is always recommend for beginners due to its simplicity. Second, where did the idea come from? The idea stemmed from my need to calculate the expectancy of stocks that I'm interested in to decide on the stock that I will buy. This process of calculating the expectancy of each stock is very exhausting, so I thought about automating the process through my programming skills. The program developed through time to become a "platform" for Investopedia automation.
## What Does Investopedia Bot do?
Investopedia Bot asks you to enter the stocks you're interested in to calculate their expectancies (a measure to show which stocks are less risky and gonna make you more money).
It also shows you stock data and recommends you the number of shares to be bought according to many factors that you decide on; all of that in order to facilitate reaching a decisoin. After you choose the stocks that you want to trade, you can execute the trade from the program automatically as well as make a new record in your Notion database (trading journal) with the info of your trade. 
## Setup
First, in lines 52 and 53 in the scraping.py file, you got to replace `creds.username` and `creds.password` with your Investopedia's email and password.

Second, you got to add uBlock Origin (chrome extension) files to the program directory. To do that:
1. Add uBlock Origin as an extension on chrome shorturl.at/qvCLM
2. Now assuming you are on windows, go to `C:\Users\YOUR_USER_NAME\AppData\Local\Google\Chrome\User Data\Default\Extensions\cjpalhdlnbpafiamejdnhcphjbkeiagm`
3. There should be a folder with a number (the version number). Copy that folder and paste it in the program directory.

Third, you got to add the paths of some folders and files:
1. In line 12 in Scraping.py you gotta add the path of ublock origin extension. It'll be something like this for example `C:\Users\Bassel Attia\Documents\Trading Core\1.37.2_0`
2. In line 30 in `tkinterFuncitons.py`, you got to add the path of the icon of the program that is called `money_icon.ico`. The path should be somehting like this `C:\Users\Bassel Attia\Documents\Trading Core\money_icon.ico`.
Fourth, you got to make the program access your notion databse. If you don't want to use notion, you can simply delete the `addNotionRow` method and delete the lines, in which it's called; they're all present in the `Stock.py` file. However, if you want to use notion then follow along. In line 258 you should add your notion database's token; follow this video https://www.youtube.com/watch?v=6sJFI8LbhpY&t=436s from 4:30 to do that. You also got to paste your database url in line 260.
## How to Use Investopedia Trading?
Upon running the program, you get this window which asks you about the **risk percentage**: how much of your cash are you ready to lose on a single trade? Risk percentage is often 2% if you have much cash. On the other hand, people with less cash tend to increase it to 5%. If you uncheck 2%, you can enter your own risk percentage. Secondly, the program will ask you about the chance of winning which set by default to 0.9 to all stocks. If you uncheck it, you'll have to enter winning chance to each individual stock. Thirdly, below the two checkboxes you'll find the account value and cash. These values are scraped from your Investopedia profile.

![image](https://user-images.githubusercontent.com/40627412/135750345-24be1cf0-889d-4085-a896-03318fb0a248.png)

Then, you'll have this window for each stock that you're interested in. The first entry is for the ticker (symbol) of the stock. The second is for the target price (what price you think the stock will reach). The third entry is for the stop loss price (the price at which you accept your loss and exit the trade.) If you've got more stocks that you're intersted in, then you can press "Onto the next stock" button. If this is the last stock, then you can press "finish" to display the results.

![image](https://user-images.githubusercontent.com/40627412/135750914-2b92c67f-d3f7-4b67-91a0-84b03a4dcb7b.png)

After you enter the stocks you're interested in, the results are displayed and the stocks are ranked descendingly according to expectancy. You get to choose the type of order (either market or limit order) and also specify the price of the limit order (the limit price is by default `current price ± 0.02`). The number of shares that are to be bought/ shorted is displayed. The number of shares is calculated through the following rule: `position size (number of shares) = Max loss per trade/ amount you can lose per share` or in other words: `position size (number of shares) = quantity = account value * (risk percentage / 100) / (|current price - stop loss price|)`. Upon clicking on "Execute order", the order is automatically placed on Investopedia and a new record on your notion database is formed with the details of the trade.

![image](https://user-images.githubusercontent.com/40627412/136072260-660f6a72-d608-48ef-b480-ac4e3728974b.png)
