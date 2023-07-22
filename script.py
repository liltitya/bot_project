import requests
import time
import wget
import zipfile
import os
from TOKEN import token_st,token_vip,token_qiwi


def get_info_bestchange():
    url = 'http://api.bestchange.ru/info.zip'
    wget.download(url, 'C:/pythonProject3')
    unzip = zipfile.ZipFile('info.zip')
    unzip.extractall()
    unzip.close()
    banks = {}
    banks_id = []
    currency = {}
    currency_id = []
    possible_coins1 = ['USDT TRC20', 'BTC', 'BCH', 'ETH', 'ETC', 'LTC', 'XRP', 'XMR', 'DOGE', 'DASH', 'TRX', 'BNB', 'SOL',
                       'MATIC', 'ZEC', 'DAI', 'XEM', 'NEO', 'EOS',
                       'ADA', 'XLM', 'WAVES', 'OMG', 'ZRX',
                       'ICX', 'KMD', 'BAT', 'ONT', 'QTUM', 'LINK', 'ATOM',
                       'XTZ', 'DOT', 'UNI', 'RVN', 'VET',
                       'ALGO', 'MKR', 'AVAX', 'YFI', 'MANA', 'LUNA', 'NEAR']
    with open('bm_cy.dat') as currencies:
        for line in currencies.readlines():
            if line.split(';')[2] in ['Сбербанк RUB', 'Тинькофф RUB', 'Райффайзен RUB', 'QIWI RUB']:
                banks[line.split(';')[0]] = line.split(';')[2]
                banks_id.append(line.split(';')[0])
            if line.split(';')[3] in possible_coins1:
                if line.split(';')[3]=='USDT TRC20':
                    currency[line.split(';')[0]]='USDT'
                    currency_id.append(line.split(';')[0])
                else:
                    currency[line.split(';')[0]] = line.split(';')[3]
                    currency_id.append(line.split(';')[0])
    best_currency = {}
    with open('bm_rates.dat') as rates:
        for rline in rates.readlines():
            rline = rline.split(';')
            if rline[0] in banks_id and rline[1] in currency_id:
                if f"{currency[rline[1]]}" not in best_currency:
                    best_currency[f"{currency[rline[1]]}"] = [float(rline[3]), banks[rline[0]], rline[2]]
                elif float(rline[3]) < best_currency[f"{currency[rline[1]]}"][0]:
                    best_currency[f"{currency[rline[1]]}"] = [float(rline[3]), banks[rline[0]], rline[2]]
    exchange = {}
    with open('bm_exch.dat') as exchangers:
        for eline in exchangers.readlines():
            eline = eline.split(';')
            exchange[eline[0]] = eline[1]
    for coin, arr in best_currency.items():
        best_currency[coin] = [arr[0], arr[1], exchange[arr[2]]]

    os.remove('C:/pythonProject3/bm_bcodes.dat')
    os.remove('C:/pythonProject3/bm_brates.dat')
    os.remove('C:/pythonProject3/bm_cities.dat')
    os.remove('C:/pythonProject3/bm_cy.dat')
    os.remove('C:/pythonProject3/bm_cycodes.dat')
    os.remove('C:/pythonProject3/bm_exch.dat')
    os.remove('C:/pythonProject3/bm_info.dat')
    os.remove('C:/pythonProject3/bm_news.dat')
    os.remove('C:/pythonProject3/bm_rates.dat')
    os.remove('C:/pythonProject3/bm_top.dat')
    os.remove('C:/pythonProject3/info.zip')

    return best_currency


def get_info_binance_spot(coin1='BTC', coin2='USDT'):
    rev=0
    if coin1==coin2:
        return 1,-1
    url = f"https://www.binance.com/api/v3/depth?symbol={coin1}{coin2}&limit=1000"
    try:
        response = requests.get(url=url).json()
        answer1 = response['asks'][0][0]
        return float(answer1),rev
    except Exception as e:
        url2=f"https://www.binance.com/api/v3/depth?symbol={coin2}{coin1}&limit=1000"
        try:
            response2=requests.get(url=url2).json()
            answer2=1/float(response2['asks'][0][0])
            rev=1
            return float(answer2),rev
        except Exception as e:
            return 0,rev


def get_info_binance_p2p(coin,banks):
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    params = {
        "proMerchantAds": False,
        "page": 1,
        "rows": 10,
        "payTypes": banks,
        "countries": [],
        "publisherType": None,
        "transAmount": "",
        "asset": coin,
        "fiat": "RUB",
        "tradeType": "SELL"
    }

    try:
        response = requests.post(url=url, headers=headers, json=params).json()
        price = response['data'][0]['adv']['price']
        bank=response['data'][0]['adv']['tradeMethods'][0]['identifier']
        return [float(price),bank]
    except:
        return [0,'RosBankNew']


def find_best_way():
    mes = ''
    start_up_capital = 100000.00
    possible_coins1 = {'USDT': 'tether-trc20',
                       'BTC': 'bitcoin',
                       'BCH': 'bitcoin-cash',
                       'ETH': 'ethereum',
                       'ETC': 'ethereum-classic',
                       'LTC': 'litecoin',
                       'XRP': 'ripple',
                       'XMR': 'monero',
                       'DOGE': 'dogecoin',
                       'DASH': 'dash',
                       'TRX': 'tron',
                       'BNB': 'binance-coin',
                       'SOL': 'solana',
                       'MATIC': 'polygon',
                       'ZEC': 'zcash',
                       'DAI': 'dai',
                       'XEM': 'nem',
                       'NEO': 'neo',
                       'EOS': 'eos',
                       'ADA': 'cardano',
                       'XLM': 'stellar',
                       'WAVES': 'waves',
                       'OMG': 'omg',
                       'ZRX': 'zrx',
                       'ICX': 'icon',
                       'KMD': 'komodo',
                       'BAT': 'bat',
                       'ONT': 'ontology',
                       'QTUM': 'qtum',
                       'LINK': 'chainlink',
                       'ATOM': 'cosmos',
                       'XTZ': 'tezos',
                       'DOT': 'polkadot',
                       'UNI': 'uniswap',
                       'RVN': 'ravencoin',
                       'VET': 'vechain',
                       'ALGO': 'algorand',
                       'MKR': 'maker',
                       'AVAX': 'avalanche',
                       'YFI': 'yearn-finance',
                       'MANA': 'decentraland',
                       'LUNA': 'terra',
                       'NEAR': 'near',
                       }
    possible_coins2 = ['BTC', 'ETH', 'BNB', 'USDT']
    final_banks = ["TinkoffNew", "RaiffeisenBank", "RosBankNew"]
    first_banks = {
        'Райффайзен RUB': 'raiffeisen-bank',
        'Сбербанк RUB': 'sberbank',
        'Тинькофф RUB': 'tinkoff',
        'QIWI RUB': 'qiwi'
    }
    first_step = get_info_bestchange()
    final_sum = start_up_capital * 1.002
    for short_coin1, arr in first_step.items():
        for coin2 in possible_coins2:
            second_step,revers = get_info_binance_spot(short_coin1, coin2)
            third_step = get_info_binance_p2p(coin2, final_banks)
            print(start_up_capital / arr[0] * second_step * third_step[0] * 0.999, f"{arr[1]}->{short_coin1}->{coin2}->{third_step[1]}",arr[0],second_step,third_step[0])
            if start_up_capital / arr[0] * second_step * third_step[0] * 0.999 > final_sum:
                final_sum = start_up_capital / arr[0] * second_step * third_step[0] * 0.999
                profit=100 * (final_sum - start_up_capital) / start_up_capital
                start_bank=arr[1]
                if revers==0:
                    mes = f"{arr[1]}->{short_coin1}->{coin2}->{third_step[1]}\n" \
                          f"profit {(100 * (final_sum - start_up_capital) / start_up_capital):.2f}%\n\n" \
                          f"Обменник: {arr[2]}\n\n" \
                          f"▶ Обмениваем на https://www.bestchange.ru/{first_banks[arr[1]]}-to-{possible_coins1[short_coin1]}.html: 100 000 рублей {arr[1]}\n" \
                          f"по курсу {arr[0]}\n" \
                          f"Получаем на binance: {start_up_capital / arr[0]} {short_coin1}\n\n" \
                          f"▶ Продаем {short_coin1} на https://www.binance.com/ru/trade/{short_coin1}_{coin2}?type=spot?\n" \
                          f"по курсу {second_step}\n" \
                          f"Получаем {start_up_capital / arr[0] * second_step} {coin2}\n\n" \
                          f"▶ Продаем {coin2} на https://p2p.binance.com/ru/trade/{third_step[1]}/{coin2}?fiat=RUB?\n" \
                          f"по курсу {third_step[0]}\n" \
                          f"Получаем на {third_step[1]} {final_sum:.2f}"
                elif revers==-1:
                    mes=f"{arr[1]}->{coin2}->{third_step[1]}\n" \
                          f"profit {(100 * (final_sum - start_up_capital) / start_up_capital):.2f}%\n\n" \
                          f"Обменник: {arr[2]}\n\n" \
                          f"▶ Обмениваем на https://www.bestchange.ru/{first_banks[arr[1]]}-to-{possible_coins1[short_coin1]}.html: 100 000 рублей {arr[1]}\n" \
                          f"по курсу {arr[0]}\n" \
                          f"Получаем на binance: {start_up_capital / arr[0]} {short_coin1}\n\n" \
                          f"▶ Продаем {coin2} на https://p2p.binance.com/ru/trade/{third_step[1]}/{coin2}?fiat=RUB?\n" \
                          f"по курсу {third_step[0]}\n" \
                          f"Получаем на {third_step[1]} {final_sum:.2f}"
                else:
                    mes=f"{arr[1]}->{short_coin1}->{coin2}->{third_step[1]}\n" \
                          f"profit {(100 * (final_sum - start_up_capital) / start_up_capital):.2f}%\n\n" \
                          f"Обменник: {arr[2]}\n\n" \
                          f"▶ Обмениваем на https://www.bestchange.ru/{first_banks[arr[1]]}-to-{possible_coins1[short_coin1]}.html: 100 000 рублей {arr[1]}\n" \
                          f"по курсу {arr[0]}\n" \
                          f"Получаем на binance: {start_up_capital / arr[0]} {short_coin1}\n\n" \
                          f"▶ Продаем {short_coin1} на https://www.binance.com/ru/trade/{coin2}_{short_coin1}?type=spot?\n" \
                          f"по курсу {second_step}\n" \
                          f"Получаем {start_up_capital / arr[0] * second_step} {coin2}\n\n" \
                          f"▶ Продаем {coin2} на https://p2p.binance.com/ru/trade/{third_step[1]}/{coin2}?fiat=RUB?\n" \
                          f"по курсу {third_step[0]}\n" \
                          f"Получаем на {third_step[1]} {final_sum:.2f}"
    try:
        return (mes,start_bank,profit)
    except:
        return ('','',0)


if __name__ == '__main__':
    while True:
        try:
            answer = find_best_way()
            ans=answer[0]
            bank=answer[1]
            profit=answer[2]
            if ans:
                if bank=='QIWI RUB':
                    with open('users_qiwi.txt') as users:
                        just_users = users.readlines()
                    for user in just_users:
                        params = {
                            'chat_id': int(user),
                            'text': ans
                        }
                        requests.get(f'https://api.telegram.org/bot{token_qiwi}/sendMessage', params=params)
                elif profit>1:
                    with open('users_vip.txt') as users:
                        just_users = users.readlines()
                    for user in just_users:
                        params = {
                            'chat_id': int(user),
                            'text': ans
                        }
                        requests.get(f'https://api.telegram.org/bot{token_vip}/sendMessage', params=params)
                    """with open('users_st.txt') as users:
                        just_users = users.readlines()
                    for user in just_users:
                        params = {
                            'chat_id': int(user),
                            'text': ans
                        }
                        requests.get(f'https://api.telegram.org/bot{token_st}/sendMessage', params=params)"""
                else:
                    with open('users_st.txt') as users:
                        just_users = users.readlines()
                    for user in just_users:
                        params = {
                            'chat_id': int(user),
                            'text': ans
                        }
                        requests.get(f'https://api.telegram.org/bot{token_st}/sendMessage', params=params)
        except:
            print('Something wrong')
            time.sleep(30)
        print('______________')
