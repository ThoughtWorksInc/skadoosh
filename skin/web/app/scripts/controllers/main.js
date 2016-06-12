'use strict';

angular.module('angularAppApp').controller('MainCtrl', function ($scope, $route, $timeout,$http) {
    $scope.chat = {
        status : {
            error: null,
            starting: false,
            started: false
        },
        data : {
            users: [],
            username: '',
            history: '',
            messageText: ''
        }
    }

    $scope.init = function(){
      $scope.chat.status.starting = true;
        if($scope.username){
          $scope.onMessage("Hello " + $scope.username + ", How can I help you?\n");
          $scope.chat.status.started=true
        }
    }

    $scope.send = function(question) {
        $scope.onMessage($scope.username +"  : "+question);
        $http.post("http://localhost:4000/api/help", {"text": question})
        .success(function(response, status) {
         if(response.agent_response){
             $scope.onMessage("Agent  : " +response.agent_response);
             var utterance = new SpeechSynthesisUtterance(response.agent_response);
             window.speechSynthesis.speak(utterance);
         }else{
             $scope.onMessage("Agent  : " +response.answer);
             var utterance = new SpeechSynthesisUtterance(response.answer);
             window.speechSynthesis.speak(utterance);
         }
     })

    };

    $scope.scrollBottom = function() {
        angular.element("#chat-history").scrollTop(angular.element("#chat-history")[0].scrollHeight - angular.element("#chat-history").height());
    };

    $scope.onOpen = function(e) {

        $scope.chat.status.starting = false;
        $scope.chat.status.started = true;
        $scope.chat.status.error = null;

        $scope.chat.data.username = $scope.username;
        $scope.send($scope.chat.data.username);

        $scope.$apply();

    };

    $scope.onMessage = function(message) {
        var response = message;

        $scope.chat.data.history += response + '\n';
        $scope.scrollBottom();
        $scope.$apply();
    };

    $scope.onError = function(e) {

        $scope.chat.status.error = "i should ne be called"
        $scope.chat.status.started = false;

        console.log('onerror: ', e);
        $scope.$apply();
    };

    $scope.sendButtonClicked = function() {

        if($scope.chat.data.messageText != ''){
            $scope.send($scope.chat.data.messageText);
            $scope.chat.data.messageText = '';
        }
    };

    $scope.quit = function() {
        $scope.chat.socket.close();
        $route.reload();
    };
});
