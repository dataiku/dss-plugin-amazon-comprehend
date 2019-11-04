PLUGIN_VERSION=2.0.0
PLUGIN_ID=amazon-comprehend

plugin:
    cat plugin.json|json_pp > /dev/null
    rm -rf dist
    mkdir dist
    zip -r dist/dss-plugin-${PLUGIN_ID}-${PLUGIN_VERSION}.zip plugin.json python-lib custom-recipes code-env

include ../Makefile.inc