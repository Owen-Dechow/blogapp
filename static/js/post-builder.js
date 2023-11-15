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
            console.log(r);
            $(e.target).find("button").text("Saved");
            $(e.target).find("button").attr("disabled", false);
            $("#editor").find(".ql-editor").html(r);
        }
    });
}