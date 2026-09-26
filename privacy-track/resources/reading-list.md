# Reading List

> One short list per session of [The Privacy Sessions](../SESSIONS.md). **(R)** = read before the session if you can; everything else is for going deeper. Primary sources first, then explainers. Links verified September 2026.

## Always useful

- [Bitcoin Wiki: Privacy](https://en.bitcoin.it/wiki/Privacy): the long-form reference on how Bitcoin privacy breaks
- [Bitcoin Optech topics](https://bitcoinops.org/en/topics/): one page per protocol, with a history of every related change
- [Bitcoin Core PR Review Club](https://bitcoincore.reviews): the model for our Review Circle and S3

## S1-S3 · Silent Payments

- **(R)** [BIP352: Silent Payments](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki), at least "Overview" and "Creating outputs"
- [BIP352 reference.py and test vectors](https://github.com/bitcoin/bips/tree/master/bip-0352): our [lab](../labs/silent-payments/) uses the same vectors
- [Optech: Silent Payments](https://bitcoinops.org/en/topics/silent-payments/)
- [BIP352 Index Server Specification](https://github.com/silent-payments/BIP0352-index-server-specification): tweak servers vs remote scanners (S2)
- [BIP375](https://github.com/bitcoin/bips/blob/master/bip-0375.mediawiki) + [BIP374](https://github.com/bitcoin/bips/blob/master/bip-0374.mediawiki): sending SP with PSBTs and DLEQ proofs (hardware wallets)
- Bitcoin Core: [tracking issue #28536](https://github.com/bitcoin/bitcoin/issues/28536), [#35301](https://github.com/bitcoin/bitcoin/pull/35301) (merged), [#35302](https://github.com/bitcoin/bitcoin/pull/35302), [#32966](https://github.com/bitcoin/bitcoin/pull/32966) (S3)

## S4 · Chain analysis and fingerprinting

- **(R)** [Bitcoin Wiki: Blockchain attacks on privacy](https://en.bitcoin.it/wiki/Privacy#Blockchain_attacks_on_privacy)
- [Ishaana Misra: Wallet Fingerprinting](https://ishaana.com/blog/wallet_fingerprinting/): real wallets, real tells
- Hughes, [A Cypherpunk's Manifesto](https://www.activism.net/cypherpunk/manifesto.html) (1993)

## S5 · Coin selection and change

- **(R)** [Optech: Coin selection](https://bitcoinops.org/en/topics/coin-selection/)
- Erhardt, [An Evaluation of Coin Selection Strategies](https://murch.one/erhardt2016coinselection.pdf) (2016)
- [BIP329: Wallet label export](https://github.com/bitcoin/bips/blob/master/bip-0329.mediawiki) · [Optech: Wallet labels](https://bitcoinops.org/en/topics/wallet-labels/)

## S6 · Payjoin

- **(R)** [payjoin.org](https://payjoin.org): the why, plus who supports it
- [BIP77: Async Payjoin](https://github.com/bitcoin/bips/blob/master/bip-0077.md) · [BIP78: Payjoin](https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki)
- [Optech: Payjoin](https://bitcoinops.org/en/topics/payjoin/)

## S7 · Light clients and your own node

- **(R)** [Optech: Compact block filters](https://bitcoinops.org/en/topics/compact-block-filters/)
- [BIP157](https://github.com/bitcoin/bips/blob/master/bip-0157.mediawiki) · [BIP158](https://github.com/bitcoin/bips/blob/master/bip-0158.mediawiki)
- [Optech: Utreexo](https://bitcoinops.org/en/topics/utreexo/) · [Floresta](https://github.com/getfloresta/Floresta) · [Kyoto](https://github.com/2140-dev/kyoto)
- Satoshi, [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf), §8 (SPV) and §10 (Privacy)

## S8 · Network privacy

- **(R)** [Bitcoin Core 31.0 release notes](https://bitcoincore.org/en/releases/31.0/): `-privatebroadcast` and embedded asmap
- [BIP324: v2 P2P transport](https://github.com/bitcoin/bips/blob/master/bip-0324.mediawiki) · [Optech: v2 transport](https://bitcoinops.org/en/topics/v2-p2p-transport/)
- [Optech: Eclipse attacks](https://bitcoinops.org/en/topics/eclipse-attacks/)
- Biryukov, Khovratovich, Pustogarov, [Deanonymisation of clients in Bitcoin P2P network](https://arxiv.org/abs/1405.7418) (2014)
- May, [The Crypto Anarchist Manifesto](https://www.activism.net/cypherpunk/crypto-anarchy.html) (1988)

## S9 · CoinJoin and swaps

- **(R)** Maxwell, [CoinJoin: Bitcoin privacy for the real world](https://bitcointalk.org/index.php?topic=279249.0) (2013)
- [Optech: CoinJoin](https://bitcoinops.org/en/topics/coinjoin/) · [Optech: CoinSwap](https://bitcoinops.org/en/topics/coinswap/)
- Belcher, [Design for a CoinSwap implementation](https://gist.github.com/chris-belcher/9144bd57a91c194e332fb5ca371d0964)
- [JoinMarket](https://github.com/JoinMarket-Org/joinmarket-clientserver) · [openswap](https://github.com/citadel-foss/openswap)

## S10 · Lightning privacy

- **(R)** [Optech: Offers (BOLT12)](https://bitcoinops.org/en/topics/offers/)
- [BOLT12 spec](https://github.com/lightning/bolts/blob/master/12-offer-encoding.md)
- [Polar](https://lightningpolar.com): one-click regtest Lightning networks for the hands-on

## S11 · Ecash

- **(R)** [Optech: Ecash](https://bitcoinops.org/en/topics/ecash/)
- [cashu.space](https://cashu.space) · [fedimint.org](https://fedimint.org)
- Chaum, *Security without Identification: Transaction Systems to Make Big Brother Obsolete* (Communications of the ACM, 1985)

---

Found a better source, or a dead link? PRs welcome. See [CONTRIBUTING.md](../CONTRIBUTING.md).
