/* global chrome: true */

jQuery(document).ready(function() {
    jQuery('.update-chrome-extension-hosturl').click(function() {
        if (chrome && chrome.runtime) {
            var extensionId = 'kfninnbnfofmpjhlgkikjplmahfjkhjp';
            chrome.runtime.sendMessage(
                extensionId, {
                    command: 'updatesettings'
                }, function(response) {
                });
            var $el = jQuery('.update-chrome-extension-feedback');
            $el.hide();
            $el.text('Settings updated.');
            $el.fadeIn();
        }
    });
});
