from algosdk import transaction, account, util
from algosdk.v2client import algod
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get private key and address from environment variables
private_key = os.getenv("PRIVATE_KEY")
address = account.address_from_private_key(private_key)
print("Address:", address)

# Get Algorand client parameters from environment variables
algod_token = os.getenv("TESTNET_ALGOD_TOKEN")
algod_url = os.getenv("TESTNET_ALGOD_URL")
algod_port = os.getenv("TESTNET_ALGOD_PORT")

# Initialize Algorand client
algod_client = algod.AlgodClient(algod_token, algod_url)

# Define NFT parameters
asset_name = "MyMusicNFT"   # Name of the NFT
unit_name = "MUS"           # Short name (unit name)
metadata_url = "ipfs://<your-ipfs-hash>"  # IPFS URL for metadata
total_supply = 1            # NFT, so only one token
decimals = 0                # NFT is indivisible

# Get suggested transaction parameters
suggested_params = algod_client.suggested_params()

# Create the transaction to configure the asset as an NFT
payment_txn = transaction.AssetConfigTxn(
    sender=address,
    sp=suggested_params,
    total=total_supply,
    default_frozen=False,
    unit_name=unit_name,
    asset_name=asset_name,
    manager=address,      # Creator has management permissions
    reserve=None,
    freeze=None,
    clawback=None,
    url=metadata_url,
    decimals=decimals,
    strict_empty_address_check=False  # Allow empty addresses
)

payment_txn = transaction.AssetOptInTxn(
    sender=address,
    sp=suggested_params,
    index = 728528710
)

# Sign the transaction
signed_txn = payment_txn.sign(private_key)

# Send the transaction
txid = algod_client.send_transaction(signed_txn)
print(f"Txn sent: https://testnet.explorer.perawallet.app/tx/{txid}")

# Wait for transaction confirmation
result = transaction.wait_for_confirmation(algod_client, txid, 4)
print(f"Txn Confirmed in round {result['confirmed-round']}")
