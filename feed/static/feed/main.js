// var subjectObject = {
//   "Apple": {
//     "Stocks": ["Apple", "Microsoft", "Meta", "Amazon", "Google", "Walmart", "VOO"],
//     "CSS": ["Borders", "Margins", "Backgrounds", "Float"],
//     "JavaScript": ["Variables", "Operators", "Functions", "Conditions"]    
//   },
//   "Back-end": {
//     "PHP": ["Variables", "Strings", "Arrays"],
//     "SQL": ["SELECT", "UPDATE", "DELETE"]
//   }
// }

var subjectObject = {
  "Apple": {
    "Start Date": ["Price", "Volatility"],
    "End Date": ["Price", "Volatility"],
    "Forecast": ["Price", "Volatility"]
  },
  "VOO": {
    "Attributes": ["Price", "Volatility"]
  },
  "Google": {
    "Attributes": ["Price", "Volatility"]
  }
}
window.onload = function() {
  var subjectSel = document.getElementById("stock");
  var topicSel = document.getElementById("start_date");
  var chapterSel = document.getElementById("end_date");
  var chapterSel = document.getElementById("forecast");
  for (var x in subjectObject) {
    subjectSel.options[subjectSel.options.length] = new Option(x, x);
  }
  subjectSel.onchange = function() {
    //empty Chapters- and Topics- dropdowns
    chapterSel.length = 1;
    topicSel.length = 1;
    //display correct values
    for (var y in subjectObject[this.value]) {
      topicSel.options[topicSel.options.length] = new Option(y, y);
    }
  }
  topicSel.onchange = function() {
    //empty Chapters dropdown
    chapterSel.length = 1;
    //display correct values
    var z = subjectObject[subjectSel.value][this.value];
    for (var i = 0; i < z.length; i++) {
      chapterSel.options[chapterSel.options.length] = new Option(z[i], z[i]);
    }
  }
}