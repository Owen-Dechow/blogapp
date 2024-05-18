function flagPost(e) {
    e.preventDefault();

    let user = $(".post-author").text();

    if (!confirm(`Are you sure you want to report this post by ${user}?`))
        return;

    let commentId = $("#post-content").attr("post-id");
    $.ajax({
        method: "POST",
        url: `/flag-post/${commentId}`,
        data: $(e.target).serialize(),
        success: () => {
            alert("Post reported: awaiting review.");
            e.target.remove();
        }
    }).fail(() => {
        alert("Report failed to send. Please try again.");
    });
}