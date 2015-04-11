function submitQuery() {
  window.location.href = window.location.href.substr(0,window.location.href.indexOf('?')) + '?q=' + document.getElementById('query').value;
}
