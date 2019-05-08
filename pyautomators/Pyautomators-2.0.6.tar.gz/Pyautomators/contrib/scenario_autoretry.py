# -*- coding: UTF -*-
# pylint: disable=line-too-long
"""
Provides support functionality to retry scenarios a number of times before
their failure is accepted. This functionality can be helpful when you use
Pyautomators tests in a unreliable server/network infrastructure.

EXAMPLE:

.. sourcecode:: gherkin

    # -- FILE: features/alice.feature
    # TAG:  Feature or Scenario/ScenarioOutline with @autoretry
    # NOTE: If you tag the feature, all its scenarios are retried.
    @autoretry
    Feature: Use unreliable Server infrastructure

        Scenario: ...


.. sourcecode:: python

    # -- FILE: features/environment.py
    from Pyautomators.contrib.scenario_autoretry import __patch_scenario_with_autoretry

    def before_feature(context, feature):
        for scenario in feature.scenarios:
            if "autoretry" in scenario.effective_tags:
                __patch_scenario_with_autoretry(scenario, max_attempts=2)

.. seealso::

"""

from __future__ import print_function
import functools
from Pyautomators.model import ScenarioOutline
import logging

def __patch_scenario_with_autoretry(scenario, max_attempts=3):
    """Monkey-patches :func:`~Pyautomators.model.Scenario.run()` to auto-retry a
    scenario that fails. The scenario is retried a number of times
    before its failure is accepted.

    This is helpful when the test infrastructure (server/network environment)
    is unreliable (which should be a rare case).

    :param scenario:        Scenario or ScenarioOutline to patch.
    :param max_attempts:    How many times the scenario can be run.
    """
    def scenario_run_with_retries(scenario_run, *args, **kwargs):
        for attempt in range(1, max_attempts+1):
            if not scenario_run(*args, **kwargs):
                if attempt > 1:
                    message = u"AUTO-RETRY SCENARIO PASSED (after {0} attempts)"
                    ##Log para definir
                    print(message.format(attempt))
                    logging.info(message.format(attempt))
                    
                return False    # -- NOT-FAILED = PASSED
            # -- SCENARIO FAILED:
            if attempt < max_attempts:
                print(u"AUTO-RETRY SCENARIO (attempt {0})".format(attempt))
                ##Log para definir
                logging.info(u"AUTO-RETRY SCENARIO (attempt {0})".format(attempt))
        message = u"AUTO-RETRY SCENARIO FAILED (after {0} attempts)"
        ##Log para definir
        print(message.format(max_attempts))
        logging.info(message.format(max_attempts))
        return True

    if isinstance(scenario, ScenarioOutline):
        scenario_outline = scenario
        for scenario in scenario_outline.scenarios:
            scenario_run = scenario.run
            scenario.run = functools.partial(scenario_run_with_retries, scenario_run)
    else:
        scenario_run = scenario.run
        scenario.run = functools.partial(scenario_run_with_retries, scenario_run)


def scenario_retry(scenario,attempts=5,tag=None):
    if tag is None:
        __patch_scenario_with_autoretry(scenario,max_attempts=attempts)
    elif tag in scenario.effective_tags:
        __patch_scenario_with_autoretry(scenario, max_attempts=attempts)