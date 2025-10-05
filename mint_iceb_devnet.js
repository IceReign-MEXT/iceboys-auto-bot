// mint_iceb_devnet.js
// Usage: NODE_OPTIONS=--max-old-space-size=512 node mint_iceb_devnet.js
const fs = require('fs');
const { Connection, Keypair, LAMPORTS_PER_SOL, clusterApiUrl } = require('@solana/web3.js');
const { createMint, getOrCreateAssociatedTokenAccount, mintTo } = require('@solana/spl-token');

(async () => {
  try {
    const walletPath = process.env.HOME + '/icehub_system/wallets/sol_account.json';
    const j = JSON.parse(fs.readFileSync(walletPath,'utf8'));
    const secretHex = j.secret_key_bytes_hex;
    const secret = Buffer.from(secretHex, 'hex');
    const payer = Keypair.fromSecretKey(secret);

    const connection = new Connection(clusterApiUrl('devnet'), 'confirmed');
    console.log('Using wallet:', payer.publicKey.toBase58());

    // ensure some devnet SOL for fees
    const bal = await connection.getBalance(payer.publicKey);
    console.log('SOL balance:', bal / LAMPORTS_PER_SOL);
    if (bal < LAMPORTS_PER_SOL) {
      console.log('Requesting airdrop 2 SOL (devnet)...');
      const sig = await connection.requestAirdrop(payer.publicKey, 2 * LAMPORTS_PER_SOL);
      await connection.confirmTransaction(sig, 'confirmed');
      console.log('Airdrop completed.');
    }

    // create mint
    const decimals = 9;
    console.log('Creating mint (decimals=' + decimals + ')...');
    const mint = await createMint(connection, payer, payer.publicKey, null, decimals);
    console.log('Mint created:', mint.toBase58());

    // create owner associated token account
    const ata = await getOrCreateAssociatedTokenAccount(connection, payer, mint, payer.publicKey);
    console.log('Owner ATA:', ata.address.toBase58());

    // mint total supply (3,000,000,000 * 10^decimals)
    const totalSupply = BigInt(3000000000) * (BigInt(10) ** BigInt(decimals));
    console.log('Minting total supply:', totalSupply.toString());
    await mintTo(connection, payer, mint, ata.address, payer.publicKey, totalSupply);
    console.log('Minting complete.');

    console.log('FINAL: Mint address:', mint.toBase58());
    console.log('Token account:', ata.address.toBase58());
  } catch (err) {
    console.error('ERROR', err);
  }
})();
