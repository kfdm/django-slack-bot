# v0.9.0 - 2023-08-18

- [IMPROVEMENT] Add initial test bot implementation #11

# v0.8.1 - 2023-07-02

- [BUGFIX] Swap import order #9

# v0.8.0 - 2022-07-26

- [BUGFIX] Ensure links are unescaped when returned from text processing #6
- [BUGFIX] Fix reference to settings
- [IMPROVEMENT] Add a settings wrapper to simplify and better document settings #5
- [IMPROVEMENT] ignore_bots and ignore_users decorators #3

# v0.7.0 - 2022-07-08

- [IMPROVEMENT] Add initial test cases #1
- [IMPROVEMENT] Additional exceptions and exception cleanup #2

# v0.6.1 - 2022-06-16

- [CHANGE] Return JUST the .data values for now when using tasks.api_call

# v0.6.0 - 2022-06-08

- [CHANGE] Remove the forced ignore_result on our api_call shared_task
- [CHANGE] Use StreamHandler/Formatter directly to maintain more control
- [CHANGE] Use importlib.metadata over pkg_resources
