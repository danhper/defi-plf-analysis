const fs = require('fs/promises')
const Web3 = require('web3')
const signale = require('signale')

const web3 = new Web3(new Web3.providers.HttpProvider('http://satoshi.doc.ic.ac.uk:8545'))

const batchSize = 10000

async function getContractEvents (contract, startBlock, output, options) {
  const fd = await fs.open(output, 'w', '0644')
  const latestBlock = options.latestBlock || await web3.eth.getBlockNumber()
  signale.info(`latest block: ${latestBlock}`)
  const totalCount = latestBlock - startBlock + 1
  signale.info(`fetching ${totalCount} blocks`)

  let count = 0

  for (let i = latestBlock; i >= startBlock - batchSize; i -= batchSize, count += batchSize) {
    const percentage = ((count / totalCount) * 100).toFixed(2)
    signale.info(`progress ${count}/${totalCount} (${percentage}%)`)

    const params = { fromBlock: i - batchSize, toBlock: i - 1 }
    const events = await contract.getPastEvents(params)
    for (const event of events) {
      await fd.write(JSON.stringify(event) + '\n', 'utf8')
    }
  }
  await fd.close()

  signale.success(`saved ${count} events`)
}

(async function () {
  const { program } = require('commander')

  program
    .requiredOption('-a, --address <string>', 'contract address')
    .requiredOption('-s, --start-block <number>', 'first block number')
    .requiredOption('--abi <string>', 'path to the JSON ABI file')
    .requiredOption('-o, --output <string>', 'output file')
    .option('-e, --end-block <number>', 'last block number (defaults to latest block)')

  program.parse(process.argv)
  const abi = require(program.abi)
  const contract = new web3.eth.Contract(abi, program.address)
  const options = { endBlock: program.endBlock }

  await getContractEvents(contract, program.startBlock, program.output, options)
})()
