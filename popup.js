//params - time spent / random noise, max word length

// submitBtn
// to get input values you can use document.getElementById().value
// class: syllable
submitBtn.addEventListener("click", function () {
    console.log("submitted values");
    const timeOffset = document.getElementById('timeInput').value;
    const maxLength = document.getElementById('maxLengthInput').value;
    chrome.tabs.query({ active: true }, function(tabs) {
        const { id: tabId } = tabs[0].url;
        chrome.tabs.executeScript(tabId, {runAt: 'document_end', code: 'document.querySelectorAll(.syllable)'}, function(result) {
            console.log(result);
        })
    })
})