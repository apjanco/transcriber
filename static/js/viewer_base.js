function documentViewerInit(textName, thisPage, lastPage, pageMap) {
    $("#jumpToInput").keypress(function (event) {
        if (event.which === 13) {
            var userVal = $(this).val();
            if (!(userVal in pageMap) && !userVal.endsWith('v') && !userVal.endsWith('r')) {
                userVal += 'r';
            }
            if (userVal in pageMap) {
                thisPage = parseInt(pageMap[userVal]);
            }
            initPage(textName, lastPage, thisPage);
            $(this).val("");
        }
    });
    // Fade the image after a page flip before the next image is loaded
    $("#pageImage").load(function () {
        $(this).removeClass("faded-image");
    });
    // Unselect buttons when focus is lost.
    // Courtesy of stackoverflow.com/questions/23443579
    $(".btn").mouseup(function () {
        $(this).blur();
    });
    $(".first-button").click(function () {
        thisPage = 0;
        initPage(textName, lastPage, thisPage);
    });
    $(".previous-button").click(function () {
        thisPage--;
        initPage(textName, lastPage, thisPage);
    });
    $(".next-button").click(function () {
        thisPage++;
        initPage(textName, lastPage, thisPage);
    });
    $(".last-button").click(function () {
        thisPage = lastPage;
        initPage(textName, lastPage, thisPage);
    });
    initPage(textName, lastPage, thisPage);
}

function initPage(textName, lastPage, pageNumber) {
    $("#tab1-slug").html("");
    $("#tab2-slug").html("");
    if (pageNumber >= lastPage) {
        $(".next-button").addClass("disabled");
        pageNumber = lastPage;
    } else {
        $(".next-button").removeClass("disabled");
    }
    if (pageNumber <= 0) {
        $(".previous-button").addClass("disabled");
        pageNumber = 0;
    } else {
        $(".previous-button").removeClass("disabled");
    }
    var pageURL = window.location.href;
    var splitURL = pageURL.split("/");
    splitURL[6] = pageNumber.toString();
    window.history.pushState("","",splitURL.join("/"));
    initImage(textName, pageNumber);
    var downloadURL = '/texts/' + textName + '/' + pageNumber
    $("#download-anchor").attr("href", getDownloadURL(textName, pageNumber, "original"));
    $.get(getJsonURL(textName, pageNumber), function (data) {
        $("#tab1-slug").html(data['transcription']).promise().done(initPopovers);
        $("#tab2-slug").html(data['transcription_regular']).promise().done(initPopovers);
        document.title = "Page " + data['n'] + " of " + capitalize(textName);
    });
}

function getJsonURL(textName, pageNumber) {
    var fixedName = textName.replace(/ /g, "-");
    return "/texts/" + fixedName + "/" + pageNumber + "/json";
}

function getDownloadURL(textName, pageNumber, mode) {
    var fixedName = textName.replace(/ /g, "-");
    return "/texts/" + fixedName + "/" + pageNumber + "/" + mode + "/download";
}

// Courtesy of stackoverflow.com/questions/1026069
function capitalize(string) {
    return string.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.slice(1); } );
}
