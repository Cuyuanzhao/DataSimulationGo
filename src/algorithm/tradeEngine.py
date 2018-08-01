def trade(prices, buyThresh=0.001, sellThresh=0.001, interval=1):
    # hold a share at open
    preMin = prices[0]
    preMax = prices[0]
    buyIdx = [0]
    buyPrices = [prices[0]]
    sellIdx = []
    sellPrices = []
    gains = []
    isHeld = True
    totalCount = 0

    for i in range(0, len(prices), interval):
        price = prices[i]
        if isHeld: # need to sell
            if price >= preMax: # continue hold it
                preMax = price
            elif (preMax - price) / preMax >= sellThresh:  # or (buyPrices[-1] - price) / buyPrices[-1] >= sellThreshLastBuy: # sell it
                sellIdx.append(i)
                sellPrices.append(price)
                gains.append(price - buyPrices[-1])
                isHeld = False
                preMin = price
                totalCount += 1
        else:  # need to buy
            if price <= preMin:
                preMin = price
            elif (price - preMin) / preMin >= buyThresh or price >= buyPrices[-1]:
                buyIdx.append(i)
                buyPrices.append(price)
                isHeld = True
                preMax = price

    # sell the share at close
    if len(sellPrices) < len(buyPrices):
        sellIdx.append(len(prices) - 1)
        sellPrices.append(prices[-1])
        gains.append(sellPrices[-1] - buyPrices[-1])
        totalCount += 1

    totalGain = sum(gains[0 : len(gains)])
    actualYield = totalGain / prices[0]
    defaultYield = (prices[-1] - prices[0]) / prices[0]

    return {
        "defaultYield": defaultYield,
        "actualYield": actualYield,
        "extraYield": actualYield - defaultYield,
        "count": totalCount,
        "gain": totalGain,
        "buyData": {
            "buyIdx": buyIdx,
            "buyPrices": buyPrices
        },
        "sellData": {
            "sellIdx": sellIdx,
            "sellPrices": sellPrices
        }
    }
