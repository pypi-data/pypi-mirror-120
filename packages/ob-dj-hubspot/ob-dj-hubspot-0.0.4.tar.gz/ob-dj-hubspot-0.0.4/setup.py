from setuptools import setup

setup(
    install_requires=["django", "celery", "djangorestframework",],
    packages=[
        "ob_dj_hubspot.apis",
        "ob_dj_hubspot.apis.hubspot",
        "ob_dj_hubspot.core",
        "ob_dj_hubspot.core.hubspot",
        "ob_dj_hubspot.core.hubspot.migrations",
        "ob_dj_hubspot.core.hubspot.templates",
    ],
    tests_require=["pytest"],
    use_scm_version={"write_to": "version.py",},
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.html",],
    },
)
