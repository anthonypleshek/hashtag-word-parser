var query = "";
var words = [];
var results = [];

function submitQuery() {
  window.location.href = window.location.href.substr(0,window.location.href.indexOf('&')) + "?q=" + document.getElementById("query").value;
}

function initialize(query, words, results) {
  this.query = query;
  this.words = words;
  this.results = results;
  sortResults();
}

function sortResults() {
  this.results.sort(function(a,b) {
    return getResultScore(b)-getResultScore(a);
  });
}

function getResultScore(result) {
  var score = 0;
  for(index in result) {
    score += result[index][1];
  }
  score = score/result.length;
  return score;
}
