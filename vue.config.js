module.exports = {
    pluginOptions: {
        electronBuilder: {
            builderOptions: {
                "extraFiles": [
                    "./bin/**"
                ],
                "mac": {
                    "binaries": ["bin/"],
                    "icon": "src/assets/logo.png"
                }
            }
        }
    }
}