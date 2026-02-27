# 手数料・コストの一次情報ソース

このプロジェクトでは、手数料をハードコードせず、`config/default.yaml` と `arb_bot/fee_probe.py` で更新できる設計にしています。

## 公式ページ（確認用）
- Bybit Trading Fee Structure（公式ヘルプ）  
  https://www.bybit.com/en/help-center/article/Trading-Fee-Structure/
- OKX Fee Details（公式ヘルプ）  
  https://www.okx.com/help/fee-details
- Etherscan Gas Tracker（Ethereum実勢ガス）  
  https://etherscan.io/gastracker
- mempool.space（Bitcoin mempool/fee可視化）  
  https://mempool.space/

## 実運用向け更新手順
1. `python -m arb_bot.fee_probe` を実行し、`reports/fee_probe.json` を更新
2. 取引対象ペアの maker/taker fee を `config/default.yaml` に反映
3. 出金手数料（BTC等）およびネットワーク手数料（ETH/BTC）を最新値に更新
4. `python -m arb_bot.backtest ...` を再実行し、コスト反映後の有効性を再評価

> 注意: 取引所手数料はVIPレベル・キャンペーン・保有トークン等で変動します。必ず実アカウント条件で再検証してください。
