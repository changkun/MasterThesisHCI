
/**
 * Global variable that stores the current URL
 */
let url;


/**
 * Clicked element collection
 */
document.addEventListener('click', function(e) {
  e = e || window.event;
  var target = e.target || e.srcElement,
      text = target.textContent || target.innerText;

  console.log(e.clientX, e.clientY)
  console.log(target);
}, false);


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
      } catch (err) {
        console.log('ERROR: ', err)
      }
    }
  );
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