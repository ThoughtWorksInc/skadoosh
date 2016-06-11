'use strict';

var server = "http://localhost:4000/api/help";
// var server = "http://angularjs-chat-server.aws.af.cm/chat";

angular.module('angularAppApp').factory('chatService', function($http) {
    return {

        // RETURNS SockJS object
        socket : function(){
            return new SockJS(null, null, {debug: true});
        }

    }
});
