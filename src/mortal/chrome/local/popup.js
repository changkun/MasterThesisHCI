
let history = JSON.parse(chrome.extension.getBackgroundPage().getPredictionHistory())

console.log('popup script: ', history)

function makeUL(arr) {
  if (arr == null) {
    return null
  }

  let list = document.createElement('ul');
  let length = arr.length
  if (length > 10) {
    length = 10
  }
  for (let i = 0; i < length; i++) {
    let item = document.createElement('li');
    var a = document.createElement('a');
    a.appendChild(document.createTextNode(arr[i].description));
    a.href = arr[i].url
    a.target = '_blank'
    item.appendChild(a)
    list.appendChild(item);
  }
  return list
}

// add behavior
if (history.productivity < 40) {
  document.getElementById('prod-val').innerHTML = 'Exploring'
  document.getElementById('prod-val').style.color = '#ba592e'
} else if (history.productivity >= 40 && history.productivity <= 60) {
  // document.getElementById('prod-val').innerHTML = ''
  // document.getElementById('prod-val').style.color = 'gray'
} else {
  document.getElementById('prod-val').innerHTML = 'Goal-oriented viewing'
  document.getElementById('prod-val').style.color = '#38ad76'
}

// add next lists
document.getElementById('next-list').innerHTML = ''
document.getElementById('next-list').appendChild(makeUL(history.next))

// add destinations
document.getElementById('dest-list').innerHTML = ''
document.getElementById('dest-list').appendChild(makeUL(history.destination))