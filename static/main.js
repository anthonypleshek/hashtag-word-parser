var results = [];

function submitQuery() {
  console.log('here');
}

function sortResults(results) {
  this.results = results;
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
