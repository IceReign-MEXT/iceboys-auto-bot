# Minimal offline Bip39 + Solana derivation (for Termux)
from mnemonic import Mnemonic
from solders.keypair import Keypair
from bip_utils.utils import CryptoUtils
import hashlib

class Bip39SeedGenerator:
    def __init__(self, mnemonic: str):
        self.mnemonic = mnemonic
    def Generate(self, passphrase: str = ""):
        mnemo = Mnemonic("english")
        seed = mnemo.to_seed(self.mnemonic, passphrase)
        return seed

class Bip44Coins:
    SOLANA = "solana"

class Bip44:
    def __init__(self, seed, coin):
        self.seed = seed
        self.coin = coin
    @classmethod
    def FromSeed(cls, seed, coin):
        return cls(seed, coin)
    def Purpose(self):
        return self
    def Coin(self):
        return self
    def Account(self, idx):
        return self
    def Change(self, idx):
        return self
    def AddressIndex(self, idx):
        return self
    def PrivateKey(self):
        return CryptoUtils.Hash256(self.seed)
