
/**
 * Global variable that stores the current URL
 */
let url;


/**
 * Clickstream collection
 */
document.addEventListener('DOMContentLoaded', function()
{

  // first loaded
  if (url != location.href) {
    url = location.href
    sendToBackground(url)
  }

  // handling for single page applications
  document.body.addEventListener('click', ()=>{
      requestAnimationFrame(()=>{
        if (url !== location.href) {
          url = location.href;
          sendToBackground(url)
        }
      });
  }, true);

  // handling back/forward button
  (function() {
    if (window.history && window.history.pushState) {
      window.onpopstate = function(event) {
        if (url !== location.href) {
          url = location.href;
          sendToBackground(url)
        }
      };
    }
  })();
});

/**
 * send message to background.js
 */
function sendToBackground(data) {
  chrome.runtime.sendMessage(
    data, 
    function(response) {
      try {

          var responseObj = JSON.parse(response);
          // do nothing if not OK
          if (responseObj.message != 'OK') {
            console.log('NOT OK')
            return
          }
          var next = responseObj.next;
          var dest = responseObj.destination;
          var prod = responseObj.productivity;
          makeDecision(next, dest, prod);

      } catch (err) {
        console.log('ERROR: ', err)
      }
    }
  );
}

/**
 * decide should present the prediction or not
 * @param {Array} next array of url and confidence
 * @param {Array} destination array of url and confidence
 * @param {int} productivity productivity from 0 to 100
 */
function makeDecision(next, destination, productivity) {
  console.log(next, destination, productivity);

  // next and destination, display if confidence lager than 80% and random number less than 0.5
  if (next.length >= 1 && next[0].confidence > 80 && Math.random() < 0.5) {
    displayNext(next[0].url, next[0].description)
  }
  if (destination.length >= 1 && destination[0].confidence > 80 && Math.random() < 0.5) {
    displayDestination(destination[0].url, destination[0].description)
  }

  // productivity becomes low, then randomly display notifications
  if (productivity < 50 && Math.random() < 0.5) {
    lowProductivity(productivity)
  }
}

function displayNext(url, message) {
  console.log('display')
  Toastify({
    text: 'Are you looking for: ' + message,
    duration: 6000,
    destination: url,
    newWindow: true,
    close: true,
    gravity: "top", // `top` or `bottom`
    positionLeft: false, // `true` or `false`
    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
  }).showToast();
}

function displayDestination(url, message) {
  console.log('display')
  Toastify({
    text: 'You probablly looking for: ' + message,
    duration: 6000,
    destination: url,
    newWindow: true,
    close: true,
    gravity: "top", // `top` or `bottom`
    positionLeft: false, // `true` or `false`
    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
  }).showToast();
}

function lowProductivity(prod) {
  Toastify({
    text: 'Your current productivity is low: ' + prod + '%',
    duration: 3000,
    destination: url,
    newWindow: true,
    close: true,
    gravity: "top", // `top` or `bottom`
    positionLeft: false, // `true` or `false`
    // backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
    backgroundColor: "linear-gradient(to right, #b02900, #c9703d)",
  }).showToast();
}

/**
 * Handling tab changes
 */

// if tab changes, send message to server for collecting clickstream.
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse)
{
  if(request.cmd == 'tabchange') {
    // NOTE: no matter the url changes or not, send the tab change event url
    // it should be consider as a clickstream event
    url = location.href
    sendToBackground(url)
    
    // console.log('tabchange collected: ', request.value)
    sendResponse('message recived in content!');
  }
});