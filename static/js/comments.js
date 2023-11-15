function submitComment(e) {
    e.preventDefault();

    $.ajax({
        url: "/comment",
        type: "POST",
        data: $(e.target).serialize(),
        success: (r) => {
            commentSuccessful(e, r);
        }
    });
}

function commentSuccessful(e, r) {
    if (r["success"]) {
        let comment = $("#comment-template")[0].content.cloneNode(true);
        $(comment).find(".comment-content").text($(e.target).find("*[name=content]").val());

        if ($(e.target).find("*[name=parent]").val()) {
            $(comment).find("button[type=button]").remove();
            $(e.target).parent().find(".replies").first().prepend(comment);
            e.target.remove();
        }
        else {
            $(comment).find(".comment").attr("comment-id", r["comment-id"]);
            $("#comments").prepend(comment);
            e.target.reset();
        }
    }
    else { }
}

function reply(e) {
    $(".open-comment-reply-form").remove();

    let form = $("#comment-form-template")[0].content.cloneNode(true);
    $(form).find("*[name=parent]").val($(e.target).parent().attr("comment-id"));
    $(form).find("*").first().addClass("open-comment-reply-form");
    $(e.target).closest(".comment").find(".reply-section").first().prepend(form);
}

function cancelReply(e) {
    if ($(e.target).closest(".comment").attr("comment-id")) {
        $(e.target).closest("form").remove();
    } else {
        $(e.target).closest("form").trigger("reset");
    }
}

function loadReplies(e) {
    data = {
        "parent": $(e.target).closest(".comment").attr("comment-id"),
        "loaded": $(e.target).closest(".comment").find(".replies").attr("loaded")
    };

    $.ajax({
        url: "/get-replies",
        type: "GET",
        data: data,
        success: (r) => {
            r["objects"].forEach(element => {
                let comment = $("#comment-template")[0].content.cloneNode(true);
                $(comment).find("button[type=button]").remove();
                $(comment).find(".comment-user").text(element["user"]);
                $(comment).find(".comment-content").text(element["content"]);
                $(e.target).closest(".comment").find(".replies").attr("loaded", r["loaded"]);
                $(e.target).closest(".comment").find(".replies").first().append(comment);

            });

            if (r["remaining"] == 0) {
                $(e.target).find(".reply-count").closest("button").remove();
            } else {
                $(e.target).find(".reply-count").text(r["remaining"]);
            }
        },
    });
}

function loadComments(e) {
    data = {
        "post": $(e.target).attr("post"),
        "loaded": $("#comments").attr("loaded")
    };

    $.ajax({
        url: "/get-comments",
        type: "GET",
        data: data,
        success: (r) => {
            r["objects"].forEach(element => {
                let comment = $("#comment-template")[0].content.cloneNode(true);
                $(comment).find(".comment-user").text(element["user"]);
                $(comment).find(".comment-content").text(element["content"]);
                $(comment).find(".comment").attr("comment-id", element["id"]);

                if (element["replies"] == 0) {
                    $(comment).find(".reply-count").closest("button").remove();
                } else {
                    $(comment).find(".reply-count").text(element["replies"]);
                }

                $("#comments").append(comment);
            });

            $("#comments").attr("loaded", r["loaded"]);

            if (r["remaining"] == 0) {
                e.target.remove();
            }
        }
    }
    );
}