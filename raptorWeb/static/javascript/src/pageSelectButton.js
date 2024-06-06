var select_1 = $('#select-button-1')
var select_2 = $('#select-button-2')
var select_3 = $('#select-button-3')

var section_1 = $('#page_content')
var section_2 = $('#page_cssjs')
var section_3 = $('#page_seo')

var select_list = [select_1, select_2, select_3 ]

function resetButtonStates(button) {
    if (button.hasClass('btn-primary')) {
        button.toggleClass('btn-primary')
    }
    if (button.hasClass('btn-secondary')) {
        void 0;
    }
    else {
        button.toggleClass('btn-secondary')
    }
}

document.getElementById('select-button-1').addEventListener('click', function(e) {
    if (select_1.hasClass('btn-primary')) {
        void 0;
    }
    else {
        select_list.forEach(resetButtonStates)
        select_1.toggleClass('btn-secondary')
        select_1.toggleClass('btn-primary')
    }
    if (document.getElementById('page_content').style.display === 'block') {
        void 0
    }
    else {
        section_1.css('display','block')
        section_2.css('display','none')
        section_3.css('display','none')
    }
});

document.getElementById('select-button-2').addEventListener('click', function(e) {
    if (select_2.hasClass('btn-primary')) {
        void 0;
    }
    else {
        select_list.forEach(resetButtonStates)
        select_2.toggleClass('btn-secondary')
        select_2.toggleClass('btn-primary')
    }
    if (document.getElementById('page_cssjs').style.display === 'block') {
        void 0
    }
    else {
        section_2.css('display','block')
        section_1.css('display','none')
        section_3.css('display','none')
    }
});

document.getElementById('select-button-3').addEventListener('click', function(e) {
    if (select_3.hasClass('btn-primary')) {
        void 0;
    }
    else {
        select_list.forEach(resetButtonStates)
        select_3.toggleClass('btn-secondary')
        select_3.toggleClass('btn-primary')
    }
    if (document.getElementById('page_seo').style.display === 'block') {
        void 0
    }
    else {
        section_3.css('display','block')
        section_1.css('display','none')
        section_2.css('display','none')
    }
});
