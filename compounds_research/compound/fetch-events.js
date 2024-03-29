const fs = require('fs').promises
const path = require('path')
const Web3 = require('web3')
const signale = require('signale')
const { await } = require('signale')

const web3 = new Web3(new Web3.providers.HttpProvider('http://satoshi.doc.ic.ac.uk:8545'))

const batchSize = 10000

async function fetchEventsSplitBatch (contract, params, splitSize, options = {}) {
  const miniBatchSize = batchSize / splitSize
  const events = []
  for (let i = 0; i < splitSize; i++) {
    const start = params.fromBlock + miniBatchSize * i
    const splittedParams = { fromBlock: start, toBlock: start + miniBatchSize - 1 }
    try {
      const batchEvents = await contract.getPastEvents(splittedParams)
      events.push(...batchEvents)
    } catch (e) {
      if (options.ignoreErrors) {
        signale.warn('failed to fetch', splittedParams, ': ', e)
      } else {
        throw e
      }
    }
  }
  return events
}

async function fetchEvents (contract, params, retries = 3) {
  try {
    return await contract.getPastEvents(params)
  } catch (e) {}
  // split in smaller chunks if this fails
  for (const size of [10, 100, 1000, 10000]) {
    signale.warn('failed to fetch ', params, 'trying in batches of', batchSize / size)
    try {
      return await fetchEventsSplitBatch(contract, params, size)
    } catch (e) {}
  }
  return await fetchEventsSplitBatch(contract, params, 10000, { ignoreErrors: true })
}

async function getContractEvents (contract, startBlock, output, options = {}) {
  const fd = await fs.open(output, 'w', '0644')
  const name = contract.name || contract.options.address
  const endBlock = options.endBlock || await web3.eth.getBlockNumber()
  const totalCount = endBlock - startBlock + 1
  signale.info(`fetching ${name}, ${totalCount} blocks from ${startBlock} to ${endBlock}`)

  let eventsCount = 0
  for (let i = endBlock, count = 0; i >= startBlock - batchSize; i -= batchSize, count += batchSize) {
    const percentage = ((count / totalCount) * 100).toFixed(2)
    signale.info(`progress ${name}: ${count}/${totalCount} (${percentage}%)`)

    const params = { fromBlock: i - batchSize, toBlock: i - 1 }
    const events = await fetchEvents(contract, params)
    eventsCount += events.length
    for (const event of events) {
      await fd.write(JSON.stringify(event) + '\n', 'utf8')
    }
  }
  await fd.close()

  signale.success(`saved ${eventsCount} events for ${name}`)
}

async function fetchBulk (abi, contracts, outputDir) {
  const abiState = await fs.lstat(abi)
  await Promise.all(contracts.map(async contractConfig => {
    let abiPath = abi
    if (abiState.isDirectory()) {
      abiPath = path.join(abiPath, contractConfig.name + '.json')
    }
    const rawABI = await fs.readFile(abiPath, 'utf-8')
    const parsedABI = JSON.parse(rawABI)
    const output = path.join(outputDir, contractConfig.name + '.jsonl')
    const contract = new web3.eth.Contract(parsedABI, contractConfig.address)
    contract.name = contractConfig.name
    return getContractEvents(contract, contractConfig.deployed, output)
  }))
}

(async function () {
  const { program } = require('commander')

  program
    .command('fetch-single')
    .requiredOption('-a, --address <string>', 'contract address')
    .requiredOption('-s, --start-block <number>', 'first block number')
    .requiredOption('--abi <string>', 'path to the JSON ABI file')
    .requiredOption('-o, --output <string>', 'output file')
    .option('-e, --end-block <number>', 'last block number (defaults to latest block)')
    .action(async (prog) => {
      const abi = require(prog.abi)
      const contract = new web3.eth.Contract(abi, prog.address)
      const options = { endBlock: prog.endBlock }
      await getContractEvents(contract, prog.startBlock, prog.output, options)
    })

  program
    .command('fetch-bulk')
    .requiredOption('--abi <string>', 'path to the JSON ABI file, or directory with ABIS')
    .requiredOption('-c, --config <string>', 'addresses with config')
    .requiredOption('-o, --output <string>', 'output directory')
    .action(async (prog) => {
      const config = require(prog.config)
      await fetchBulk(prog.abi, config, prog.output)
    })

  await program.parseAsync(process.argv)
})()
