# Changelog

## 0.1.0 (2026-08-04)


### Features

* **checker:** run() + DriftReport with missing-literal detection ([c6edb92](https://github.com/assaads/docdrift/commit/c6edb929c8e3fdded8d194679cf45b34d6704687))
* **ci:** reusable docs-drift workflow + self-contained fallback ([9a644d9](https://github.com/assaads/docdrift/commit/9a644d9cdf144808844ca4ef0108d85022f57a87))
* **cli:** check / init / list commands ([08f5677](https://github.com/assaads/docdrift/commit/08f567756ca4dc2d168ecb5522b82186eaf16c24))
* **config:** load_first + manifest version guard ([01ac424](https://github.com/assaads/docdrift/commit/01ac4240439d0c4dc4fd2c791c655d54b5d03699))
* **core:** Extractor Protocol, Context, Registry ([12653c1](https://github.com/assaads/docdrift/commit/12653c12bbff6614cab1df6e8873876b35b2cd73))
* dogfood manifest + README + self-CI ([0863a13](https://github.com/assaads/docdrift/commit/0863a13d40ffad393622dadb5df3c7cc87490948))
* **extractors:** typer/click/argparse/files+regex extractors ([3bd6963](https://github.com/assaads/docdrift/commit/3bd696382b9c923ff61bcd2050b2e6c98434436e))
* **manifest:** pydantic Manifest + open Source model ([ca79894](https://github.com/assaads/docdrift/commit/ca7989409e0c798d436dd26f88871debbdacac68))
* **pytest:** pytest11 plugin — .docdrift.yml auto-collects test_docdrift ([d546b39](https://github.com/assaads/docdrift/commit/d546b39465e92039274ac711d514aabbf62bc522))
* **skill:** docs-drift-guard skill (detection + scaffolding) ([ccf093e](https://github.com/assaads/docdrift/commit/ccf093e6fb66f0c454f457678a79f4e57652f51d))


### Bug Fixes

* **ci:** pin release-please-action to real v5.0.0 SHA ([7c5e723](https://github.com/assaads/docdrift/commit/7c5e72395325d1b2accee75e97b6add2032ea6b8))
* **extractors:** resolve src-layout packages under isolated uvx ([44f610d](https://github.com/assaads/docdrift/commit/44f610d21e5dbffa0e6a0dbbf1a740e50a82ccd2))
* harden checker/cli/config per adversarial review (missing-doc, per-doc match, format validation, init templates/guard, non-dict YAML, empty-items warning) ([18e2171](https://github.com/assaads/docdrift/commit/18e2171bfb65336b46457b14a11ba78df856316d))
