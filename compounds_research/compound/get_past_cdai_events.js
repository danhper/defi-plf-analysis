var Web3 = require('web3');
var web3 = new Web3(new Web3.providers.HttpProvider('http://satoshi.doc.ic.ac.uk:8545'));

web3.eth.getBlockNumber().then(console.log);

const abi = require('./abi.json');

const address = '0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643';

const cDaiContract = new web3.eth.Contract(abi, address);

// cDaiContract.getPastEvents(
//     'NewMarketInterestRateModel',
//     {
//       fromBlock: 8500000,
//       toBlock: 9000000
//     },
//     (err, events) => { console.log(events) }
//   );

  //JUMP RATE MODEL -- "jump_rate"
  // [
  //   {
  //     address: '0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643',
  //     blockNumber: 8983575,
  //     transactionHash: '0x090ce7d33359e5d288ce169f41bb3d2cb55ac17b026a10cf80b3fc4f0c85c827',
  //     transactionIndex: 66,
  //     blockHash: '0xa1cd69490a27b1c72c730ffbde9d37ae0b27f9918ea986273b7fd192931c3d02',
  //     logIndex: 68,
  //     removed: false,
  //     id: 'log_d0aa3f0a',
  //     returnValues: Result {
  //       '0': '0x0000000000000000000000000000000000000000',
  //       '1': '0x5562024784cc914069d67D89a28e3201bF7b57E7',
  //       oldInterestRateModel: '0x0000000000000000000000000000000000000000',
  //       newInterestRateModel: '0x5562024784cc914069d67D89a28e3201bF7b57E7'
  //     },
  //     event: 'NewMarketInterestRateModel',
  //     signature: '0xedffc32e068c7c95dfd4bdfd5c4d939a084d6b11c4199eac8436ed234d72f926',
  //     raw: {
  //       data: '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000005562024784cc914069d67d89a28e3201bf7b57e7',
  //       topics: [Array]
  //     }
  //   }
  // ]


  //DAIInterestRateModel "dai_rate"
  // [
  //   {
  //     address: '0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643',
  //     blockNumber: 9133122,
  //     transactionHash: '0x20d692e5986096498627dae978dde8b40b2354aec47a4e901d68010b22f2b261',
  //     transactionIndex: 181,
  //     blockHash: '0x29a5a5f7efe296f76c1bb1e24ef076257a53a0812e7e397bff25671e3f8ab5b3',
  //     logIndex: 181,
  //     removed: false,
  //     id: 'log_02270a41',
  //     returnValues: Result {
  //       '0': '0x5562024784cc914069d67D89a28e3201bF7b57E7',
  //       '1': '0xec163986cC9a6593D6AdDcBFf5509430D348030F',
  //       oldInterestRateModel: '0x5562024784cc914069d67D89a28e3201bF7b57E7',
  //       newInterestRateModel: '0xec163986cC9a6593D6AdDcBFf5509430D348030F'
  //     },
  //     event: 'NewMarketInterestRateModel',
  //     signature: '0xedffc32e068c7c95dfd4bdfd5c4d939a084d6b11c4199eac8436ed234d72f926',
  //     raw: {
  //       data: '0x0000000000000000000000005562024784cc914069d67d89a28e3201bf7b57e7000000000000000000000000ec163986cc9a6593d6addcbff5509430d348030f',
  //       topics: [Array]
  //     }
  //   }
  // ]

  //DAIInterestRateModelV2 - "dai_rate"
  // [
  //   {
  //     address: '0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643',
  //     blockNumber: 9987151,
  //     transactionHash: '0x4caa5276108eb7800091c100223b31f2f71de2ba218460e2acf99c45743c4675',
  //     transactionIndex: 90,
  //     blockHash: '0xd2edfa0d1c1a505c705ae5493c4fa6e348251336ff132d0b535db0ec5789e13f',
  //     logIndex: 134,
  //     removed: false,
  //     id: 'log_e15f7d01',
  //     returnValues: Result {
  //       '0': '0xec163986cC9a6593D6AdDcBFf5509430D348030F',
  //       '1': '0x000000007675b5E1dA008f037A0800B309e0C493',
  //       oldInterestRateModel: '0xec163986cC9a6593D6AdDcBFf5509430D348030F',
  //       newInterestRateModel: '0x000000007675b5E1dA008f037A0800B309e0C493'
  //     },
  //     event: 'NewMarketInterestRateModel',
  //     signature: '0xedffc32e068c7c95dfd4bdfd5c4d939a084d6b11c4199eac8436ed234d72f926',
  //     raw: {
  //       data: '0x000000000000000000000000ec163986cc9a6593d6addcbff5509430d348030f000000000000000000000000000000007675b5e1da008f037a0800b309e0c493',
  //       topics: [Array]
  //     }
  //   }
  // ]
  
  //Reserve factor mantissa changes
  async function getReserveFactors() {

    // var startingBlock;
    // await web3.eth.getBlockNumber()
    //     .then((number)=>{
    //         startingBlock = number;            
    //     });


    await  cDaiContract.getPastEvents('NewReserveFactor',{
            fromBlock: 10000000,
            toBlock: 'latest'
            },
        (error, events) => { console.log(events) })

}

getReserveFactors()

//Reserve Factor MAntissa only changed once on 
// 158 days 15 hrs ago (Dec-20-2019 12:38:39 AM +UTC)
// [
//   {
//     address: '0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643',
//     blockNumber: 9133173,
//     transactionHash: '0xc8c5f7c143ec0834227b03b567a4a42f35f14cd7f73f4d054d10a52993339bce',
//     transactionIndex: 110,
//     blockHash: '0xa67df3b9122b5dec07bfd7cd1d4a3ade5d7d05e223b33e3b568c52d22b0bf9ff',
//     logIndex: 110,
//     removed: false,
//     id: 'log_40168da0',
//     returnValues: Result {
//       '0': '100000000000000000',
//       '1': '50000000000000000',
//       oldReserveFactorMantissa: '100000000000000000',
//       newReserveFactorMantissa: '50000000000000000'
//     },
//     event: 'NewReserveFactor',
//     signature: '0xaaa68312e2ea9d50e16af5068410ab56e1a1fd06037b1a35664812c30f821460',
//     raw: {
//       data: '0x000000000000000000000000000000000000000000000000016345785d8a000000000000000000000000000000000000000000000000000000b1a2bc2ec50000',
//       topics: [Array]
//     }
//   }
// ]
