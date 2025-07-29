# Changelog

## [1.5.1](https://github.com/zentrum-lexikographie/gdex/compare/v1.5.0...v1.5.1) (2025-07-29)


### Dependencies

* prepare v1.5.1 ([5d9d396](https://github.com/zentrum-lexikographie/gdex/commit/5d9d39602a8b941979378ed3456f786d1040cd98))

## [1.5.0](https://github.com/zentrum-lexikographie/gdex/compare/v1.4.1...v1.5.0) (2025-07-25)


### Features

* Extend _de_whitelist and _de_vulger_blacklist ([0d4b662](https://github.com/zentrum-lexikographie/gdex/commit/0d4b662ed9a5b72334a29fe7b0fec9b4e3badde4))
* Modify _de_is_deixis, revise default terms ([6fd7612](https://github.com/zentrum-lexikographie/gdex/commit/6fd7612559b953348a29eff1ab303bbdc19b1fee))

## [1.4.1](https://github.com/zentrum-lexikographie/gdex/compare/v1.4.0...v1.4.1) (2025-07-03)


### Bug Fixes

* Do not lock project dependencies, allowing for platform-dependent installs ([9aebc4c](https://github.com/zentrum-lexikographie/gdex/commit/9aebc4ce51af037b559e4bb297a560bde7b8a6da))


### Dependencies

* prepare release v1.4.1 ([48fb59e](https://github.com/zentrum-lexikographie/gdex/commit/48fb59efce0b428e036dc0778d0ff10485a10924))

## [1.4.0](https://github.com/zentrum-lexikographie/gdex/compare/v1.3.1...v1.4.0) (2025-06-25)


### Features

* Adjust default penalties for hypotaxis and deixis ([8a6b882](https://github.com/zentrum-lexikographie/gdex/commit/8a6b882c5e6f015b17de8695b4ef72a170ee8b5a))
* Base project on ZDL custom spaCy models, pin dependencies ([b5032c2](https://github.com/zentrum-lexikographie/gdex/commit/b5032c2018f8e04936f2216a50b1d1abeefafd26))
* Change tagline of project, explaining origin of GDEX acronym ([701c6da](https://github.com/zentrum-lexikographie/gdex/commit/701c6da2a121d272a61e64bb58e9e6e37d0bf4f0))
* Exclude conjunctions and pronominal adverbs as rare lemmas ([557d446](https://github.com/zentrum-lexikographie/gdex/commit/557d44640e6ec63457a8d91eb600be962112509e))
* Exclude more variations/spellings of blacklisted words from whitelist ([99a8674](https://github.com/zentrum-lexikographie/gdex/commit/99a8674d5e4ecaf44dcddc84ae3256c2124ec4f3))
* Increase default value for penalty_blacklist (now equal to penalty_named_entity) ([b4c6157](https://github.com/zentrum-lexikographie/gdex/commit/b4c61574308cb975ad09d5acaa6a9acb5616c61c))
* Increase impact of notkeyboardchar (square penalty) ([30b8896](https://github.com/zentrum-lexikographie/gdex/commit/30b8896bd630cb5dd99abd1eb3a47e53d48d190a))
* Redefine hit_in_subordinate_clause ([959cc42](https://github.com/zentrum-lexikographie/gdex/commit/959cc4208b6295e9f11239cbbdd8281cd0ac7560))
* Remove hyphen-minus from _DEFAULT_RARE_CHARS ([c4278ce](https://github.com/zentrum-lexikographie/gdex/commit/c4278ceed5b34298d68ec1c19e35392bd7be3b22))
* Update _DEFAULT_ILLEGAL_CHARS and _DEFAULT_RARE_CHARS ([f411752](https://github.com/zentrum-lexikographie/gdex/commit/f41175246213003be09a198804ebf187eec3600f))
* Update dependencies and tests ([4da1400](https://github.com/zentrum-lexikographie/gdex/commit/4da1400478b6178a25469433d50ee7e2c8ef89e5))
* Use custom Token attribute is_hit instead of kwarg headword ([d41820b](https://github.com/zentrum-lexikographie/gdex/commit/d41820b52d7654753d943f7002aab71d96d9d8e2))

## [1.3.1](https://github.com/zentrum-lexikographie/gdex/compare/v1.3.0...v1.3.1) (2025-04-10)


### Bug Fixes

* Exclude relevant POS in factor_rarelemmas ([e687826](https://github.com/zentrum-lexikographie/gdex/commit/e68782602515e7da88e8dd1819daf8676d5b2099))

## [1.3.0](https://github.com/zentrum-lexikographie/gdex/compare/v1.2.2...v1.3.0) (2025-04-10)


### Features

* Extract German whitelist from DWDS lemma list ([f72044d](https://github.com/zentrum-lexikographie/gdex/commit/f72044d02853c545275b7ee76d14f207c66498e1))

## [1.2.2](https://github.com/zentrum-lexikographie/gdex/compare/v1.2.1...v1.2.2) (2025-02-24)


### Bug Fixes

* Only set extension "is_hit" if not yet existing ([9e5a182](https://github.com/zentrum-lexikographie/gdex/commit/9e5a1822904598723e924f5c59a6016ce990e736))

## [1.2.1](https://github.com/zentrum-lexikographie/gdex/compare/v1.2.0...v1.2.1) (2025-02-21)


### Bug Fixes

* Declare required token annotation "is_hit" in main module ([af2b93c](https://github.com/zentrum-lexikographie/gdex/commit/af2b93c51b8522d85595e63468dcc8326a3e4e1e))

## [1.2.0](https://github.com/zentrum-lexikographie/gdex/compare/v1.1.0...v1.2.0) (2025-02-11)


### Features

* penalize subordinate clauses ([12e4208](https://github.com/zentrum-lexikographie/gdex/commit/12e4208d0ad27f33bcbc18b97a04d39edfcf9e00))


### Bug Fixes

* **Documentation:** Corrects description of score range ([9d73907](https://github.com/zentrum-lexikographie/gdex/commit/9d73907cbdba8bd64212190f69a4698f5f3ba99d))
* **Project:** Add @Natalie-T-E as contributor ([a32947f](https://github.com/zentrum-lexikographie/gdex/commit/a32947f17b3ede4e4c890f4590f36fc983eface8))

## [1.1.0](https://github.com/zentrum-lexikographie/gdex/compare/v1.0.1...v1.1.0) (2024-12-19)


### Features

* Define valid sentence endings more strictly ([04e128a](https://github.com/zentrum-lexikographie/gdex/commit/04e128a73f6f1aa658588d8798c4d3b8cf3b418c))

## [1.0.1](https://github.com/zentrum-lexikographie/gdex/compare/v1.0.0...v1.0.1) (2024-11-25)


### Bug Fixes

* adds py.typed marker ([4a873c3](https://github.com/zentrum-lexikographie/gdex/commit/4a873c374ef0c7cee8a8c29c686b5dd78186627f))

## 1.0.0 (2024-11-25)


### Miscellaneous Chores

* release 1.0.0 ([b163278](https://github.com/zentrum-lexikographie/gdex/commit/b163278bfcbbe11d7c87f63c0f16e44f183d6fa1))
