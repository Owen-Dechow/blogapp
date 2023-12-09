var saveTimeoutHandler;
var lastSave;
var saving;
var contentOnLastSave;
var bannerImageSaved = true;

function savePost(e) {
    e.preventDefault();
    $(e.target).find("button").attr("disabled", true);
    $(e.target).find("button").text("Saving ...");

    let formdata = $(e.target).serializeArray();
    let data = {};
    $(formdata).each(function (index, obj) {
        data[obj.name] = obj.value;
    });

    console.log(quill.root.innerHTML);
    contentOnLastSave = quill.root.innerHTML;
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
    if (quill.root.innerHTML !== contentOnLastSave) {
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

    contentOnLastSave = quill.root.innerHTML;
    saveTimeoutHandler = window.setTimeout(preventDoubleSave, 5 * 1000);
};

function selectBannerImage(e) {
    $(e.target).find("input[type=file]").click();
}

function bannerImageSelected(e) {
    let file = e.target.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = re => {
        $(e.target).closest(".banner-select").find("img").attr("src", re.target.result);
        bannerImageSaved = false;
    };
}