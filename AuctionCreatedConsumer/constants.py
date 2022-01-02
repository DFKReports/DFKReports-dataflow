ONE_TESTNET = "https://api.s0.b.hmny.io"
ONE_MAINNET = "https://api.s0.t.hmny.io"

GRAPH_URL = "https://graph4.defikingdoms.com/subgraphs/name/defikingdoms/dex"
GRAPHQL_QUERY = """query {
    token(id: "%(hash)s"){
    name
    tokenDayData(orderBy: date, orderDirection: desc, where: {date_lte: %(date_lte)s, date_gte: %(date_gte)s}){
      priceUSD
      date
    }
  }
}"""

JEWEL_CONTRACT = "0x72Cb10C6bfA5624dD07Ef608027E366bd690048F"

ABI = """[
    {
        "anonymous": false,
        "inputs": [
          {
            "indexed": false,
            "internalType": "uint256",
            "name": "auctionId",
            "type": "uint256"
          },
          {
            "indexed": true,
            "internalType": "address",
            "name": "owner",
            "type": "address"
          },
          {
            "indexed": true,
            "internalType": "uint256",
            "name": "tokenId",
            "type": "uint256"
          },
          {
            "indexed": false,
            "internalType": "uint256",
            "name": "startingPrice",
            "type": "uint256"
          },
          {
            "indexed": false,
            "internalType": "uint256",
            "name": "endingPrice",
            "type": "uint256"
          },
          {
            "indexed": false,
            "internalType": "uint256",
            "name": "duration",
            "type": "uint256"
          },
          {
            "indexed": false,
            "internalType": "address",
            "name": "winner",
            "type": "address"
          }
        ],
        "name": "AuctionCreated",
        "type": "event"
    }
]"""
