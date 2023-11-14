var draggedToolItem = null;
var focusedElement = null;

function getDraggedToolItemClone() {
    return $(`template[for=${draggedToolItem.id}]`)[0].content.cloneNode(true);
}

function elementPanelDragOver(e) {
    if (draggedToolItem)
        e.preventDefault();
}

function elementPanelDrop(e) {
    if (draggedToolItem) {
        let newElem = $(getDraggedToolItemClone()).children()[0];

        if ($(".dragging-over").length > 0)
            $(".dragging-over").first().after(newElem);
        else
            $("#post-element-panel").append(newElem);

        $(".dragging-over").removeClass("dragging-over");
        focusOn(newElem);
    }
}

function elementDragEnter(e) {
    if (draggedToolItem)
        e.target.classList.add("dragging-over");
}

function elementDragLeave(e) {
    if (draggedToolItem)
        e.target.classList.remove("dragging-over");
}

function dragStart(e) {
    draggedToolItem = e.target;
}

function dragEnd(e) {
    draggedToolItem = null;
}

function elementFocus(e) {
    focusOn(e.target);
}

function focusOn(element) {
    focusedElement = element;
    $(".focused").removeClass("focused");
    element.classList.add("focused");

    for (let li of $(".post-editor-properties li")) {
        let cssRule = $(li).attr("css-rule");
        let cssValue = element.style.getPropertyValue(cssRule);
        if (cssValue) {
            let main = $(li).find("*[main=true]");
            if ($(main).attr("type") === "color")
                $(main).val(rgbToHexColor(cssValue));
            else if ($(main).attr("unit"))
                $(main).val(cssValue.replace($(main).attr("unit"), ""));
            else
                $(main).val(cssValue);

            $(li).find("*[reset=true]")[0].checked = true;
        } else {
            $(li).find("*[reset=true]")[0].checked = false;
        }
    };
}

function rgbToHexColor(c) {
    let values = c.replace("rgb(", "").replace(")", "").split(",");
    return '#' + values.map(x => parseInt(x, 10).toString(16).padStart(2, '0')).join('');
}

function updateStyle(e) {
    if (!focusedElement)
        return false;

    let rule = $(e.target).parent().attr("css-rule");
    function setToStyle(input) {
        if ($(input).attr("unit"))
            $(focusedElement).css(rule, input.value + $(input).attr("unit"));
        else
            $(focusedElement).css(rule, input.value);

        $(input).parent().find("input[reset=true]")[0].checked = true;
    };

    if ($(e.target).attr("reset") === "true") {
        if (e.target.checked) {
            setToStyle($(e.target).parent().find("*[main=true]")[0]);
        }
        else {
            focusedElement.style.setProperty(rule, null);
        }

    } else {
        setToStyle(e.target);
    }
}

function saveForm(e) {
    e.preventDefault();
    $(e.target).find("button").attr("disabled", true);
    $(e.target).find("button").text("Saving ...");

    let postId = $(".post-editor").attr("post-id");
    if (!postId) postId = -1;

    let formdata = $(e.target).serializeArray();
    let data = {};
    $(formdata).each(function (index, obj) {
        data[obj.name] = obj.value;
    });

    data["post-content"] = $("#post-element-panel").html();
    data["post-id"] = postId;

    $.ajax({
        url: "/save-post",
        type: "POST",
        data: data
    });
}