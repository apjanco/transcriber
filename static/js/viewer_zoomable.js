function initImage(textName, pageNumber) {
    var fixedName = textName.replace(/ /g, "-");
    var url = "//ticha.haverford.edu/images/dzi/" + fixedName + pageNumber + ".dzi";
    $("#openseadragon1").html("")
    var viewer = OpenSeadragon({
        id: "openseadragon1",
        prefixUrl: "http://ticha.haverford.edu/images/openseadragon/",
        tileSources: url,
        showNavigator: true,
        navigatorPosition: "ABSOLUTE",
        navigatorTop: "40px",
        navigatorLeft: "4px",
        navigatorHeight: "110px",
        navigatorWidth: "90px",
        referenceStripScroll: 'horizontal',
    });
}
