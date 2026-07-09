# 50-asr / recovery-plan-sales-prod

Recovery Plan 순서:

1. Pre Action: `dr-precheck`
2. Group 1: DB VM
3. Group 2: WAS VM
4. Group 3: WEB VM
5. Final Action: `dr-dns-switch`, `dr-inventory-update`
