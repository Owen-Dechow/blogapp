var saveTimeoutHandler;
var lastSave;

function savePost(e) {
    e.preventDefault();
    $(e.target).find("button").attr("disabled", true);
    $(e.target).find("button").text("Saving ...");

    let postId = $(".editor").attr("post-id");
    if (!postId) postId = -1;

    let formdata = $(e.target).serializeArray();
    let data = {};
    $(formdata).each(function (index, obj) {
        data[obj.name] = obj.value;
    });

    data["content"] = quill.root.innerHTML.trim();
    data["post-id"] = postId;

    $.ajax({
        url: "/save-post",
        type: "POST",
        data: data,
        success: (r) => {
            $(e.target).find("button").attr("disabled", false);

            if (!saveTimeoutHandler)
                $(e.target).find("button").text("Saved (No detected changes)");
        }
    }).fail((r) => {
        $(e.target).find("button").attr("disabled", false);
        $(e.target).find("button").text("Save failed, try again");
    });
}

function checkChange() {
    if (quill.root.innerHTML !== contentOnLastSave) {
        changeDetected();
    }

    window.setTimeout(checkChange, 100);
}

function changeDetected() {
    if (lastSave)
        $(".save-post button[type=submit]").text(`Save unsaved changes (Last save ${lastSave})`);
    else
        $(".save-post button[type=submit]").text(`Save unsaved changes`);

    if (saveTimeoutHandler)
        window.clearTimeout(saveTimeoutHandler);

    contentOnLastSave = quill.root.innerHTML;
    saveTimeoutHandler = window.setTimeout(() => {
        lastSave = new Date().toLocaleString();
        $(".save-post").submit();
        saveTimeoutHandler = null;
    }, 5 * 1000);
};
