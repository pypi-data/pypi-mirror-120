import requests
import optparse
import urllib
import json

HOST = "https://api.0x.org"

class ZeroEx:
    """
    0x API

    ...

    Attributes
    ----------
    

    Methods
    -------
    

    """

    def __init__(self, host="https://api.0x.org", verbose=False):
        self.host = host
        self.verbose = verbose
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def request(self, method, path, query):

        url = self.host + path 
        if query:
            url += '?' + urllib.parse.urlencode(query)

        if self.verbose:
            print()
            print(method, url)
            if query != "":
                print('query: '+str(query))

        headers = {
            'Content-Type': 'application/json'
        }

        self.session.headers = headers

        response = self.session.request(method, url)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + " " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    #############################################################################################

    # /swap/v1/price
    def get_price(self, sellAmountInWei, sellToken, buyToken, takerAddress=None, affiliateAddress=None, asJSON=False):
        qs = {
            'sellToken': sellToken,
            'buyToken': buyToken,
            'sellAmount': sellAmountInWei
        }
        if takerAddress:
            qs['takerAddress'] = takerAddress
        if affiliateAddress:
            qs['affiliateAddress'] = affiliateAddress
        # 'skipValidation': True, # enabled by default
        return self.request('GET', '/swap/v1/price', qs)

    # sellToken (Optional, defaults to "WETH") The ERC20 token address or symbol of the token 
    #   you want to get the price of tokens in. "ETH" can be provided as a valid sellToken.
    # /swap/v1/prices
    def get_prices(self, sellToken="WETH"):
        qs = {
            'sellToken': sellToken
        }
        return list(self.request('GET', '/swap/v1/prices', qs)['records'])

    # /swap/v1/tokens
    def get_tokens(self):
        return list(self.request('GET', '/swap/v1/tokens', None)['records'])

    # /swap/v1/quote
    def get_quote(self, amountInWei, sellToken, buyToken):
        qs = {
            'sellToken': sellToken,
            'buyToken': buyToken,
            'sellAmount': amountInWei,
        }
        return self.request('GET', '/swap/v1/quote', qs)

    #############################################################################################

    # def fill_quote(self, quote, contract, _from):
    #     # Fill the quote through 0x provided contract method
    #     receipt = contract.methods.fillQuote(
    #         quote.sellTokenAddress,
    #         quote.buyTokenAddress,
    #         quote.allowanceTarget,
    #         quote.to,
    #         quote.data
    #     ).send({
    #         'from': _from,
    #         'value': quote.value,
    #         'gasPrice': quote.gasPrice,
    #     })
    #     print("response: {}".format(receipt))
    #     return receipt

    #############################################################################################

def main():
    parser = optparse.OptionParser()

    parser.add_option('-h', '--host', dest="host", help="Host for request", default=HOST)
    parser.add_option('-m', '--method', dest="method", help="Method for request", default="GET")
    parser.add_option('-p', '--path', dest="path", help="Path for request", default="/")
    parser.add_option('-q', '--params', dest="params", help="Parameters for request")
    parser.add_option('-d', '--body', dest="body", help="Body for request")

    options, args = parser.parse_args()

    ZeroEx = ZeroEx()

    query = ''
    if options.params is not None:
        query = options.params

    try:
        response = ZeroEx.request(options.method, options.path, query, options.body)
    except Exception as ex:
        print("Unexpected error:", ex)
        exit(1)

    print(response)
    exit(0)

if __name__ == "__main__":
    main()
