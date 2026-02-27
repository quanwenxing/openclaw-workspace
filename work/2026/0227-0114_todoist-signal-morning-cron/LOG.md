# LOG

- 01:14: ユーザーから送信先番号を受領（+818034032911）
- 01:14: cron job作成
  - id: 3614c34f-32f5-4ebd-8b6d-bdb9b3190580
  - schedule: 0 8 * * * (Asia/Tokyo)
  - delivery: signal -> +818034032911
  - sessionTarget: isolated
