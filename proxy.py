import zipfile
# Set your proxy server, port, username, and password
proxy_server = "brd.superproxy.io"
proxy_port = "22225"
proxy_username = "brd-customer-hl_cab77d8a-zone-residential"
proxy_password = "agajhf0mq5mh"
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (proxy_server, proxy_port, proxy_username, proxy_password)
pluginfile = 'proxy_auth_plugin.zip'
with zipfile.ZipFile(pluginfile, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)

