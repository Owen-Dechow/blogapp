var saveTimeoutHandler;
var lastSave;
var saving;
var contentOnLastSave;

function savePost(e) {
    e.preventDefault();
    $(e.target).find("button").attr("disabled", true);
    $(e.target).find("button").text("Saving ...");

    let formdata = $(e.target).serializeArray();
    let data = {};
    $(formdata).each(function (index, obj) {
        data[obj.name] = obj.value;
    });

    contentOnLastSave = getSaveSig();
    data["content"] = contentOnLastSave;
    data["post_id"] = $("#editor").attr("post-id");
    data["blog_name"] = $("#editor").attr("blog-name");

    saving = true;
    $.ajax({
        url: "/save-post/",
        type: "POST",
        data: data,
        success: (r) => {
            saving = false;
            $(e.target).find("button").attr("disabled", false);
            $("#editor").attr("post-id", r["post-id"]);

            if (!saveTimeoutHandler)
                $(e.target).find("button").text("Saved (No detected changes)");
        }
    }).fail((r) => {
        saving = false;
        $(e.target).find("button").attr("disabled", false);
        $(e.target).find("button").text("Save failed, try again");
    });
}

function checkChange() {
    if (getSaveSig() !== contentOnLastSave) {
        changeDetected();
    }

    window.setTimeout(checkChange, 100);
}

function preventDoubleSave() {
    if (saving) {
        saveTimeoutHandler = window.setTimeout(preventDoubleSave, 100);
        return;
    }

    lastSave = new Date().toLocaleString();
    $(".save-post").submit();
    saveTimeoutHandler = null;
}

function changeDetected() {
    if (lastSave)
        $(".save-post button[type=submit]").text(`Save unsaved changes (Last save ${lastSave})`);
    else
        $(".save-post button[type=submit]").text(`Save unsaved changes`);

    if (saveTimeoutHandler)
        window.clearTimeout(saveTimeoutHandler);

    contentOnLastSave = getSaveSig();
    saveTimeoutHandler = window.setTimeout(preventDoubleSave, 5 * 1000);
};

function getSaveSig() {
    return $("#post_name").val() + quill.root.innerHTML;
}