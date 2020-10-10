

setup:
	scripts/setup.sh


run:
	@poetry run ubiquiti-monitor | tee monitoring.log; \
	exit $${PIPESTATUS[0]}


test:
	@echo
	@echo "Running the unit tests"
	@echo
	@poetry run pytest \
	--cov=ubiquiti_monitor \
  --cov-branch \
  --cov-report term-missing:skip-covered \
  .
