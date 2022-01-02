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
        "indexed": true,
        "internalType": "uint256",
        "name": "questId",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "player",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "heroId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "rewardItem",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "itemQuantity",
        "type": "uint256"
      }
    ],
    "name": "QuestReward",
    "type": "event"
  }
]"""
