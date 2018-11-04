'use strict';

/**
 * Global variables for collecting events
 */
const server = 'http://0.0.0.0:12346/api/v1/recv'

/**
 * Variables initialized after plugin installed
 */
let userID = null;
let lastURL = null;
let lastCollectEvent = null;

function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}
chrome.runtime.onInstalled.addListener(function() {
  userID = guid();
  localStorage.setItem('user_id', userID);
  lastURL = '';
});

/**
 * Post clickstream data to server
 */

chrome.runtime.onMessage.addListener(function(url, sender, sendResponse) {
  postCollection(url, function (response) {
    savePredictionHistory(response)
    sendResponse(response);
  })
  return true // declare async
});

function postCollection(url, callback) {
  var request = new XMLHttpRequest();
  request.open('POST', server, true);

  // response callback
  request.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      callback(this.responseText)
    }
  };

  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

  if (userID === '') {
    userID = localStorage.getItem('user_id')
  }

  var data = {
    user_id: userID,
    previous_url: lastURL,
    current_url: url,
    stay_seconds: '0',
    time: Now()
  }
  // update last url
  lastURL = url

  // calculate residence seconds
  if (lastCollectEvent != null) {
    var current = new Date()
    data.stay_seconds = (current.getTime() - lastCollectEvent.getTime()) / 1000;
    data.stay_seconds = data.stay_seconds.toString()
    // update last collect event
    lastCollectEvent = current
  } else {
    lastCollectEvent = new Date()
  }
  console.log('final data: ', data)

  request.send(JSON.stringify(data));
}

let responseHistory = null
function savePredictionHistory(response) {
  responseHistory = response
}
function getPredictionHistory() {
  return responseHistory
}

/**
 * generating ISO date string
 */

function ISODateString(d){
  function pad(n){return n<10 ? '0'+n : n}
  return d.getUTCFullYear()+'-'
       + pad(d.getUTCMonth()+1)+'-'
       + pad(d.getUTCDate())+'T'
       + pad(d.getUTCHours())+':'
       + pad(d.getUTCMinutes())+':'
       + pad(d.getUTCSeconds())+'Z'
}

function Now() {
  var d = new Date();
  return ISODateString(d)
}


/**
 * Detects tab change
 */

function sendMessageToContentScript(message, callback)
{
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, message, function(response) {
      if(callback) callback(response);
    });
  });
}

chrome.tabs.onActivated.addListener(function(activeInfo) {
  sendMessageToContentScript({
    cmd:'tabchange', 
    value: activeInfo,
  }, function(response) {
    console.log('response from content ' + response);
  });
});