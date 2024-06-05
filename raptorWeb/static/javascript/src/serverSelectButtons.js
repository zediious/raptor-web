select_1 = $('#select-button-1')
select_2 = $('#select-button-2')
select_3 = $('#select-button-3')
select_4 = $('#select-button-4')
select_5 = $('#select-button-5')

section_1 = $('#server_general')
section_2 = $('#server_information')
section_3 = $('#server_querying')
section_4 = $('#server_discord_announcements')
section_5 = $('#server_donations')

select_list = [select_1, select_2, select_3, select_4, select_5]

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
    if (document.getElementById('server_general').style.display === 'block') {
        void 0
    }
    else {
        section_1.css('display','block')
        section_2.css('display','none')
        section_3.css('display','none')
        section_4.css('display','none')
        section_5.css('display','none')
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
    if (document.getElementById('server_information').style.display === 'block') {
        void 0
    }
    else {
        section_2.css('display','block')
        section_1.css('display','none')
        section_3.css('display','none')
        section_4.css('display','none')
        section_5.css('display','none')
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
    if (document.getElementById('server_querying').style.display === 'block') {
        void 0
    }
    else {
        section_3.css('display','block')
        section_1.css('display','none')
        section_2.css('display','none')
        section_4.css('display','none')
        section_5.css('display','none')
    }
});

document.getElementById('select-button-4').addEventListener('click', function(e) {
    if (select_4.hasClass('btn-primary')) {
        void 0;
    }
    else {
        select_list.forEach(resetButtonStates)
        select_4.toggleClass('btn-secondary')
        select_4.toggleClass('btn-primary')
    }
    if (document.getElementById('server_discord_announcements').style.display === 'block') {
        void 0
    }
    else {
        section_4.css('display','block')
        section_1.css('display','none')
        section_2.css('display','none')
        section_3.css('display','none')
        section_5.css('display','none')
    }
});

document.getElementById('select-button-5').addEventListener('click', function(e) {
    if (select_5.hasClass('btn-primary')) {
        void 0;
    }
    else {
        select_list.forEach(resetButtonStates)
        select_5.toggleClass('btn-secondary')
        select_5.toggleClass('btn-primary')
    }
    if (document.getElementById('server_donations').style.display === 'block') {
        void 0
    }
    else {
        section_5.css('display','block')
        section_1.css('display','none')
        section_2.css('display','none')
        section_3.css('display','none')
        section_4.css('display','none')
    }
});