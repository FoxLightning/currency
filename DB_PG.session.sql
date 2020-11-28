SELECT max(id), source, currency, MAX(created)
FROM rate_rate
GROUP BY source, currency