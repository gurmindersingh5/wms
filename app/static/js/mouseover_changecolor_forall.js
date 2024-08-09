var listofItems = document.getElementsByClassName('alt-row-color');

for (var i = 0; i < listofItems.length; i++) {
  (function() {
    var originalColor = listofItems[i].style.backgroundColor;

    listofItems[i].addEventListener('mouseover', function () {
      this.style.backgroundColor = "#e09e7d";
      this.style.color = "white";
    });

    listofItems[i].addEventListener('mouseout', function () {
      this.style.backgroundColor = originalColor;
      this.style.color = "";
    });
  })();
}