import csv
from web3.auto import w3

w3.HTTPProvider('http:satoshi.doc.ic.ac.uk:8545')

def write_block_times(fromBlock=9000000, toBlock=w3.eth.blockNumber, file='eth_block_times.csv'):
    assert fromBlock <= toBlock, 'Invalid block range specified.' 
    with open(file, 'w', newline='') as csvfile:
        fieldnames = ['block_height', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        counter = 0
        while fromBlock <= toBlock:
            timestamp = w3.eth.getBlock(fromBlock)['timestamp']
            #if counter % 10000 == 0:
                #print(round(counter/(toBlock-fromBlock)*100, 2), '% of blocks parsed')
            writer.writerow({
                    'block_height': fromBlock, 
                    'timestamp': timestamp
            })
            fromBlock += 1
            counter += 1

write_block_times()
        
