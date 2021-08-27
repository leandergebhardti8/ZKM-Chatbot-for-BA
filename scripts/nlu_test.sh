#!/bin/bash
rasa test core --e2e --stories tests/conversation_tests.md --out stories_results --debug --verbose
rasa test nlu -u data/nlu.md --config config.yml --cross-validation --out nlu_results --successes
python3 scripts/nlu_errors.py