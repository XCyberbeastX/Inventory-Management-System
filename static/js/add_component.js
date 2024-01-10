function convertNewlinesToBr() {
    var descriptionTextarea = document.querySelector('textarea[name="description"]');
    if (descriptionTextarea) {
        var description = descriptionTextarea.value;
        var descriptionWithLineBreaks = description.replace(/\n/g, '<br>');
        descriptionTextarea.value = "<br>" + descriptionWithLineBreaks;
    }
}
var form = document.querySelector('form');
if (form) {
    form.addEventListener('submit', convertNewlinesToBr);
}