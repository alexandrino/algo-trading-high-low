invoke_trade_high_low:
	sls invoke local -f trade_high_low

invoke_trade_sma:
	sls invoke local -f trade_sma

deploy:
	sls deploy

test:
	pytest --cov=. --cov-report term-missing --cov-fail-under=72 -vv ./tests


build:
	git pull origin main
	docker build -t trade-bot .

run:
	docker run -d -t trade-bot